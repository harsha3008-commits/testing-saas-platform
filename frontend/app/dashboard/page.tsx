"use client"

import { DashboardLayout } from '@/components/dashboard-layout'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function DashboardPage() {
  const stats = [
    { label: 'Total Projects', value: '12', change: '+2 this month', trend: 'up', gradient: 'from-purple-500 to-pink-500' },
    { label: 'Tests Run Today', value: '47', change: '+8 from yesterday', trend: 'up', gradient: 'from-blue-500 to-cyan-500' },
    { label: 'Pass Rate', value: '94%', change: '+3% improvement', trend: 'up', gradient: 'from-green-500 to-emerald-500' },
    { label: 'Critical Issues', value: '3', change: '-2 resolved', trend: 'down', gradient: 'from-orange-500 to-red-500' },
  ]

  const recentTests = [
    { project: 'E-commerce API', status: 'passed', score: 95, time: '2 hours ago' },
    { project: 'Mobile App', status: 'failed', score: 67, time: '4 hours ago' },
    { project: 'Analytics Dashboard', status: 'passed', score: 88, time: '6 hours ago' },
    { project: 'Payment Service', status: 'running', score: 0, time: 'In progress' },
  ]

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Welcome Section */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-2">
              <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                Welcome to Lyzo AI
              </span>
            </h1>
            <p className="text-gray-400">Your intelligent testing platform dashboard</p>
          </div>
          <Link href="/projects/new">
            <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold">
              + New Test
            </Button>
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat) => (
            <div key={stat.label} className="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-800 rounded-xl p-6 hover:border-purple-500/50 transition-all duration-300 group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-gray-400">{stat.label}</h3>
                <span className={`text-xs px-3 py-1 rounded-full bg-gradient-to-r ${stat.gradient} text-white font-medium`}>
                  {stat.change}
                </span>
              </div>
              <p className="text-4xl font-extrabold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                {stat.value}
              </p>
            </div>
          ))}
        </div>

        {/* Recent Tests */}
        <div className="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-800 rounded-xl overflow-hidden">
          <div className="p-6 border-b border-gray-800">
            <h2 className="text-2xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
              Recent Test Runs
            </h2>
          </div>
          <div className="p-6">
            <div className="space-y-3">
              {recentTests.map((test, index) => (
                <div key={index} className="flex items-center justify-between p-5 bg-black/40 border border-gray-800 rounded-xl hover:border-purple-500/50 transition-all duration-300 group">
                  <div className="flex items-center gap-4">
                    <div className={`w-3 h-3 rounded-full ${
                      test.status === 'passed' ? 'bg-green-500 shadow-lg shadow-green-500/50' :
                      test.status === 'failed' ? 'bg-red-500 shadow-lg shadow-red-500/50' :
                      'bg-yellow-500 animate-pulse shadow-lg shadow-yellow-500/50'
                    }`} />
                    <div>
                      <h3 className="font-semibold text-white group-hover:text-purple-400 transition-colors">{test.project}</h3>
                      <p className="text-sm text-gray-500">{test.time}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    {test.status !== 'running' && (
                      <div className="text-right">
                        <p className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">{test.score}%</p>
                        <p className="text-xs text-gray-500">Score</p>
                      </div>
                    )}
                    <Button className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 hover:border-purple-500 text-white">
                      View Report
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="bg-gradient-to-br from-purple-900/40 to-pink-900/40 border border-purple-500/30 p-8 rounded-xl hover:border-purple-500 transition-all duration-300 group text-left">
            <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">🔍</div>
            <h3 className="text-xl font-bold mb-2 text-white">Run New Test</h3>
            <p className="text-sm text-gray-400">Upload project or connect repository</p>
          </button>
          <button className="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-800 p-8 rounded-xl hover:border-pink-500/50 transition-all duration-300 group text-left">
            <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">📊</div>
            <h3 className="text-xl font-bold mb-2 text-white">View Analytics</h3>
            <p className="text-sm text-gray-400">Check performance trends</p>
          </button>
          <button className="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-800 p-8 rounded-xl hover:border-purple-500/50 transition-all duration-300 group text-left">
            <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">⚙️</div>
            <h3 className="text-xl font-bold mb-2 text-white">Configure Tests</h3>
            <p className="text-sm text-gray-400">Customize test parameters</p>
          </button>
        </div>
      </div>
    </DashboardLayout>
  )
}