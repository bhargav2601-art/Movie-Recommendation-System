import { memo } from 'react'
import { Bell, Clapperboard, Heart, Home, Ticket, UserCircle2 } from 'lucide-react'
import { Link, NavLink, useNavigate } from 'react-router-dom'

import { useAuth } from '../../context/AuthContext'
import { Button } from '../ui/button'
import { ThemeToggle } from './ThemeToggle'


const publicLinks = [
  { to: '/home', label: 'Home', icon: Home },
  { to: '/browse', label: 'Movies', icon: Clapperboard },
  { to: '/cinemas', label: 'Cinemas', icon: Clapperboard },
]

const userLinks = [
  { to: '/tickets', label: 'My Tickets', icon: Ticket },
  { to: '/watchlist', label: 'Watchlist', icon: Heart },
  { to: '/profile', label: 'Profile', icon: UserCircle2 },
]


export const Navbar = memo(function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <header className="sticky top-0 z-40 border-b border-border/25 bg-[linear-gradient(180deg,rgba(var(--card-rgb),0.74),rgba(var(--card-rgb),0.56))] shadow-[0_10px_40px_rgba(var(--background-deep-rgb),0.12)] backdrop-blur-2xl">
      <div className="section-shell flex h-20 items-center justify-between gap-4">
        <Link to="/home" className="flex items-center gap-3">
          <div className="flex size-11 items-center justify-center rounded-2xl bg-gradient-to-br from-gold to-neon text-ink shadow-glow">
            <Clapperboard className="size-5" />
          </div>
          <div>
            <p className="font-display text-lg font-extrabold tracking-wide text-foreground">CineVerse</p>
            <p className="text-xs uppercase tracking-[0.35em] text-subtle">Premium Tickets</p>
          </div>
        </Link>

        <nav className="hidden items-center gap-2 rounded-full border border-border/35 bg-[rgba(var(--card-rgb),0.42)] px-2 py-2 shadow-card lg:flex">
          {[...publicLinks, ...(user?.role === 'user' ? userLinks : [])].map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `rounded-full px-4 py-2 text-sm transition ${
                  isActive ? 'bg-background-elevated/90 text-foreground shadow-card' : 'text-muted hover:text-foreground'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <button
            type="button"
            className="glass-button hidden size-11 items-center justify-center md:inline-flex"
            aria-label="Notifications"
            title="Notifications"
          >
            <Bell className="size-4 text-muted" />
          </button>
          <ThemeToggle />
          {user?.role === 'user' ? (
            <>
              <div className="hidden items-center gap-3 rounded-full border border-border/35 bg-[rgba(var(--card-rgb),0.42)] px-4 py-2 md:flex">
                <UserCircle2 className="size-4 text-neon" />
                <div>
                  <p className="text-sm font-semibold text-foreground">{user.username}</p>
                  <p className="text-[11px] uppercase tracking-[0.2em] text-subtle">member</p>
                </div>
              </div>
              <Button variant="ghost" onClick={handleLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link to="/login" className="hidden md:block">
                <Button variant="secondary">Login</Button>
              </Link>
              <Link to="/signup">
                <Button>
                  <Ticket className="mr-2 size-4" />
                  Book Now
                </Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  )
})
