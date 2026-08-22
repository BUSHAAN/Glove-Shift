import { motion } from 'framer-motion'
import { Download, Code } from 'lucide-react'
import { Container } from './ui/Container'
import { Button } from './ui/Button'
import { LINKS } from '../lib/constants'

export function DownloadCTA() {
  return (
    <section id="download" className="relative overflow-hidden py-24 sm:py-32">
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            'radial-gradient(ellipse 70% 50% at 50% 50%, rgba(216,30,39,0.12), transparent 70%)',
        }}
      />
      <Container className="relative">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="border-gradient-ring mx-auto max-w-3xl rounded-2xl bg-gs-surface px-6 py-14 text-center sm:px-12 sm:py-16"
        >
          <p className="font-mono text-[11px] tracking-[0.28em] text-gs-red uppercase">
            Try it
          </p>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl md:text-6xl">
            Ready to drive differently?
          </h2>
          <p className="mx-auto mt-5 max-w-lg text-base leading-relaxed text-gs-muted">
            Download Glove Shift and turn your webcam into a controller.
          </p>

          <div className="mt-9 flex flex-wrap justify-center gap-3">
            <Button href={LINKS.download}>
              <Download className="size-3.5" />
              Download for Windows
            </Button>
            <Button href={LINKS.github} variant="secondary">
              <Code className="size-3.5" />
              View source
            </Button>
          </div>

          <ul className="mt-10 flex flex-wrap justify-center gap-x-6 gap-y-2 font-mono text-[11px] tracking-[0.14em] text-gs-dim uppercase">
            <li>Windows 10 / 11</li>
            <li>Webcam required</li>
            <li>Either hand supported</li>
          </ul>
        </motion.div>
      </Container>
    </section>
  )
}
