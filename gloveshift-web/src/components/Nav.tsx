import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Menu, X, Code, Download } from 'lucide-react'
import { Container } from './ui/Container'
import { LINKS } from '../lib/constants'
import icon from '../assets/icon.png'

const navLinks = [
  { href: '#gestures', label: 'Gestures' },
  { href: '#pipeline', label: 'How it works' },
  { href: '#download', label: 'Download' },
]

export function Nav() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
      className={`fixed inset-x-0 top-0 z-50 transition-colors duration-300 ${
        scrolled
          ? 'border-b border-gs-border/80 bg-gs-black/85 backdrop-blur-md'
          : 'bg-transparent'
      }`}
    >
      <Container className="flex h-16 items-center justify-between">
        <a href="#top" className="flex items-center gap-3">
          <img src={icon} alt="" className="size-9 rounded-full" />
          <span className="font-display text-xl font-semibold tracking-wide text-white uppercase">
            Glove <span className="text-gs-red">Shift</span>
          </span>
        </a>

        <nav className="hidden items-center gap-8 md:flex">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="font-mono text-[11px] tracking-[0.2em] text-gs-muted uppercase transition-colors hover:text-white"
            >
              {link.label}
            </a>
          ))}
          <a
            href={LINKS.github}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 font-mono text-[11px] tracking-[0.2em] text-gs-muted uppercase transition-colors hover:text-gs-blue"
          >
            <Code className="size-3.5" />
            GitHub
          </a>
          <a
            href={LINKS.download}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-sm bg-gs-red px-3.5 py-2 font-mono text-[11px] tracking-[0.16em] text-white uppercase transition-colors hover:bg-gs-red-bright"
          >
            <Download className="size-3.5" />
            Download
          </a>
        </nav>

        <button
          type="button"
          className="inline-flex size-10 items-center justify-center rounded-sm border border-gs-border text-gs-silver md:hidden"
          aria-label={open ? 'Close menu' : 'Open menu'}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X className="size-5" /> : <Menu className="size-5" />}
        </button>
      </Container>

      {open && (
        <div className="border-t border-gs-border bg-gs-black/95 md:hidden">
          <Container className="flex flex-col gap-4 py-5">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="font-mono text-xs tracking-[0.2em] text-gs-silver uppercase"
                onClick={() => setOpen(false)}
              >
                {link.label}
              </a>
            ))}
            <a
              href={LINKS.github}
              target="_blank"
              rel="noopener noreferrer"
              className="font-mono text-xs tracking-[0.2em] text-gs-blue uppercase"
            >
              GitHub
            </a>
            <a
              href={LINKS.download}
              target="_blank"
              rel="noopener noreferrer"
              className="font-mono text-xs tracking-[0.2em] text-gs-red uppercase"
            >
              Download
            </a>
          </Container>
        </div>
      )}
    </motion.header>
  )
}
