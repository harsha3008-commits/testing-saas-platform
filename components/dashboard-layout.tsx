"use client"

import { ReactNode } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface DashboardLayoutProps {
  children: ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname()

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Projects', href: '/projects', icon: '📁' },
    { name: 'Test Reports', href: '/reports', icon: '📄' },
    { name: 'Settings', href: '/settings', icon: '⚙️' },
  ]

  return (
    <div className="min-h-screen bg-secondary">
      {/* Sidebar */}
      <aside className="fixed inset-y-0 left-0 w-64 bg-primary text-primary-foreground">
        <div className="flex h-16 items-center justify-center border-b border-border">
          <h1 className="text-xl font-bold">Testing SaaS</h1>
        </div>
        <nav className="p-4 space-y-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-accent text-accent-foreground'
                    : 'hover:bg-secondary hover:text-foreground'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.name}</span>
              </Link>
            )
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <div className="ml-64">
        {/* Header */}
        <header className="h-16 bg-card border-b border-border px-6 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Universal Testing Platform</h2>
          <div className="flex items-center gap-4">
            <button className="px-4 py-2 bg-accent text-accent-foreground rounded-lg hover:opacity-90 transition-opacity">
              New Test Run
            </button>
          </div>
        </header>

        {/* Page Content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  )
}