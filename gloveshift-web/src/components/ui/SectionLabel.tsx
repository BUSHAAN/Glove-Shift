type SectionLabelProps = {
  children: string
  accent?: 'blue' | 'red' | 'split'
}

export function SectionLabel({ children, accent = 'blue' }: SectionLabelProps) {
  const color =
    accent === 'red'
      ? 'text-gs-red'
      : accent === 'split'
        ? 'text-gradient-blue-red'
        : 'text-gs-blue'

  return (
    <p
      className={`font-mono text-[11px] font-medium tracking-[0.28em] uppercase ${color}`}
    >
      {children}
    </p>
  )
}
