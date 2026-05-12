import { useEffect, useMemo, useState } from 'react'
import { Activity, Flame, ShieldCheck, Users } from 'lucide-react'
import { BarChart, Bar, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis, AreaChart, Area } from 'recharts'

import {
  createAdminMovie,
  createAdminScreen,
  createAdminShow,
  createAdminTheater,
  fetchAdminAnalytics,
  fetchAdminCatalog,
} from '../api/admin'
import { AdminSidebar } from '../components/admin/AdminSidebar'
import { AnalyticsCard } from '../components/admin/AnalyticsCard'
import { Button } from '../components/ui/button'
import { Card } from '../components/ui/card'
import { Input } from '../components/ui/input'
import { useTheme } from '../context/ThemeProvider'
import { useToast } from '../hooks/useToast'
import { currency } from '../lib/utils'

function DashboardForm({ title, fields, onSubmit, loading }) {
  const [state, setState] = useState({})

  return (
    <Card className="p-5">
      <h3 className="font-display text-2xl font-bold text-foreground">{title}</h3>
      <form
        className="mt-5 grid gap-3"
        onSubmit={async (event) => {
          event.preventDefault()
          await onSubmit(state)
          setState({})
        }}
      >
        {fields.map((field) =>
          field.type === 'select' ? (
            <select
              key={field.name}
              value={state[field.name] ?? ''}
              onChange={(event) => setState((prev) => ({ ...prev, [field.name]: event.target.value }))}
              className="select-theme"
              required={field.required}
            >
              <option value="">{field.placeholder}</option>
              {field.options.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          ) : (
            <Input
              key={field.name}
              placeholder={field.placeholder}
              type={field.type || 'text'}
              value={state[field.name] ?? ''}
              onChange={(event) => setState((prev) => ({ ...prev, [field.name]: event.target.value }))}
              required={field.required}
            />
          ),
        )}
        <Button disabled={loading}>{loading ? 'Saving...' : 'Submit'}</Button>
      </form>
    </Card>
  )
}

export function AdminDashboardPage() {
  const [analytics, setAnalytics] = useState(null)
  const [catalog, setCatalog] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(false)
  const { push } = useToast()
  const { resolvedTheme } = useTheme()
  const isDark = resolvedTheme === 'dark'
  const chartAxisColor = isDark ? '#94a3b8' : '#64748b'
  const chartGridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(100,116,139,0.14)'
  const chartTooltipStyle = {
    backgroundColor: isDark ? 'rgba(15, 23, 42, 0.94)' : 'rgba(255, 255, 255, 0.96)',
    borderColor: isDark ? 'rgba(255,255,255,0.12)' : 'rgba(148, 163, 184, 0.28)',
    borderRadius: '18px',
    color: isDark ? '#f8fafc' : '#111827',
    boxShadow: isDark
      ? '0 18px 50px rgba(2, 6, 23, 0.36)'
      : '0 18px 50px rgba(148, 163, 184, 0.22)',
  }

  const load = async () => {
    const [analyticsData, catalogData] = await Promise.all([fetchAdminAnalytics(), fetchAdminCatalog()])
    setAnalytics(analyticsData)
    setCatalog(catalogData)
  }

  useEffect(() => {
    void load()
  }, [])

  const screenOptions = useMemo(
    () =>
      (catalog?.screens ?? []).map((screen) => ({
        value: screen.id,
        label: `${screen.name} (#${screen.id})`,
      })),
    [catalog],
  )

  const theaterOptions = useMemo(
    () =>
      (catalog?.theaters ?? []).map((theater) => ({
        value: theater.id,
        label: `${theater.name} • ${theater.city}`,
      })),
    [catalog],
  )

  const runCreate = async (action, payload, transform = (value) => value) => {
    setLoading(true)
    try {
      await action(transform(payload))
      push({ title: 'Admin action completed successfully.' })
      await load()
    } catch (error) {
      push({ title: error?.response?.data?.detail || 'Admin action failed.', tone: 'error' })
    } finally {
      setLoading(false)
    }
  }

  if (!analytics || !catalog) {
    return <section className="section-shell py-20 text-muted">Loading dashboard...</section>
  }

  return (
    <section className="min-h-screen bg-[radial-gradient(circle_at_top_right,rgba(var(--accent-rgb),0.14),transparent_20%),linear-gradient(180deg,rgba(var(--background-rgb),0.8),rgba(var(--background-deep-rgb),0.96))] py-10">
      <div className="section-shell mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-neon/75">Admin Dashboard</p>
          <h1 className="mt-3 font-display text-4xl font-extrabold text-foreground">Cinema operations command</h1>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-muted">
            Revenue analytics, movie management, show scheduling, and user activity monitoring in one enterprise control surface.
          </p>
        </div>
        <div className="rounded-[24px] border border-neon/20 bg-neon/10 px-5 py-4 text-sm text-foreground">
          <div className="flex items-center gap-3">
            <ShieldCheck className="size-4" />
            <div>
              <p className="font-semibold">Privileged session active</p>
              <p className="text-xs uppercase tracking-[0.25em] text-muted">role: admin</p>
            </div>
          </div>
        </div>
      </div>
      <div className="section-shell">
      <div className="grid gap-6 xl:grid-cols-[0.22fr_1fr]">
        <AdminSidebar active={activeTab} onSelect={setActiveTab} />
        <div className="min-w-0 space-y-6">
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            <AnalyticsCard label="Revenue" value={currency(analytics.overview.revenue)} hint="All-time gross ticket sales" />
            <AnalyticsCard label="Active Movies" value={analytics.overview.activeMovies} hint={`Top seller: ${analytics.topSellingMovie ?? 'N/A'}`} />
            <AnalyticsCard label="Total Users" value={analytics.overview.total_users} hint={`${analytics.overview.total_bookings} bookings processed`} />
            <AnalyticsCard label="Tickets Sold" value={analytics.overview.total_tickets} hint={`${analytics.overview.shows} live show slots`} />
          </div>

          <div className="grid gap-5 md:grid-cols-3">
            <Card className="p-5">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-neon/10 p-3 text-neon"><Users className="size-5" /></div>
                <div>
                  <p className="text-xs uppercase tracking-[0.35em] text-subtle">Live Users</p>
                  <p className="mt-1 font-display text-3xl font-extrabold text-foreground">{analytics.realTimeStats.liveUsers}</p>
                </div>
              </div>
            </Card>
            <Card className="p-5">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-gold/10 p-3 text-gold"><Flame className="size-5" /></div>
                <div>
                  <p className="text-xs uppercase tracking-[0.35em] text-subtle">Live Bookings</p>
                  <p className="mt-1 font-display text-3xl font-extrabold text-foreground">{analytics.realTimeStats.liveBookings}</p>
                </div>
              </div>
            </Card>
            <Card className="p-5">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-card/70 p-3 text-foreground"><Activity className="size-5" /></div>
                <div>
                  <p className="text-xs uppercase tracking-[0.35em] text-subtle">Occupancy</p>
                  <p className="mt-1 font-display text-3xl font-extrabold text-foreground">{analytics.realTimeStats.occupancyRate}%</p>
                </div>
              </div>
            </Card>
          </div>

          <div className="grid gap-6 lg:grid-cols-[1fr_0.8fr]">
            <Card className="min-w-0 p-5">
              <h2 className="font-display text-2xl font-bold text-foreground">Revenue by Movie</h2>
              <div className="mt-6 h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={analytics.revenueByMovie}>
                    <CartesianGrid stroke={chartGridColor} vertical={false} />
                    <XAxis dataKey="movie" tick={{ fill: chartAxisColor, fontSize: 12 }} />
                    <YAxis tick={{ fill: chartAxisColor, fontSize: 12 }} />
                    <Tooltip contentStyle={chartTooltipStyle} />
                    <Bar dataKey="revenue" fill="#69e6ff" radius={[12, 12, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>

            <Card className="min-w-0 p-5">
              <h2 className="font-display text-2xl font-bold text-foreground">City Performance</h2>
              <div className="mt-6 h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={analytics.cityPerformance}>
                    <defs>
                      <linearGradient id="cityFill" x1="0" x2="0" y1="0" y2="1">
                        <stop offset="5%" stopColor="#f6c469" stopOpacity={0.85} />
                        <stop offset="95%" stopColor="#f6c469" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid stroke={chartGridColor} vertical={false} />
                    <XAxis dataKey="city" tick={{ fill: chartAxisColor, fontSize: 12 }} />
                    <YAxis tick={{ fill: chartAxisColor, fontSize: 12 }} />
                    <Tooltip contentStyle={chartTooltipStyle} />
                    <Area type="monotone" dataKey="shows" stroke="#f6c469" fill="url(#cityFill)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </div>

          <div className="grid gap-6 lg:grid-cols-[1fr_0.8fr]">
            <Card className="min-w-0 p-5">
              <h2 className="font-display text-2xl font-bold text-foreground">Occupancy by Movie</h2>
              <div className="mt-6 h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={analytics.occupancyByMovie}>
                    <CartesianGrid stroke={chartGridColor} vertical={false} />
                    <XAxis dataKey="movie" tick={{ fill: chartAxisColor, fontSize: 12 }} />
                    <YAxis tick={{ fill: chartAxisColor, fontSize: 12 }} />
                    <Tooltip contentStyle={chartTooltipStyle} />
                    <Bar dataKey="occupancy" fill="#f6c469" radius={[12, 12, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>

            <Card className="p-5">
              <h2 className="font-display text-2xl font-bold text-foreground">User Activity Heatmap</h2>
              <div className="mt-6 grid grid-cols-5 gap-2">
                {analytics.bookingHeatmap.map((slot) => (
                  <div
                    key={`${slot.day}-${slot.hour}`}
                    className="rounded-2xl border border-border/30 p-3 text-center"
                    style={{ background: `rgba(105,230,255,${Math.max(0.08, slot.value / 120)})` }}
                  >
                    <p className="text-[11px] uppercase tracking-[0.25em] text-subtle">{slot.day}</p>
                    <p className="mt-2 text-sm font-semibold text-foreground">{slot.hour}</p>
                    <p className="mt-1 text-xs text-muted">{slot.value}%</p>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          <div className="grid gap-6 xl:grid-cols-3">
            <DashboardForm
              title="Add Movie"
              loading={loading}
              fields={[
                { name: 'name', placeholder: 'Movie title', required: true },
                { name: 'language', placeholder: 'Languages (comma separated)', required: true },
                { name: 'release_date', placeholder: 'Release date YYYY-MM-DD', required: true },
              ]}
              onSubmit={(payload) => runCreate(createAdminMovie, payload)}
            />
            <DashboardForm
              title="Add Theater"
              loading={loading}
              fields={[
                { name: 'name', placeholder: 'Theater name', required: true },
                { name: 'city', placeholder: 'City', required: true },
              ]}
              onSubmit={(payload) => runCreate(createAdminTheater, payload)}
            />
            <DashboardForm
              title="Add Screen"
              loading={loading}
              fields={[
                { name: 'theater_id', placeholder: 'Select theater', type: 'select', options: theaterOptions, required: true },
                { name: 'screen_name', placeholder: 'Screen name', required: true },
                { name: 'total_seats', placeholder: 'Total seats', type: 'number', required: true },
                { name: 'seat_rows', placeholder: 'Rows', type: 'number', required: true },
                { name: 'seats_per_row', placeholder: 'Seats per row', type: 'number', required: true },
              ]}
              onSubmit={(payload) =>
                runCreate(createAdminScreen, payload, (value) => ({
                  ...value,
                  theater_id: Number(value.theater_id),
                  total_seats: Number(value.total_seats),
                  seat_rows: Number(value.seat_rows),
                  seats_per_row: Number(value.seats_per_row),
                }))
              }
            />
          </div>

          <DashboardForm
            title="Schedule Show"
            loading={loading}
            fields={[
              { name: 'movie_id', placeholder: 'Movie ID', type: 'number', required: true },
              { name: 'screen_id', placeholder: 'Select screen', type: 'select', options: screenOptions, required: true },
              { name: 'show_time', placeholder: 'Show time e.g. 19:30', required: true },
              { name: 'ticket_price', placeholder: 'Ticket price', type: 'number', required: true },
            ]}
            onSubmit={(payload) =>
              runCreate(createAdminShow, payload, (value) => ({
                ...value,
                movie_id: Number(value.movie_id),
                screen_id: Number(value.screen_id),
                ticket_price: Number(value.ticket_price),
              }))
            }
          />

          <Card className="p-5">
            <h2 className="font-display text-2xl font-bold text-foreground">Recent Booking Activity</h2>
            <div className="mt-5 overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className="text-subtle">
                  <tr>
                    <th className="pb-3 font-medium">Movie</th>
                    <th className="pb-3 font-medium">Theater</th>
                    <th className="pb-3 font-medium">Seats</th>
                    <th className="pb-3 font-medium">Amount</th>
                  </tr>
                </thead>
                <tbody className="text-muted">
                  {analytics.recentBookings.map((booking) => (
                    <tr key={booking.id} className="border-t border-border/20">
                      <td className="py-3">{booking.movie.title}</td>
                      <td className="py-3">{booking.ticket.theater}</td>
                      <td className="py-3">{booking.seatNumbers.join(', ')}</td>
                      <td className="py-3">{currency(booking.amountPaid)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      </div>
      </div>
    </section>
  )
}
