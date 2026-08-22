import { motion } from 'framer-motion'
import { Code, Download, Play } from 'lucide-react'
import { Container } from './ui/Container'
import { Button } from './ui/Button'
import { SectionLabel } from './ui/SectionLabel'
import { LINKS } from '../lib/constants'

export function Explore() {
  return (
    <section className="relative py-24 sm:py-32">
      <Container>
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mx-auto max-w-2xl text-center"
        >
          <SectionLabel accent="blue">Open source</SectionLabel>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl">
            Explore the code.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-gs-muted">
            Glove Shift is open source under the MIT License. Inspect the
            vision pipeline, gesture rules, and Windows input layer on GitHub.
          </p>
          <div className="mt-9 flex flex-wrap justify-center gap-3">
            <Button href={LINKS.github}>
              <Code className="size-3.5" />
              GitHub
            </Button>
            <Button href={LINKS.download} variant="secondary">
              <Download className="size-3.5" />
              Download
            </Button>
            <Button href={LINKS.demo} variant="ghost">
              <Play className="size-3.5" />
              Demo
            </Button>
          </div>
        </motion.div>
      </Container>
    </section>
  )
}
