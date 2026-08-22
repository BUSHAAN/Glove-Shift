import { motion } from 'framer-motion'
import { Container } from './ui/Container'
import { SectionLabel } from './ui/SectionLabel'

const stack = [
  { name: 'Python', layer: 'Language' },
  { name: 'OpenCV', layer: 'Vision' },
  { name: 'MediaPipe', layer: 'Vision' },
  { name: 'PyQt6', layer: 'UI' },
  { name: 'Windows SendInput', layer: 'Input' },
  { name: 'PyInstaller', layer: 'Packaging' },
  { name: 'Inno Setup', layer: 'Installer' },
]

export function Tech() {
  return (
    <section className="relative py-24 sm:py-32">
      <Container>
        <div className="max-w-2xl">
          <SectionLabel accent="split">Real project</SectionLabel>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl">
            Shipped with these tools.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-gs-muted sm:text-lg">
            The actual stack used to build and package Glove Shift — nothing
            invented for the website.
          </p>
        </div>

        <div className="mt-12 flex flex-wrap gap-3">
          {stack.map((t, i) => (
            <motion.div
              key={t.name}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="border-gradient-ring rounded-sm bg-gs-surface px-5 py-4"
            >
              <p className="font-mono text-[10px] tracking-[0.2em] text-gs-dim uppercase">
                {t.layer}
              </p>
              <p className="mt-1 font-display text-xl font-semibold tracking-wide text-white uppercase">
                {t.name}
              </p>
            </motion.div>
          ))}
        </div>
      </Container>
    </section>
  )
}
