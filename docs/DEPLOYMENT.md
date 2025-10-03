# Deployment Guide - Testing SaaS Platform

## Production Deployment Architecture

### Infrastructure Overview
- **Frontend:** Vercel or AWS Amplify
- **Backend:** AWS EC2 or Google Cloud Run
- **Database:** AWS RDS PostgreSQL
- **Cache/Queue:** AWS ElastiCache Redis
- **Storage:** AWS S3 for reports and uploads
- **CDN:** CloudFront for static assets

## Environment Configuration

### Production Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@production-db.amazonaws.com:5432/testing_saas

# Redis
REDIS_URL=redis://production-redis.cache.amazonaws.com:6379/0

# Security
SECRET_KEY=your-production-secret-key-256-bit
JWT_SECRET_KEY=your-jwt-secret-key-256-bit

# API Keys
STRIPE_API_KEY=sk_live_your_live_stripe_key
OPENAI_API_KEY=sk-your-production-openai-key
GITHUB_TOKEN=ghp_your_github_personal_access_token

# AWS
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=testing-saas-production-reports
AWS_REGION=us-east-1

# Application
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Deployment Steps

### 1. Database Setup

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier testing-saas-prod \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username admin \
  --master-user-password YourSecurePassword \
  --allocated-storage 100

# Initialize schema
psql -h production-db.amazonaws.com -U admin -d testing_saas -f database/schema.sql
```

### 2. Backend Deployment (AWS EC2)

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Clone repository
git clone https://github.com/yourorg/testing-saas-platform.git
cd testing-saas-platform/backend

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure systemd service
sudo nano /etc/systemd/system/testing-saas-api.service
```

**Service Configuration:**
```ini
[Unit]
Description=Testing SaaS API
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/testing-saas-platform/backend
Environment="PATH=/home/ec2-user/testing-saas-platform/backend/venv/bin"
EnvironmentFile=/home/ec2-user/testing-saas-platform/.env
ExecStart=/home/ec2-user/testing-saas-platform/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl enable testing-saas-api
sudo systemctl start testing-saas-api
```

### 3. Celery Workers

```bash
# Configure Celery service
sudo nano /etc/systemd/system/testing-saas-celery.service
```

```ini
[Unit]
Description=Testing SaaS Celery Worker
After=network.target redis.service

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/testing-saas-platform/backend
Environment="PATH=/home/ec2-user/testing-saas-platform/backend/venv/bin"
EnvironmentFile=/home/ec2-user/testing-saas-platform/.env
ExecStart=/home/ec2-user/testing-saas-platform/backend/venv/bin/celery -A tasks worker --loglevel=info

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable testing-saas-celery
sudo systemctl start testing-saas-celery
```

### 4. Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

**vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "https://api.yourdomain.com"
  }
}
```

### 5. NGINX Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 6. SSL Certificate (Let's Encrypt)

```bash
sudo certbot --nginx -d api.yourdomain.com
```

## Monitoring and Logging

### CloudWatch Setup
```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

# Configure log collection
sudo nano /opt/aws/amazon-cloudwatch-agent/etc/config.json
```

### Health Checks
- Backend: `GET /health`
- Database: Connection pooling monitoring
- Redis: Memory usage alerts
- Celery: Task queue length monitoring

## Scaling Configuration

### Auto Scaling Group
```bash
# Create launch template
aws ec2 create-launch-template \
  --launch-template-name testing-saas-template \
  --launch-template-data '{"ImageId":"ami-xxxxx","InstanceType":"t3.medium"}'

# Create auto scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name testing-saas-asg \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 2
```

## Backup Strategy

### Database Backups
```bash
# Automated daily backups via RDS
aws rds modify-db-instance \
  --db-instance-identifier testing-saas-prod \
  --backup-retention-period 30 \
  --preferred-backup-window "03:00-04:00"
```

### S3 Report Backups
```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket testing-saas-production-reports \
  --versioning-configuration Status=Enabled
```

## CI/CD Pipeline (GitHub Actions)

```yaml
name: Deploy Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          ssh ec2-user@production-server 'cd testing-saas-platform && git pull && sudo systemctl restart testing-saas-api'
      
      - name: Deploy Frontend
        run: |
          cd frontend
          vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

## Security Checklist

- [ ] HTTPS enabled on all endpoints
- [ ] Database credentials rotated
- [ ] API rate limiting configured
- [ ] CORS properly configured
- [ ] Security headers enabled
- [ ] DDoS protection (CloudFlare)
- [ ] Regular security audits
- [ ] Dependency vulnerability scanning

## Cost Optimization

- Use Reserved Instances for predictable workloads
- Implement auto-scaling for variable loads
- S3 lifecycle policies for old reports
- CloudFront caching for static assets
- Database connection pooling

## Troubleshooting

### Common Issues

**API not responding:**
```bash
sudo systemctl status testing-saas-api
sudo journalctl -u testing-saas-api -f
```

**Database connection errors:**
```bash
# Check security groups
aws ec2 describe-security-groups --group-ids sg-xxxxx
```

**High memory usage:**
```bash
# Monitor Celery workers
celery -A tasks inspect stats
```

## Rollback Procedure

```bash
# Backend rollback
git checkout previous-stable-commit
sudo systemctl restart testing-saas-api

# Frontend rollback
vercel rollback production
```

## Support

For deployment issues, contact: devops@yourdomain.com