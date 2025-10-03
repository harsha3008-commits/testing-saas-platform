import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-black/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Testing SaaS
          </div>
          <div className="flex gap-4">
            <Link href="/dashboard">
              <Button variant="ghost" className="text-gray-300 hover:text-white">
                Dashboard
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-4 pt-24 pb-20">
        <div className="text-center max-w-5xl mx-auto">
          {/* Animated Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/20 mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span>
            </span>
            <span className="text-sm text-purple-300">AI-Powered Testing Platform</span>
          </div>

          <h1 className="text-6xl md:text-7xl lg:text-8xl font-extrabold mb-6 leading-tight">
            <span className="bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent">
              Test Smarter,
            </span>
            <br />
            <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent">
              Ship Faster
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-400 mb-10 max-w-3xl mx-auto leading-relaxed">
            Automated code testing, security scanning, and AI-powered fix suggestions.
            Built for modern development teams.
          </p>
          <div className="flex gap-4 justify-center flex-wrap mb-12">
            <Link href="/dashboard">
              <Button size="lg" className="text-lg px-10 py-6 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold rounded-xl">
                Start Testing Free
              </Button>
            </Link>
            <Link href="https://github.com/harsha3008-commits/testing-saas-platform">
              <Button size="lg" variant="outline" className="text-lg px-10 py-6 border-2 border-gray-700 hover:border-purple-500 text-white rounded-xl">
                View on GitHub →
              </Button>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto pt-8 border-t border-gray-800">
            <div>
              <div className="text-3xl font-bold text-purple-400">10+</div>
              <div className="text-sm text-gray-500">Testing Engines</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-pink-400">99.9%</div>
              <div className="text-sm text-gray-500">Uptime</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-400">AI</div>
              <div className="text-sm text-gray-500">Powered Fixes</div>
            </div>
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
      <div className="py-24 bg-black">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
              Powered by modern tech
            </span>
          </h2>
          <p className="text-center text-gray-500 mb-16">Industry-leading technologies for reliability and scale</p>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <Card className="p-8 bg-gradient-to-br from-gray-900 to-gray-800 border-gray-800">
              <h3 className="text-2xl font-bold mb-6 text-purple-400">Frontend</h3>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-gray-300">Next.js 15 with App Router</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-gray-300">TypeScript & TailwindCSS</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-gray-300">shadcn/ui Components</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-gray-300">Recharts Analytics</span>
                </div>
              </div>
            </Card>
            
            <Card className="p-8 bg-gradient-to-br from-gray-900 to-gray-800 border-gray-800">
              <h3 className="text-2xl font-bold mb-6 text-pink-400">Backend</h3>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
                  <span className="text-gray-300">FastAPI (Python)</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
                  <span className="text-gray-300">PostgreSQL & Redis</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
                  <span className="text-gray-300">Celery + RabbitMQ</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
                  <span className="text-gray-300">Docker & GitHub Actions</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-4 py-24 text-center">
        <div className="max-w-4xl mx-auto bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-3xl p-16 border border-purple-500/30">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              Ready to ship with confidence?
            </span>
          </h2>
          <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
            Join teams using our platform to deliver better code, faster.
          </p>
          <Link href="/dashboard">
            <Button size="lg" className="text-lg px-12 py-6 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold rounded-xl">
              Get Started Free →
            </Button>
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 bg-black">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              Testing SaaS
            </div>
            <div className="flex gap-8 text-gray-400">
              <Link href="/dashboard" className="hover:text-purple-400 transition-colors">Dashboard</Link>
              <Link href="/organizations" className="hover:text-purple-400 transition-colors">Organizations</Link>
              <Link href="/settings/notifications" className="hover:text-purple-400 transition-colors">Settings</Link>
              <Link href="https://github.com/harsha3008-commits/testing-saas-platform" className="hover:text-purple-400 transition-colors">GitHub</Link>
            </div>
          </div>
          <div className="text-center mt-8 text-gray-600 text-sm">
            © 2025 Testing SaaS Platform. Built with Next.js and FastAPI.
          </div>
        </div>
      </footer>
    </div>
  );
}
