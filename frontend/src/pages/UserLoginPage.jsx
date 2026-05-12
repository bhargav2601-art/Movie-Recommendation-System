import { Eye, EyeOff, PlayCircle, Sparkles } from 'lucide-react'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../hooks/useToast'


export function UserLoginPage() {
  const navigate = useNavigate()
  const { loginUser } = useAuth()
  const { push } = useToast()
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({ username: '', password: '' })

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    try {
      await loginUser(form)
      push({ title: 'Welcome back. Your movie world is ready.' })
      navigate('/home')
    } catch (error) {
      push({ title: error?.response?.data?.detail || 'Unable to sign you in.', tone: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="section-shell flex min-h-[calc(100vh-9rem)] items-center py-14">
      <div className="grid w-full gap-8 lg:grid-cols-[1.05fr_0.75fr]">
        <div className="overflow-hidden rounded-[36px] border border-border/30 bg-[radial-gradient(circle_at_top_left,rgba(244,114,182,0.14),transparent_28%),radial-gradient(circle_at_70%_25%,rgba(var(--accent-rgb),0.16),transparent_30%),linear-gradient(180deg,rgba(var(--background-soft-rgb),1),rgba(var(--background-deep-rgb),1))] p-8 md:p-10 shadow-card">
          <div className="inline-flex items-center gap-3 rounded-full border border-border/30 bg-card/55 px-4 py-2 text-sm text-muted">
            <Sparkles className="size-4 text-gold" />
            Customer access portal
          </div>
          <h1 className="mt-6 font-display text-5xl font-extrabold leading-tight text-foreground">
            Sign in for your next big-screen plan.
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-8 text-muted">
            Track watchlists, unlock smart recommendations, revisit past bookings, and jump back into the movies that fit your mood.
          </p>
          <div className="mt-8 grid gap-4 md:grid-cols-3">
            {[
              ['OTT-inspired', 'A clean, friendly login built for movie lovers.'],
              ['Smart picks', 'Recommendations tuned by genre, language, and format.'],
              ['Fast booking', 'Go from browse to seat selection without friction.'],
            ].map(([title, copy]) => (
              <div key={title} className="rounded-[28px] border border-border/30 bg-card/45 p-5">
                <p className="text-sm font-semibold text-foreground">{title}</p>
                <p className="mt-2 text-sm leading-7 text-muted">{copy}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-panel rounded-[34px] p-7 md:p-8">
          <p className="text-xs uppercase tracking-[0.35em] text-neon/80">User Login</p>
          <h2 className="mt-3 font-display text-4xl font-extrabold text-foreground">Welcome back</h2>
          <p className="mt-3 text-sm leading-7 text-muted">Use your customer account to browse films, manage tickets, and continue your booking journey.</p>

          <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
            <Input
              placeholder="Username"
              value={form.username}
              onChange={(event) => setForm((prev) => ({ ...prev, username: event.target.value }))}
              required
            />
            <div className="relative">
              <Input
                placeholder="Password"
                type={showPassword ? 'text' : 'password'}
                value={form.password}
                onChange={(event) => setForm((prev) => ({ ...prev, password: event.target.value }))}
                className="pr-12"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword((value) => !value)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-subtle"
              >
                {showPassword ? <EyeOff className="size-4" /> : <Eye className="size-4" />}
              </button>
            </div>
            <Button className="w-full" disabled={loading}>
              {loading ? 'Signing in...' : 'Login'}
            </Button>
          </form>

          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            <button className="rounded-2xl border border-border/30 bg-card/55 px-4 py-3 text-sm text-muted">
              Continue with Google
            </button>
            <button className="rounded-2xl border border-border/30 bg-card/55 px-4 py-3 text-sm text-muted">
              Continue with Apple
            </button>
          </div>

          <div className="mt-6 flex items-center justify-between rounded-2xl border border-border/30 bg-card/55 px-4 py-4">
            <div>
              <p className="text-sm text-muted">New to CineVerse?</p>
              <p className="text-xs uppercase tracking-[0.28em] text-subtle">Create your customer account</p>
            </div>
            <Link to="/signup">
              <Button variant="secondary">
                <PlayCircle className="mr-2 size-4" />
                Sign Up
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}
