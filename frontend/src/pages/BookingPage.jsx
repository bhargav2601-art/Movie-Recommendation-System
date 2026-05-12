import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { createBooking } from '../api/bookings'
import { fetchSeatMap } from '../api/movies'
import { BookingSummary } from '../components/booking/BookingSummary'
import { SeatGrid } from '../components/booking/SeatGrid'
import { SeatViewPreview } from '../components/booking/SeatViewPreview'
import { useToast } from '../hooks/useToast'

export function BookingPage() {
  const { showId } = useParams()
  const navigate = useNavigate()
  const { push } = useToast()
  const [seatMap, setSeatMap] = useState(null)
  const [selectedSeats, setSelectedSeats] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedCombo, setSelectedCombo] = useState(null)
  const [selectedCoupon, setSelectedCoupon] = useState(null)
  const [selectedPayment, setSelectedPayment] = useState('UPI')
  const [secondsLeft, setSecondsLeft] = useState(600)

  useEffect(() => {
    let cancelled = false

    const loadSeatMap = async () => {
      const data = await fetchSeatMap(showId)
      if (!cancelled) {
        setSeatMap(data)
        setSelectedSeats((current) => current.filter((seatId) => data.seats.some((seat) => seat.id === seatId && seat.status === 'available')))
      }
    }

    loadSeatMap()
    const timer = window.setInterval(loadSeatMap, 30_000)

    return () => {
      cancelled = true
      window.clearInterval(timer)
    }
  }, [showId])

  useEffect(() => {
    if (!seatMap) return undefined
    setSecondsLeft(seatMap.countdownSeconds)
    const timer = window.setInterval(() => {
      setSecondsLeft((value) => (value > 0 ? value - 1 : 0))
    }, 1000)
    return () => window.clearInterval(timer)
  }, [seatMap])

  const handleSelect = (seatId) => {
    setSelectedSeats((current) => {
      if (current.includes(seatId)) return current.filter((item) => item !== seatId)
      if (current.length >= 4) {
        push({ title: 'You can select a maximum of 4 seats.', tone: 'error' })
        return current
      }
      return [...current, seatId]
    })
  }

  const total = useMemo(() => {
    if (!seatMap) return 0
    let subtotal = selectedSeats.reduce((sum, seatId) => {
      const seat = seatMap.seats.find((item) => item.id === seatId)
      const premiumExtra = seat?.type === 'premium' ? seatMap.pricing.premiumSurcharge : 0
      return sum + seatMap.pricing.basePrice + premiumExtra
    }, 0)
    if (selectedCombo) subtotal += selectedCombo.price
    if (selectedCoupon?.discount) subtotal = Math.max(0, subtotal - selectedCoupon.discount)
    if (selectedCoupon?.discountPercent) subtotal = subtotal * (1 - selectedCoupon.discountPercent / 100)
    return Math.round(subtotal)
  }, [seatMap, selectedSeats, selectedCombo, selectedCoupon])

  const timerLabel = useMemo(() => {
    const minutes = String(Math.floor(secondsLeft / 60)).padStart(2, '0')
    const seconds = String(secondsLeft % 60).padStart(2, '0')
    return `${minutes}:${seconds}`
  }, [secondsLeft])

  const handleConfirm = async () => {
    setLoading(true)
    try {
      const booking = await createBooking({ show_id: Number(showId), seat_numbers: selectedSeats })
      push({ title: 'Booking confirmed successfully.' })
      navigate(`/confirmation/${booking.id}`, { state: booking })
    } catch (error) {
      push({
        title: error?.response?.data?.detail || 'Could not complete booking.',
        tone: 'error',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="section-shell py-14">
      <div className="mb-8">
        <p className="text-xs uppercase tracking-[0.35em] text-neon/80">Seat Selection</p>
        <h1 className="mt-3 font-display text-4xl font-extrabold text-foreground md:text-5xl">
          Pick your perfect seats
        </h1>
        <p className="mt-3 text-muted">
          Premium rows, real-time availability, and a clean mobile-friendly booking summary.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_0.36fr]">
        <div className="space-y-6">
          <SeatGrid seats={seatMap?.seats ?? []} selectedSeats={selectedSeats} onSelect={handleSelect} />
          <SeatViewPreview seatMap={seatMap} selectedSeats={selectedSeats} />
        </div>
        <BookingSummary
          seatMap={seatMap}
          selectedSeats={selectedSeats}
          total={total}
          onConfirm={handleConfirm}
          loading={loading}
          selectedCombo={selectedCombo}
          onSelectCombo={setSelectedCombo}
          selectedCoupon={selectedCoupon}
          onSelectCoupon={setSelectedCoupon}
          selectedPayment={selectedPayment}
          onSelectPayment={setSelectedPayment}
          timerLabel={timerLabel}
        />
      </div>
    </section>
  )
}
