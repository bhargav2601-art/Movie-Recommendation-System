import { motion } from 'framer-motion'

export function SectionHeader({ eyebrow, title, description, action }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between"
    >
      <div className="max-w-2xl">
        {eyebrow ? (
          <p className="mb-3 text-xs uppercase tracking-[0.35em] text-neon/80">{eyebrow}</p>
        ) : null}
        <h2 className="font-display text-3xl font-extrabold tracking-tight text-foreground md:text-4xl">
          {title}
        </h2>
        {description ? <p className="mt-3 text-sm leading-7 text-muted">{description}</p> : null}
      </div>
      {action}
    </motion.div>
  )
}
