import { AlertTriangle, Eye, EyeOff, ShieldCheck } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../hooks/useToast'


export function AdminLoginPage() {
  const navigate = useNavigate()
  const { loginAdmin } = useAuth()
  const { push } = useToast()
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({ username: 'admin', password: 'admin123', twoFactor: '' })

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    try {
      await loginAdmin({ username: form.username, password: form.password })
      push({ title: 'Admin access granted.' })
      navigate('/admin/dashboard')
    } catch (error) {
      push({ title: error?.response?.data?.detail || 'Admin sign-in failed.', tone: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="min-h-screen bg-[radial-gradient(circle_at_top_right,rgba(var(--accent-rgb),0.18),transparent_24%),linear-gradient(180deg,rgba(var(--background-rgb),0.94),rgba(var(--background-deep-rgb),1))] px-4 py-10">
      <div className="mx-auto grid min-h-[calc(100vh-5rem)] w-full max-w-7xl gap-8 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="rounded-[36px] border border-neon/15 bg-[linear-gradient(180deg,rgba(var(--background-soft-rgb),0.96),rgba(var(--background-deep-rgb),0.98))] p-8 shadow-card md:p-10">
          <div className="inline-flex items-center gap-3 rounded-full border border-neon/20 bg-neon/10 px-4 py-2 text-sm text-foreground">
            <ShieldCheck className="size-4" />
            Admin access portal
          </div>
          <h1 className="mt-6 font-display text-5xl font-extrabold leading-tight text-foreground">
            Secure cinema operations control.
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-8 text-muted">
            This environment is reserved for management operations, revenue oversight, scheduling, and analytics visibility.
          </p>
          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {[
              ['Access badge', 'Enterprise management portal with role-restricted entry.'],
              ['Login activity', 'Last privileged sign-in: Today, 14:12 IST from secure device.'],
              ['Security warning', 'Unauthorized access attempts are logged and monitored.'],
              ['2FA placeholder', 'Second-factor challenge UI reserved for production hardening.'],
            ].map(([title, copy]) => (
              <div key={title} className="rounded-[28px] border border-border/25 bg-card/45 p-5">
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-neon/85">{title}</p>
                <p className="mt-3 text-sm leading-7 text-muted">{copy}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-panel rounded-[36px] p-7 md:p-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.35em] text-neon/80">Management Login</p>
              <h2 className="mt-3 font-display text-4xl font-extrabold text-foreground">Admin sign in</h2>
            </div>
            <span className="rounded-full border border-neon/25 bg-neon/10 px-4 py-2 text-xs uppercase tracking-[0.28em] text-foreground">
              role: admin
            </span>
          </div>

          <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
            <Input
              placeholder="Admin email or username"
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
            <Input
              placeholder="2FA code placeholder"
              value={form.twoFactor}
              onChange={(event) => setForm((prev) => ({ ...prev, twoFactor: event.target.value }))}
            />
            <div className="rounded-2xl border border-amber-500/25 bg-amber-500/10 px-4 py-4 text-sm text-foreground">
              <div className="flex gap-3">
                <AlertTriangle className="mt-0.5 size-4 shrink-0" />
                <p>Restricted management access. Continue only if you are authorized to view commercial cinema data.</p>
              </div>
            </div>
            <Button className="w-full" disabled={loading}>
              {loading ? 'Verifying admin access...' : 'Access dashboard'}
            </Button>
          </form>
        </div>
      </div>
    </section>
  )
}
