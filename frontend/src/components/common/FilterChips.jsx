export function FilterChips({ items = [], value, onChange }) {
  return (
    <div className="flex flex-wrap gap-2">
      {items.map((item) => {
        const active = value === item
        return (
          <button
            key={item}
            onClick={() => onChange(active ? '' : item)}
            className={`rounded-full border px-4 py-2 text-sm transition ${
              active
                ? 'pill-button pill-button-active'
                : 'pill-button'
            }`}
          >
            {item}
          </button>
        )
      })}
    </div>
  )
}
