import { Link } from 'react-router-dom'

import { Button } from '../components/ui/button'

export function NotFoundPage() {
  return (
    <section className="section-shell flex min-h-[70vh] flex-col items-center justify-center text-center">
      <p className="text-xs uppercase tracking-[0.35em] text-neon/75">404</p>
      <h1 className="mt-4 font-display text-5xl font-extrabold text-foreground">This screening does not exist.</h1>
      <p className="mt-4 max-w-xl text-muted">The page you requested may have left the schedule. Let’s get you back to the spotlight.</p>
      <Link to="/" className="mt-8">
        <Button>Return Home</Button>
      </Link>
    </section>
  )
}
