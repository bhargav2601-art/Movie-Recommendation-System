import { CalendarClock, CreditCard, MapPin, Popcorn, Ticket } from 'lucide-react'

import { currency } from '../../lib/utils'
import { Button } from '../ui/button'
import { Card } from '../ui/card'

export function BookingSummary({
  seatMap,
  selectedSeats,
  total,
  onConfirm,
  loading,
  selectedCombo,
  onSelectCombo,
  selectedCoupon,
  onSelectCoupon,
  selectedPayment,
  onSelectPayment,
  timerLabel,
}) {
  const show = seatMap?.show
  const combos = seatMap?.foodCombos ?? []
  const coupons = seatMap?.coupons ?? []
  const payments = seatMap?.paymentMethods ?? []

  return (
    <Card className="sticky top-28 p-5">
      <p className="text-xs uppercase tracking-[0.35em] text-subtle">Booking Summary</p>
      <h3 className="mt-3 font-display text-2xl font-bold text-foreground">{show?.movieTitle}</h3>
      <div className="mt-5 space-y-3 text-sm text-muted">
        <div className="flex items-center gap-3">
          <MapPin className="size-4 text-neon" />
          <span>
            {show?.theater?.name}, {show?.theater?.city}
          </span>
        </div>
        <div className="flex items-center gap-3">
          <CalendarClock className="size-4 text-gold" />
          <span>{show?.showTime}</span>
        </div>
        <div className="flex items-center gap-3">
          <Ticket className="size-4 text-foreground" />
          <span>{selectedSeats.length ? selectedSeats.join(', ') : 'Select your seats'}</span>
        </div>
      </div>
      <div className="my-5 border-t border-border/30" />
      <div className="flex items-center justify-between text-sm">
        <span className="text-muted">Tickets</span>
        <span className="text-foreground">{selectedSeats.length}</span>
      </div>
      <div className="mt-3 flex items-center justify-between text-sm">
        <span className="text-muted">Amount</span>
        <span className="font-semibold text-foreground">{currency(total)}</span>
      </div>
      <div className="mt-6 rounded-2xl border border-neon/20 bg-neon/10 px-4 py-3 text-sm text-foreground/85">
        Complete payment in <span className="font-semibold text-foreground">{timerLabel}</span>
      </div>

      <div className="mt-6">
        <p className="text-xs uppercase tracking-[0.35em] text-subtle">Food Combos</p>
        <div className="mt-3 space-y-2">
          {combos.map((combo) => (
            <button
              key={combo.id}
              onClick={() => onSelectCombo(selectedCombo?.id === combo.id ? null : combo)}
              className={`w-full rounded-2xl border px-4 py-3 text-left text-sm transition ${
                selectedCombo?.id === combo.id
                  ? 'border-gold/30 bg-gold/10 text-foreground'
                  : 'border-border/30 bg-card/55 text-muted'
              }`}
            >
              <div className="flex items-center justify-between gap-3">
                <span className="inline-flex items-center gap-2 font-semibold">
                  <Popcorn className="size-4 text-gold" />
                  {combo.name}
                </span>
                <span>{currency(combo.price)}</span>
              </div>
              <p className="mt-2 text-xs text-subtle">{combo.items.join(' • ')}</p>
            </button>
          ))}
        </div>
      </div>

      <div className="mt-6">
        <p className="text-xs uppercase tracking-[0.35em] text-subtle">Coupons</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {coupons.map((coupon) => (
            <button
              key={coupon.code}
              onClick={() => onSelectCoupon(selectedCoupon?.code === coupon.code ? null : coupon)}
              className={`rounded-full border px-4 py-2 text-xs transition ${
                selectedCoupon?.code === coupon.code
                  ? 'border-neon/40 bg-neon/15 text-foreground'
                  : 'border-border/30 bg-card/55 text-muted'
              }`}
            >
              {coupon.code}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-6">
        <p className="text-xs uppercase tracking-[0.35em] text-subtle">Payment Method</p>
        <div className="mt-3 space-y-2">
          {payments.map((payment) => (
            <button
              key={payment.name}
              onClick={() => onSelectPayment(payment.name)}
              className={`w-full rounded-2xl border px-4 py-3 text-left text-sm transition ${
                selectedPayment === payment.name
                  ? 'border-neon/40 bg-neon/10 text-foreground'
                  : 'border-border/30 bg-card/55 text-muted'
              }`}
            >
              <div className="flex items-center gap-2 font-semibold">
                <CreditCard className="size-4 text-neon" />
                {payment.name}
              </div>
              <p className="mt-2 text-xs text-subtle">{payment.description}</p>
            </button>
          ))}
        </div>
      </div>
      <Button onClick={onConfirm} disabled={!selectedSeats.length || loading} className="mt-6 w-full">
        {loading ? 'Confirming...' : 'Proceed to Payment'}
      </Button>
    </Card>
  )
}
