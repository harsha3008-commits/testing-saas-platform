"use client"

import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface TestTrend {
  date: string
  passed: number
  failed: number
}

interface CategoryBreakdown {
  category: string
  score: number
}

interface PassRateHistory {
  name: string
  value: number
  [key: string]: string | number
}

interface AnalyticsChartsProps {
  testTrends: TestTrend[]
  categoryBreakdown: CategoryBreakdown[]
  passRateHistory: PassRateHistory[]
}

export function AnalyticsCharts({ testTrends, categoryBreakdown, passRateHistory }: AnalyticsChartsProps) {
  const COLORS = ['#27AE60', '#2F80ED', '#F2C94C', '#EB5757']

  return (
    <div className="space-y-6">
      {/* Test Trends Over Time */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Test Trends (Last 30 Days)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={testTrends}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="passed" stroke="#27AE60" strokeWidth={2} />
            <Line type="monotone" dataKey="failed" stroke="#EB5757" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Category Score Breakdown */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Score by Category</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={categoryBreakdown}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="category" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="score" fill="#2F80ED" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pass Rate Distribution */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Test Status Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={passRateHistory}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(props: { name?: string; percent?: number }) => {
                const name = props.name || '';
                const percent = props.percent || 0;
                return `${name}: ${(percent * 100).toFixed(0)}%`;
              }}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {passRateHistory.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}