import { Clock3, ShieldCheck, Ticket, UserCircle2 } from 'lucide-react'
import { useEffect, useState } from 'react'

import { fetchMyBookings } from '../api/bookings'
import { Card } from '../components/ui/card'
import { useAuth } from '../context/AuthContext'


export function ProfilePage() {
  const { user } = useAuth()
  const [bookingCount, setBookingCount] = useState(0)

  useEffect(() => {
    fetchMyBookings()
      .then((data) => setBookingCount(data.items.length))
      .catch(() => setBookingCount(0))
  }, [])

  return (
    <section className="section-shell py-14">
      <h1 className="font-display text-4xl font-extrabold text-foreground">Profile</h1>
      <p className="mt-3 text-muted">Your member identity, activity summary, and customer access status.</p>
      <div className="mt-8 grid gap-5 lg:grid-cols-[0.8fr_1.2fr]">
        <Card className="p-6">
          <div className="flex size-16 items-center justify-center rounded-3xl bg-neon/10 text-neon">
            <UserCircle2 className="size-8" />
          </div>
          <h2 className="mt-5 font-display text-3xl font-bold text-foreground">{user?.username}</h2>
          <p className="mt-2 text-muted">{user?.email}</p>
          <div className="mt-6 inline-flex rounded-full border border-border/30 bg-card/55 px-4 py-2 text-xs uppercase tracking-[0.28em] text-muted">
            role: user
          </div>
        </Card>

        <div className="grid gap-5 md:grid-cols-3">
          {[
            { icon: Ticket, label: 'Bookings', value: bookingCount },
            { icon: ShieldCheck, label: 'Session', value: 'Active' },
            { icon: Clock3, label: 'Portal', value: 'Customer' },
          ].map((item) => {
            const Icon = item.icon
            return (
              <Card key={item.label} className="p-6">
                <div className="inline-flex size-12 items-center justify-center rounded-2xl bg-card/55 text-gold">
                  <Icon className="size-5" />
                </div>
                <p className="mt-5 text-sm uppercase tracking-[0.28em] text-subtle">{item.label}</p>
                <p className="mt-3 font-display text-3xl font-bold text-foreground">{item.value}</p>
              </Card>
            )
          })}
        </div>
      </div>
    </section>
  )
}
