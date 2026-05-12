import { BarChart3, Clapperboard, LayoutDashboard, MapPinned, MonitorPlay, Settings, UserRound, Wallet } from 'lucide-react'

const items = [
  { id: 'overview', icon: LayoutDashboard, label: 'Dashboard' },
  { id: 'movies', icon: Clapperboard, label: 'Movies' },
  { id: 'cinemas', icon: MapPinned, label: 'Cinemas' },
  { id: 'shows', icon: MonitorPlay, label: 'Shows' },
  { id: 'analytics', icon: BarChart3, label: 'Analytics' },
  { id: 'revenue', icon: Wallet, label: 'Revenue' },
  { id: 'users', icon: UserRound, label: 'Users' },
  { id: 'settings', icon: Settings, label: 'Settings' },
]

export function AdminSidebar({ active, onSelect }) {
  return (
    <aside className="glass-panel rounded-[28px] p-4">
      <p className="mb-4 px-3 text-xs uppercase tracking-[0.35em] text-neon/75">Management</p>
      <div className="space-y-1">
        {items.map((item) => {
          const Icon = item.icon
          const current = item.id === active
          return (
            <button
              key={item.id}
              onClick={() => onSelect(item.id)}
              className={`flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-left text-sm transition ${
                current ? 'bg-neon/12 text-foreground shadow-card' : 'text-muted hover:bg-card/60 hover:text-foreground'
              }`}
            >
              <Icon className="size-4" />
              {item.label}
            </button>
          )
        })}
      </div>
    </aside>
  )
}
