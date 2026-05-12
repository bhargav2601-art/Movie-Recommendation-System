import { Link } from 'react-router-dom'


export function Footer() {
  return (
    <footer className="border-t border-border/30 bg-card/60 backdrop-blur-xl">
      <div className="section-shell flex flex-col gap-3 py-6 text-sm text-muted md:flex-row md:items-center md:justify-between">
        <p>CineVerse customer experience portal.</p>
        <Link to="/admin/login" className="text-subtle transition hover:text-foreground">
          Management access
        </Link>
      </div>
    </footer>
  )
}
