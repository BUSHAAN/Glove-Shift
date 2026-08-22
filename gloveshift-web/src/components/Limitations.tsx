import { motion } from 'framer-motion'
import { Container } from './ui/Container'
import { SectionLabel } from './ui/SectionLabel'

const limits = [
  {
    title: 'Windows only',
    body: 'Keyboard injection uses the Windows SendInput API.',
  },
  {
    title: 'WASD-compatible games',
    body: 'Games must accept keyboard W/A/S/D — or be remappable to those keys.',
  },
  {
    title: 'Environment matters',
    body: 'Lighting, camera angle, and hand pose affect recognition quality.',
  },
  {
    title: 'Single hand',
    body: 'Tracks one hand at a time. Default mode is either hand; lock left or right in the app.',
  },
]

export function Limitations() {
  return (
    <section className="relative border-y border-gs-border bg-gs-charcoal py-24 sm:py-28">
      <Container>
        <div className="max-w-2xl">
          <SectionLabel accent="red">Limitations</SectionLabel>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl">
            Current boundaries.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-gs-muted">
            Honest constraints of the project as it ships today.
          </p>
        </div>

        <div className="mt-12 grid gap-4 sm:grid-cols-2">
          {limits.map((l, i) => (
            <motion.div
              key={l.title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="rounded-lg border border-gs-border/80 bg-gs-surface/60 p-5"
            >
              <h3 className="font-display text-xl font-semibold tracking-wide text-gs-silver uppercase">
                {l.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-gs-muted">
                {l.body}
              </p>
            </motion.div>
          ))}
        </div>
      </Container>
    </section>
  )
}
