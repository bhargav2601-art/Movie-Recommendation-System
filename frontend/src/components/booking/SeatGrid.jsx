import { groupSeats } from '../../lib/utils'

export function SeatGrid({ seats = [], selectedSeats = [], onSelect }) {
  const rows = groupSeats(seats)

  return (
    <div className="glass-panel rounded-[30px] p-5">
      <div className="mb-6 h-3 rounded-full bg-gradient-to-r from-neon/20 via-foreground/70 to-gold/20" />
      <p className="mb-6 text-center text-xs uppercase tracking-[0.35em] text-subtle">Screen This Way</p>
      <div className="space-y-3 overflow-x-auto">
        {Object.entries(rows).map(([row, rowSeats]) => (
          <div key={row} className="flex min-w-max items-center gap-3">
            <div className="w-6 text-sm font-semibold text-subtle">{row}</div>
            <div className="flex gap-2">
              {rowSeats.map((seat) => {
                const isSelected = selectedSeats.includes(seat.id)
                const isBooked = seat.status === 'booked'
                const isPremium = seat.type === 'premium'

                return (
                  <button
                    key={seat.id}
                    onClick={() => !isBooked && onSelect(seat.id)}
                    className={`h-10 w-10 rounded-xl border text-[11px] font-semibold transition ${
                      isBooked
                        ? 'cursor-not-allowed border-border/10 bg-card/35 text-subtle/50'
                        : isSelected
                          ? 'border-neon/50 bg-neon/20 text-foreground'
                          : isPremium
                            ? 'border-gold/35 bg-gold/10 text-gold hover:bg-gold/20'
                            : 'border-border/30 bg-card/55 text-muted hover:bg-card/80'
                    }`}
                  >
                    {seat.number}
                  </button>
                )
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
