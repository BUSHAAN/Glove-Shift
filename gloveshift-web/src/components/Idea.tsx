import { motion } from 'framer-motion'
import { Container } from './ui/Container'
import { SectionLabel } from './ui/SectionLabel'

const alternatives = ['Keyboard', 'Controller', 'Steering wheel']

export function Idea() {
  return (
    <section className="relative border-y border-gs-border bg-gs-charcoal py-24 sm:py-32">
      <Container>
        <div className="mx-auto max-w-3xl text-center">
          <SectionLabel accent="split">The idea</SectionLabel>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl md:text-6xl">
            Your webcam becomes the controller.
          </h2>

          <p className="mt-8 text-base text-gs-muted sm:text-lg">
            Racing games normally require:
          </p>
          <div className="mt-5 flex flex-wrap justify-center gap-3">
            {alternatives.map((item) => (
              <span
                key={item}
                className="rounded-sm border border-gs-border bg-gs-surface px-4 py-2 font-mono text-xs tracking-[0.16em] text-gs-dim uppercase"
              >
                {item}
              </span>
            ))}
          </div>

          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mt-10 font-display text-3xl font-semibold tracking-tight text-gs-silver italic sm:text-4xl"
          >
            What if the webcam was enough?
          </motion.p>

          <p className="mx-auto mt-8 max-w-xl text-base leading-relaxed text-gs-muted">
            Glove Shift detects hand landmarks and translates gestures into
            standard WASD keyboard input — no game mods, plugins, or custom
            integrations.
          </p>
        </div>
      </Container>
    </section>
  )
}
