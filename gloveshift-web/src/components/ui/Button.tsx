import type { ReactNode } from 'react'

type ButtonProps = {
  href: string
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'ghost'
  external?: boolean
  className?: string
}

export function Button({
  href,
  children,
  variant = 'primary',
  external = true,
  className = '',
}: ButtonProps) {
  const base =
    'inline-flex items-center justify-center gap-2 rounded-sm px-5 py-3 font-mono text-xs font-medium tracking-[0.16em] uppercase transition-all duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gs-blue'

  const variants = {
    primary:
      'bg-gs-red text-white hover:bg-gs-red-bright shadow-[0_0_24px_-6px_rgba(216,30,39,0.55)] hover:shadow-[0_0_32px_-4px_rgba(216,30,39,0.7)]',
    secondary:
      'border border-gs-border bg-gs-elevated text-gs-silver hover:border-gs-blue/50 hover:text-white',
    ghost:
      'border border-transparent text-gs-muted hover:border-gs-border hover:text-gs-silver',
  }

  return (
    <a
      href={href}
      className={`${base} ${variants[variant]} ${className}`}
      {...(external
        ? { target: '_blank', rel: 'noopener noreferrer' }
        : undefined)}
    >
      {children}
    </a>
  )
}
