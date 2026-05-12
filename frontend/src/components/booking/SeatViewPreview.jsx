import { Armchair } from 'lucide-react'
import { useState } from 'react'

import { Card } from '../ui/card'

function describeHorizontalPosition(number, seatsPerRow) {
  const center = (seatsPerRow + 1) / 2
  const offset = number - center
  if (Math.abs(offset) <= 1) return 'Center aligned'
  if (offset < 0) return 'Left side angle'
  return 'Right side angle'
}

function describeDepth(rowIndex, totalRows) {
  const progress = totalRows <= 1 ? 0 : rowIndex / (totalRows - 1)
  if (progress < 0.25) return 'Front rows: closest to the screen'
  if (progress < 0.65) return 'Middle rows: balanced cinematic view'
  return 'Back rows: widest field of view'
}

export function SeatViewPreview({ seatMap, selectedSeats }) {
  const focusSeatId = selectedSeats[selectedSeats.length - 1]
  const [mode, setMode] = useState('Normal')
  const [brightness, setBrightness] = useState(88)

  if (!seatMap || !focusSeatId) {
    return (
      <Card className="p-5">
        <p className="text-xs uppercase tracking-[0.35em] text-subtle">3D Seat View</p>
        <div className="mt-5 rounded-[28px] border border-border/30 bg-card/45 p-6 text-sm text-muted">
          Select a seat to preview how your view lines up with the screen.
        </div>
      </Card>
    )
  }

  const seat = seatMap.seats.find((item) => item.id === focusSeatId)
  const rowIndex = seat.row.charCodeAt(0) - 65
  const seatDepth = ((rowIndex + 1) / seatMap.show.screen.seatRows) * 100
  const seatOffset = (seat.number / seatMap.show.screen.seatsPerRow) * 100
  const perspective = (() => {
    const center = (seatMap.show.screen.seatsPerRow + 1) / 2
    const horizontalOffset = seat.number - center
    const normalizedOffset = horizontalOffset / center
    const depthRatio = rowIndex / Math.max(1, seatMap.show.screen.seatRows - 1)
    const rotateY = normalizedOffset * 16
    const scaleX = mode === 'Wide' ? 1.12 : mode === 'IMAX' ? 1.25 : 1
    const scaleY = mode === 'IMAX' ? 1.18 : depthRatio < 0.25 ? 1.12 : 1
    const blur = depthRatio > 0.7 ? 0 : depthRatio < 0.2 ? 1.5 : 0.4
    return { rotateY, scaleX, scaleY, blur }
  })()

  return (
    <Card className="overflow-hidden p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-subtle">3D Seat View</p>
          <h3 className="mt-2 font-display text-2xl font-bold text-foreground">{focusSeatId}</h3>
        </div>
        <div className="rounded-full border border-neon/20 bg-neon/10 px-3 py-1 text-xs text-neon">
          Live perspective
        </div>
      </div>

      <div className="mt-5 flex flex-wrap gap-2">
        {seatMap.experienceModes.map((item) => (
          <button
            key={item}
            onClick={() => setMode(item)}
            className={`rounded-full border px-4 py-2 text-xs transition ${
              mode === item ? 'border-neon/40 bg-neon/10 text-foreground' : 'border-border/30 bg-card/55 text-muted'
            }`}
          >
            {item}
          </button>
        ))}
        <div className="ml-auto flex items-center gap-3 rounded-full border border-border/30 bg-card/55 px-4 py-2 text-xs text-muted">
          Brightness
          <input type="range" min="55" max="100" value={brightness} onChange={(event) => setBrightness(event.target.value)} />
        </div>
      </div>

      <div className="mt-5 rounded-[30px] border border-border/30 bg-[radial-gradient(circle_at_top,_rgba(var(--accent-rgb),0.14),_transparent_30%),linear-gradient(180deg,rgba(var(--background-soft-rgb),0.98)_0%,rgba(var(--background-deep-rgb),0.96)_100%)] p-4">
        <div
          className="mx-auto w-[70%] rounded-full bg-gradient-to-r from-foreground/20 via-neon/80 to-foreground/20 px-4 py-2 text-center text-[11px] uppercase tracking-[0.45em] text-ink"
          style={{
            transform: `perspective(1000px) rotateX(${10 + rowIndex * 0.25}deg) rotateY(${perspective.rotateY}deg) scale(${perspective.scaleX}, ${perspective.scaleY})`,
            filter: `brightness(${brightness}%) blur(${perspective.blur}px)`,
          }}
        >
          Screen
        </div>
        <div className="relative mt-8 h-72 overflow-hidden rounded-[26px] border border-border/20 bg-gradient-to-b from-card/20 to-transparent [perspective:900px]">
          <div className="absolute inset-x-6 bottom-4 top-10 rounded-[22px] border border-border/15 bg-[linear-gradient(180deg,rgba(255,255,255,0.06),rgba(255,255,255,0.01))] [transform:rotateX(64deg)]" />
          <div
            className="absolute z-10 -translate-x-1/2 -translate-y-1/2"
            style={{ left: `${seatOffset}%`, top: `${seatDepth}%` }}
          >
            <div className="relative flex flex-col items-center">
              <div className="absolute -top-8 rounded-full bg-overlay/60 px-2 py-1 text-[10px] font-semibold text-foreground">
                {focusSeatId}
              </div>
              <div className="rounded-2xl border border-gold/30 bg-gold/15 p-3 shadow-[0_0_30px_rgba(246,196,105,0.15)]">
                <Armchair className="size-6 text-gold" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-5 grid gap-3 text-sm text-muted md:grid-cols-2">
        <div className="rounded-2xl border border-border/30 bg-card/55 p-4">
          <p className="text-subtle">Horizontal angle</p>
          <p className="mt-2 font-semibold text-foreground">{describeHorizontalPosition(seat.number, seatMap.show.screen.seatsPerRow)}</p>
        </div>
        <div className="rounded-2xl border border-border/30 bg-card/55 p-4">
          <p className="text-subtle">Distance from screen</p>
          <p className="mt-2 font-semibold text-foreground">{describeDepth(rowIndex, seatMap.show.screen.seatRows)}</p>
        </div>
        <div className="rounded-2xl border border-border/30 bg-card/55 p-4">
          <p className="text-subtle">Premium perks</p>
          <p className="mt-2 font-semibold text-foreground">{seat.type === 'premium' ? 'Recliner experience • Dolby Atmos' : 'Classic auditorium view'}</p>
        </div>
        <div className="rounded-2xl border border-border/30 bg-card/55 p-4">
          <p className="text-subtle">Mode</p>
          <p className="mt-2 font-semibold text-foreground">{mode} • {seatMap.show.screen.formats.join(', ')}</p>
        </div>
      </div>
    </Card>
  )
}
