import { CheckCircle2, Download, MapPin, Share2, Ticket } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

import { fetchMyBookings } from '../api/bookings'
import { currency } from '../lib/utils'
import { Button } from '../components/ui/button'
import { Card } from '../components/ui/card'

export function ConfirmationPage() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const [booking, setBooking] = useState(state ?? null)

  useEffect(() => {
    if (booking) return
    fetchMyBookings().then((data) => {
      if (data.items.length) setBooking(data.items[0])
    })
  }, [booking])

  if (!booking) {
    return <section className="section-shell py-20 text-muted">Loading your ticket...</section>
  }

  return (
    <section className="section-shell py-14">
      <div className="mx-auto max-w-4xl">
        <div className="mb-10 text-center">
          <div className="mx-auto inline-flex size-16 items-center justify-center rounded-full bg-neon/15 text-neon">
            <CheckCircle2 className="size-8" />
          </div>
          <h1 className="mt-6 font-display text-5xl font-extrabold text-foreground">Booking Confirmed</h1>
          <p className="mt-4 text-muted">Your premium movie ticket is ready to share, save, and show at the gate.</p>
        </div>

        <Card className="overflow-hidden">
          <div className="grid md:grid-cols-[1.1fr_0.5fr]">
            <div className="p-8">
              <p className="text-xs uppercase tracking-[0.35em] text-subtle">CineVerse Ticket</p>
              <h2 className="mt-4 font-display text-4xl font-extrabold text-foreground">{booking.movie.title}</h2>
              <div className="mt-6 grid gap-4 text-sm text-muted sm:grid-cols-2">
                <div>
                  <p className="text-subtle">Seats</p>
                  <p className="mt-1 text-lg font-semibold text-foreground">{booking.seatNumbers.join(', ')}</p>
                </div>
                <div>
                  <p className="text-subtle">Amount</p>
                  <p className="mt-1 text-lg font-semibold text-foreground">{currency(booking.amountPaid)}</p>
                </div>
                <div className="sm:col-span-2">
                  <p className="text-subtle">Venue</p>
                  <p className="mt-1 inline-flex items-center gap-2 text-foreground">
                    <MapPin className="size-4 text-neon" />
                    {booking.ticket.theater}, {booking.ticket.city}
                  </p>
                </div>
              </div>
            </div>
            <div className="border-l border-dashed border-border/30 bg-card/35 p-8">
              <div className="flex h-full flex-col justify-between">
                <div className="rounded-[28px] border border-border/30 bg-background-soft/85 p-6 text-center">
                  <Ticket className="mx-auto size-10 text-gold" />
                  <div className="mt-4 grid grid-cols-6 gap-1">
                    {Array.from({ length: 36 }).map((_, index) => (
                      <div key={index} className="h-3 rounded-sm bg-foreground/15" />
                    ))}
                  </div>
                </div>
                <div className="mt-6 space-y-3">
                  <Button className="w-full">
                    <Download className="mr-2 size-4" />
                    Download Ticket
                  </Button>
                  <Button variant="secondary" className="w-full" onClick={() => navigate('/')}>
                    <Share2 className="mr-2 size-4" />
                    Share Ticket
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </section>
  )
}
