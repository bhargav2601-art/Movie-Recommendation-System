import { Card } from '../ui/card'

export function AnalyticsCard({ label, value, hint }) {
  return (
    <Card className="p-5">
      <p className="text-xs uppercase tracking-[0.35em] text-subtle">{label}</p>
      <p className="mt-4 font-display text-4xl font-extrabold text-foreground">{value}</p>
      {hint ? <p className="mt-2 text-sm text-muted">{hint}</p> : null}
    </Card>
  )
}
