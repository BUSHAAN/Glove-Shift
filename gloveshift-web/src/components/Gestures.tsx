import { motion } from 'framer-motion'
import { Container } from './ui/Container'
import { SectionLabel } from './ui/SectionLabel'
import gestureChart from '../assets/Gesture_Controls_New.png'

const gestures = [
  {
    key: 'W',
    title: 'Accelerate',
    detail: 'Drive forward when the middle finger extension rule fires.',
    accent: 'blue' as const,
  },
  {
    key: 'S',
    title: 'Brake / reverse',
    detail: 'Thumb-out pose maps to brake and reverse.',
    accent: 'red' as const,
  },
  {
    key: 'A',
    title: 'Steer left',
    detail: 'Index–pinky tilt crosses the left hysteresis threshold.',
    accent: 'blue' as const,
  },
  {
    key: 'D',
    title: 'Steer right',
    detail: 'Opposite tilt engages right steer.',
    accent: 'red' as const,
  },
]

export function Gestures() {
  return (
    <section id="gestures" className="relative py-24 sm:py-32">
      <Container>
        <div className="max-w-2xl">
          <SectionLabel>Hand → WASD</SectionLabel>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl">
            Gestures become keys.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-gs-muted sm:text-lg">
            Landmark geometry decides accelerate, brake, or neutral — plus
            left/right tilt for steering. Combinations like W+A work together.
          </p>
        </div>

        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {gestures.map((g, i) => (
            <motion.div
              key={g.key}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{ delay: i * 0.06, duration: 0.4 }}
              whileHover={{ y: -4 }}
              className="group border-gradient-ring rounded-lg bg-gs-surface p-5 transition-shadow hover:shadow-[0_0_40px_-12px_rgba(0,163,255,0.35)]"
            >
              <div className="flex items-baseline justify-between">
                <span
                  className={`font-display text-5xl font-extrabold ${
                    g.accent === 'blue' ? 'text-gs-blue' : 'text-gs-red'
                  }`}
                >
                  {g.key}
                </span>
                <span className="font-mono text-[10px] tracking-[0.2em] text-gs-dim uppercase">
                  Key
                </span>
              </div>
              <h3 className="mt-4 font-display text-xl font-semibold tracking-wide text-white uppercase">
                {g.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-gs-muted">
                {g.detail}
              </p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5 }}
          className="mt-14 overflow-hidden rounded-xl border border-gs-border bg-gs-elevated"
        >
          <div className="flex items-center justify-between border-b border-gs-border px-4 py-3 sm:px-6">
            <span className="font-mono text-[10px] tracking-[0.22em] text-gs-blue uppercase">
              Gesture reference
            </span>
            <span className="font-mono text-[10px] tracking-[0.18em] text-gs-dim uppercase">
              Either hand · Remappable keys
            </span>
          </div>
          <img
            src={gestureChart}
            alt="Glove Shift gesture control chart mapping hand poses to WASD"
            className="mx-auto w-full max-w-4xl p-4 sm:p-8"
          />
        </motion.div>
      </Container>
    </section>
  )
}
