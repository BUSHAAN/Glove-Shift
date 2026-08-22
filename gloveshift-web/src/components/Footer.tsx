import { Container } from './ui/Container'
import { LINKS } from '../lib/constants'
import icon from '../assets/icon.png'

export function Footer() {
  return (
    <footer className="border-t border-gs-border py-12">
      <Container className="flex flex-col gap-8 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="flex items-center gap-3">
            <img src={icon} alt="" className="size-8 rounded-full" />
            <span className="font-display text-xl font-semibold tracking-wide text-white uppercase">
              Glove <span className="text-gs-red">Shift</span>
            </span>
          </div>
          <p className="mt-3 max-w-sm text-sm leading-relaxed text-gs-dim">
            Open-source computer vision experiment for gesture-based racing.
          </p>
        </div>
        <div className="flex flex-wrap gap-6 font-mono text-[11px] tracking-[0.18em] uppercase">
          <a
            href={LINKS.github}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gs-muted transition-colors hover:text-gs-blue"
          >
            GitHub
          </a>
          <a
            href={LINKS.license}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gs-muted transition-colors hover:text-gs-silver"
          >
            License
          </a>
          <a
            href={LINKS.download}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gs-muted transition-colors hover:text-gs-red"
          >
            Download
          </a>
        </div>
      </Container>
      <Container className="mt-8 border-t border-gs-border pt-6">
        <p className="font-mono text-[10px] tracking-[0.14em] text-gs-dim uppercase">
          MIT · Bushaan Gunatilake
        </p>
      </Container>
    </footer>
  )
}
