import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { fetchMyBookings } from '../api/bookings'
import { currency } from '../lib/utils'
import { Card } from '../components/ui/card'

export function TicketsPage() {
  const [bookings, setBookings] = useState([])

  useEffect(() => {
    let cancelled = false

    const load = async () => {
      try {
        const data = await fetchMyBookings()
        if (!cancelled) {
          setBookings(data.items.filter((booking) => booking.status === 'active'))
        }
      } catch {
        if (!cancelled) setBookings([])
      }
    }

    load()
    const timer = window.setInterval(load, 60_000)

    return () => {
      cancelled = true
      window.clearInterval(timer)
    }
  }, [])

  return (
    <section className="section-shell py-14">
      <h1 className="font-display text-4xl font-extrabold text-foreground">My Tickets</h1>
      <p className="mt-3 text-muted">Your latest bookings, all in one polished itinerary view.</p>
      <div className="mt-8 grid gap-5">
        {!bookings.length ? (
          <Card className="p-6 text-muted">
            No active tickets right now. Completed and expired bookings remain in admin history automatically.
          </Card>
        ) : null}
        {bookings.map((booking) => (
          <Link key={booking.id} to={`/confirmation/${booking.id}`} state={booking}>
            <Card className="p-5 transition hover:border-neon/30">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <h2 className="font-display text-2xl font-bold text-foreground">{booking.movie.title}</h2>
                  <p className="mt-2 text-sm text-muted">
                    {booking.ticket.theater} • {booking.ticket.city} • {booking.ticket.showTime}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-subtle">Seats</p>
                  <p className="text-foreground">{booking.seatNumbers.join(', ')}</p>
                  <p className="mt-2 font-semibold text-gold">{currency(booking.amountPaid)}</p>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </section>
  )
}
