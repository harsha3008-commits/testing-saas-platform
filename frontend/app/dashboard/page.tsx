"use client"

import { DashboardLayout } from '@/components/dashboard-layout'

export default function DashboardPage() {
  const stats = [
    { label: 'Total Projects', value: '12', change: '+2 this month', trend: 'up' },
    { label: 'Tests Run Today', value: '47', change: '+8 from yesterday', trend: 'up' },
    { label: 'Pass Rate', value: '94%', change: '+3% improvement', trend: 'up' },
    { label: 'Critical Issues', value: '3', change: '-2 resolved', trend: 'down' },
  ]

  const recentTests = [
    { project: 'E-commerce API', status: 'passed', score: 95, time: '2 hours ago' },
    { project: 'Mobile App', status: 'failed', score: 67, time: '4 hours ago' },
    { project: 'Analytics Dashboard', status: 'passed', score: 88, time: '6 hours ago' },
    { project: 'Payment Service', status: 'running', score: 0, time: 'In progress' },
  ]

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat) => (
            <div key={stat.label} className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium text-muted-foreground">{stat.label}</h3>
                <span className={`text-xs px-2 py-1 rounded ${
                  stat.trend === 'up' ? 'bg-success/10 text-success' : 'bg-destructive/10 text-destructive'
                }`}>
                  {stat.change}
                </span>
              </div>
              <p className="text-3xl font-bold mt-2">{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Recent Tests */}
        <div className="bg-card border border-border rounded-lg">
          <div className="p-6 border-b border-border">
            <h2 className="text-xl font-semibold">Recent Test Runs</h2>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentTests.map((test, index) => (
                <div key={index} className="flex items-center justify-between p-4 border border-border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className={`w-3 h-3 rounded-full ${
                      test.status === 'passed' ? 'bg-success' :
                      test.status === 'failed' ? 'bg-destructive' :
                      'bg-warning animate-pulse'
                    }`} />
                    <div>
                      <h3 className="font-medium">{test.project}</h3>
                      <p className="text-sm text-muted-foreground">{test.time}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    {test.status !== 'running' && (
                      <div className="text-right">
                        <p className="font-semibold">{test.score}%</p>
                        <p className="text-xs text-muted-foreground">Score</p>
                      </div>
                    )}
                    <button className="px-4 py-2 bg-accent text-accent-foreground rounded-lg hover:opacity-90 transition-opacity">
                      View Report
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="bg-accent text-accent-foreground p-6 rounded-lg hover:opacity-90 transition-opacity">
            <h3 className="text-lg font-semibold mb-2">🔍 Run New Test</h3>
            <p className="text-sm opacity-90">Upload project or connect repository</p>
          </button>
          <button className="bg-card border border-border p-6 rounded-lg hover:bg-secondary transition-colors">
            <h3 className="text-lg font-semibold mb-2">📊 View Analytics</h3>
            <p className="text-sm text-muted-foreground">Check performance trends</p>
          </button>
          <button className="bg-card border border-border p-6 rounded-lg hover:bg-secondary transition-colors">
            <h3 className="text-lg font-semibold mb-2">⚙️ Configure Tests</h3>
            <p className="text-sm text-muted-foreground">Customize test parameters</p>
          </button>
        </div>
      </div>
    </DashboardLayout>
  )
}