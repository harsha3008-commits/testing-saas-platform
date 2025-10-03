import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section */}
      <div className="container mx-auto px-4 pt-20 pb-16">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Testing SaaS Platform
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8">
            Automated code testing, security scanning, and AI-powered fix suggestions
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link href="/dashboard">
              <Button size="lg" className="text-lg px-8">
                Get Started
              </Button>
            </Link>
            <Link href="https://github.com/harsha3008-commits/testing-saas-platform">
              <Button size="lg" variant="outline" className="text-lg px-8">
                View on GitHub
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Core Features</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card className="p-6">
            <div className="text-3xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold mb-2">Multi-Engine Testing</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Support for ESLint, Pylint, PyTest, Jest, and more testing engines
            </p>
          </Card>

          <Card className="p-6">
            <div className="text-3xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold mb-2">Security Scanning</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Integrated Snyk, Bandit, and OWASP ZAP for vulnerability detection
            </p>
          </Card>

          <Card className="p-6">
            <div className="text-3xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold mb-2">AI-Powered Fixes</h3>
            <p className="text-gray-600 dark:text-gray-400">
              OpenAI integration provides intelligent suggestions for test failures
            </p>
          </Card>

          <Card className="p-6">
            <div className="text-3xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2">Analytics Dashboard</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Track test trends, coverage, and failure patterns over time
            </p>
          </Card>

          <Card className="p-6">
            <div className="text-3xl mb-4">👥</div>
            <h3 className="text-xl font-semibold mb-2">Team Collaboration</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Organizations, role-based access, and team project management
            </p>
          </Card>

          <Card className="p-6">
            <div className="text-3xl mb-4">🔔</div>
            <h3 className="text-xl font-semibold mb-2">Smart Notifications</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Slack, Discord, Email, and WhatsApp integration for alerts
            </p>
          </Card>
        </div>
      </div>

      {/* Tech Stack Section */}
      <div className="bg-gray-50 dark:bg-gray-900 py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Built With Modern Tech</h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div>
              <h3 className="text-xl font-semibold mb-4">Frontend</h3>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>• Next.js 15 with App Router</li>
                <li>• TypeScript & TailwindCSS</li>
                <li>• shadcn/ui Components</li>
                <li>• Recharts Analytics</li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4">Backend</h3>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>• FastAPI (Python)</li>
                <li>• PostgreSQL & Redis</li>
                <li>• Celery + RabbitMQ</li>
                <li>• Docker & GitHub Actions</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl font-bold mb-6">Ready to improve your code quality?</h2>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
          Start testing your projects with our comprehensive automated testing platform
        </p>
        <Link href="/dashboard">
          <Button size="lg" className="text-lg px-12">
            Launch Dashboard
          </Button>
        </Link>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-700 py-8">
        <div className="container mx-auto px-4 text-center text-gray-600 dark:text-gray-400">
          <p>© 2025 Testing SaaS Platform. Built with Next.js and FastAPI.</p>
          <div className="flex gap-6 justify-center mt-4">
            <Link href="/dashboard" className="hover:text-blue-600">Dashboard</Link>
            <Link href="/organizations" className="hover:text-blue-600">Organizations</Link>
            <Link href="/settings/notifications" className="hover:text-blue-600">Settings</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
