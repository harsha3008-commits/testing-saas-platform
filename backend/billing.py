"""
Stripe Billing Integration
Handles subscription management, payment processing, and usage tracking
"""
import stripe
import os
from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseModel

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_API_KEY', 'sk_test_your_key_here')

class SubscriptionPlan(BaseModel):
    name: str
    price_id: str
    features: Dict
    monthly_price: int
    test_runs_limit: int

# Subscription Plans
PLANS = {
    'free': SubscriptionPlan(
        name='Free',
        price_id='price_free',
        features={'test_runs': 5, 'storage_gb': 1, 'ai_fixes': False},
        monthly_price=0,
        test_runs_limit=5
    ),
    'starter': SubscriptionPlan(
        name='Starter',
        price_id='price_starter',
        features={'test_runs': 50, 'storage_gb': 10, 'ai_fixes': True},
        monthly_price=2900,
        test_runs_limit=50
    ),
    'pro': SubscriptionPlan(
        name='Pro',
        price_id='price_pro',
        features={'test_runs': 500, 'storage_gb': 100, 'ai_fixes': True, 'priority_support': True},
        monthly_price=9900,
        test_runs_limit=500
    ),
    'enterprise': SubscriptionPlan(
        name='Enterprise',
        price_id='price_enterprise',
        features={'test_runs': -1, 'storage_gb': -1, 'ai_fixes': True, 'priority_support': True, 'dedicated_account': True},
        monthly_price=29900,
        test_runs_limit=-1
    )
}

class BillingManager:
    """Manages Stripe billing operations"""
    
    @staticmethod
    def create_customer(email: str, name: str) -> Dict:
        """Create a new Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={'platform': 'testing_saas'}
            )
            return {
                'success': True,
                'customer_id': customer.id,
                'email': customer.email
            }
        except stripe.error.StripeError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def create_subscription(customer_id: str, plan: str) -> Dict:
        """Create a subscription for a customer"""
        try:
            if plan not in PLANS:
                return {'success': False, 'error': 'Invalid plan'}
            
            plan_info = PLANS[plan]
            
            if plan == 'free':
                return {
                    'success': True,
                    'subscription_id': None,
                    'plan': plan,
                    'message': 'Free plan activated'
                }
            
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': plan_info.price_id}],
                metadata={'plan': plan}
            )
            
            return {
                'success': True,
                'subscription_id': subscription.id,
                'status': subscription.status,
                'current_period_start': subscription.current_period_start,
                'current_period_end': subscription.current_period_end
            }
        except stripe.error.StripeError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def cancel_subscription(subscription_id: str) -> Dict:
        """Cancel a subscription"""
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            return {
                'success': True,
                'subscription_id': subscription.id,
                'status': subscription.status
            }
        except stripe.error.StripeError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def upgrade_subscription(subscription_id: str, new_plan: str) -> Dict:
        """Upgrade or downgrade a subscription"""
        try:
            if new_plan not in PLANS:
                return {'success': False, 'error': 'Invalid plan'}
            
            plan_info = PLANS[new_plan]
            
            subscription = stripe.Subscription.modify(
                subscription_id,
                items=[{'price': plan_info.price_id}],
                proration_behavior='create_prorations'
            )
            
            return {
                'success': True,
                'subscription_id': subscription.id,
                'new_plan': new_plan,
                'status': subscription.status
            }
        except stripe.error.StripeError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def create_checkout_session(customer_id: str, plan: str, success_url: str, cancel_url: str) -> Dict:
        """Create a Stripe Checkout session"""
        try:
            if plan not in PLANS or plan == 'free':
                return {'success': False, 'error': 'Invalid plan for checkout'}
            
            plan_info = PLANS[plan]
            
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': plan_info.price_id,
                    'quantity': 1
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url
            )
            
            return {
                'success': True,
                'session_id': session.id,
                'url': session.url
            }
        except stripe.error.StripeError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def handle_webhook(payload: bytes, sig_header: str) -> Dict:
        """Handle Stripe webhook events"""
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', '')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            
            event_type = event['type']
            
            if event_type == 'customer.subscription.created':
                return {'event': 'subscription_created', 'data': event['data']['object']}
            
            elif event_type == 'customer.subscription.updated':
                return {'event': 'subscription_updated', 'data': event['data']['object']}
            
            elif event_type == 'customer.subscription.deleted':
                return {'event': 'subscription_deleted', 'data': event['data']['object']}
            
            elif event_type == 'invoice.payment_succeeded':
                return {'event': 'payment_succeeded', 'data': event['data']['object']}
            
            elif event_type == 'invoice.payment_failed':
                return {'event': 'payment_failed', 'data': event['data']['object']}
            
            return {'event': 'unhandled', 'type': event_type}
            
        except stripe.error.SignatureVerificationError:
            return {'error': 'Invalid signature'}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def check_usage_limits(user_plan: str, current_usage: Dict) -> Dict:
        """Check if user has exceeded their plan limits"""
        plan = PLANS.get(user_plan)
        
        if not plan:
            return {'allowed': False, 'reason': 'Invalid plan'}
        
        test_runs_used = current_usage.get('test_runs', 0)
        
        if plan.test_runs_limit == -1:  # Unlimited
            return {'allowed': True}
        
        if test_runs_used >= plan.test_runs_limit:
            return {
                'allowed': False,
                'reason': f'Monthly limit of {plan.test_runs_limit} test runs reached',
                'upgrade_required': True
            }
        
        return {
            'allowed': True,
            'remaining': plan.test_runs_limit - test_runs_used
        }