import { Eye, EyeOff, Film, Sparkles } from 'lucide-react'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../hooks/useToast'


export function UserSignupPage() {
  const navigate = useNavigate()
  const { signup } = useAuth()
  const { push } = useToast()
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({ username: '', email: '', password: '' })

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    try {
      await signup(form)
      push({ title: 'Account created. Let’s find your next watch.' })
      navigate('/home')
    } catch (error) {
      push({ title: error?.response?.data?.detail || 'Unable to create your account.', tone: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="section-shell flex min-h-[calc(100vh-9rem)] items-center py-14">
      <div className="grid w-full gap-8 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="glass-panel rounded-[34px] p-7 md:p-8">
          <p className="text-xs uppercase tracking-[0.35em] text-gold/80">User Signup</p>
          <h2 className="mt-3 font-display text-4xl font-extrabold text-foreground">Create your account</h2>
          <p className="mt-3 text-sm leading-7 text-muted">Set up a customer profile for bookings, wishlists, recommendations, and ticket history.</p>

          <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
            <Input
              placeholder="Username"
              value={form.username}
              onChange={(event) => setForm((prev) => ({ ...prev, username: event.target.value }))}
              required
            />
            <Input
              placeholder="Email address"
              type="email"
              value={form.email}
              onChange={(event) => setForm((prev) => ({ ...prev, email: event.target.value }))}
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
              {loading ? 'Creating account...' : 'Create account'}
            </Button>
          </form>

          <p className="mt-6 text-sm text-muted">
            Already have an account?{' '}
            <Link to="/login" className="font-semibold text-neon">
              Log in
            </Link>
          </p>
        </div>

        <div className="overflow-hidden rounded-[36px] border border-border/30 bg-[radial-gradient(circle_at_top_right,rgba(var(--gold-rgb),0.18),transparent_28%),radial-gradient(circle_at_18%_22%,rgba(var(--accent-rgb),0.18),transparent_24%),linear-gradient(180deg,rgba(var(--background-soft-rgb),1),rgba(var(--background-deep-rgb),1))] p-8 md:p-10 shadow-card">
          <div className="inline-flex items-center gap-3 rounded-full border border-border/30 bg-card/55 px-4 py-2 text-sm text-muted">
            <Film className="size-4 text-neon" />
            Movie-first customer onboarding
          </div>
          <h1 className="mt-6 font-display text-5xl font-extrabold leading-tight text-foreground">
            Build your cinema identity in seconds.
          </h1>
          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {[
              ['Watchlists', 'Save the films you plan to catch this week.'],
              ['Booking history', 'Keep every ticket and confirmation in one place.'],
              ['Recommendations', 'See language, genre, and format-aware suggestions.'],
              ['Profile access', 'Manage your customer details with a lightweight profile hub.'],
            ].map(([title, copy]) => (
              <div key={title} className="rounded-[28px] border border-border/30 bg-card/45 p-5">
                <div className="inline-flex size-10 items-center justify-center rounded-2xl bg-card/70 text-gold">
                  <Sparkles className="size-4" />
                </div>
                <p className="mt-4 text-lg font-semibold text-foreground">{title}</p>
                <p className="mt-2 text-sm leading-7 text-muted">{copy}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
