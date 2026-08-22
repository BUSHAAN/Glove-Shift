import { motion } from 'framer-motion'
import { Container } from './ui/Container'
import { SectionLabel } from './ui/SectionLabel'

/** Approximate MediaPipe hand landmark layout for a stylized right-hand viz */
const LANDMARKS: { id: number; x: number; y: number }[] = [
  { id: 0, x: 48, y: 88 },
  { id: 1, x: 40, y: 72 },
  { id: 2, x: 34, y: 58 },
  { id: 3, x: 30, y: 46 },
  { id: 4, x: 26, y: 34 },
  { id: 5, x: 44, y: 48 },
  { id: 6, x: 46, y: 34 },
  { id: 7, x: 48, y: 22 },
  { id: 8, x: 50, y: 12 },
  { id: 9, x: 52, y: 50 },
  { id: 10, x: 54, y: 34 },
  { id: 11, x: 56, y: 20 },
  { id: 12, x: 58, y: 8 },
  { id: 13, x: 60, y: 52 },
  { id: 14, x: 64, y: 38 },
  { id: 15, x: 66, y: 26 },
  { id: 16, x: 68, y: 16 },
  { id: 17, x: 68, y: 58 },
  { id: 18, x: 74, y: 48 },
  { id: 19, x: 78, y: 40 },
  { id: 20, x: 82, y: 32 },
]

const CONNECTIONS: [number, number][] = [
  [0, 1], [1, 2], [2, 3], [3, 4],
  [0, 5], [5, 6], [6, 7], [7, 8],
  [0, 9], [9, 10], [10, 11], [11, 12],
  [0, 13], [13, 14], [14, 15], [15, 16],
  [0, 17], [17, 18], [18, 19], [19, 20],
  [5, 9], [9, 13], [13, 17],
]

const callouts = [
  { label: '21 landmarks', detail: 'MediaPipe Hand Landmarker (Tasks API)' },
  { label: 'Geometry rules', detail: 'Thumb-out, mid-finger Y, index–pinky tilt' },
  { label: 'Deterministic', detail: 'No ML classification — landmark math only' },
  { label: 'Real-time', detail: 'Frame loop with sensitivity & smoothing' },
]

export function Vision() {
  return (
    <section className="relative overflow-hidden border-y border-gs-border bg-gs-charcoal py-24 sm:py-32">
      <div className="pointer-events-none absolute inset-0 grid-tech opacity-40" />
      <Container className="relative">
        <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <div>
            <SectionLabel accent="blue">Computer vision</SectionLabel>
            <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl">
              Behind the gesture
            </h2>
            <p className="mt-4 max-w-md text-base leading-relaxed text-gs-muted">
              MediaPipe finds the hand. Glove Shift decides the drive state from
              landmark positions — finger and tilt rules, not a trained gesture
              classifier.
            </p>

            <ul className="mt-10 space-y-4">
              {callouts.map((c, i) => (
                <motion.li
                  key={c.label}
                  initial={{ opacity: 0, x: -12 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.06 }}
                  className="flex gap-4 border-l-2 border-gs-blue/40 pl-4"
                >
                  <div>
                    <p className="font-mono text-[11px] tracking-[0.2em] text-gs-blue uppercase">
                      {c.label}
                    </p>
                    <p className="mt-1 text-sm text-gs-muted">{c.detail}</p>
                  </div>
                </motion.li>
              ))}
            </ul>
          </div>

          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="border-gradient-ring relative aspect-square max-w-md mx-auto w-full rounded-2xl bg-gs-surface p-6"
          >
            <p className="absolute top-4 left-4 font-mono text-[10px] tracking-[0.22em] text-gs-dim uppercase">
              21 landmarks
            </p>
            <svg
              viewBox="0 0 100 100"
              className="h-full w-full"
              aria-hidden="true"
            >
              {CONNECTIONS.map(([a, b]) => {
                const p1 = LANDMARKS[a]
                const p2 = LANDMARKS[b]
                return (
                  <line
                    key={`${a}-${b}`}
                    x1={p1.x}
                    y1={p1.y}
                    x2={p2.x}
                    y2={p2.y}
                    stroke="rgba(0,163,255,0.35)"
                    strokeWidth="0.6"
                  />
                )
              })}
              {LANDMARKS.map((p, i) => (
                <motion.circle
                  key={p.id}
                  cx={p.x}
                  cy={p.y}
                  r={i === 4 || i === 12 || i === 5 || i === 17 ? 1.8 : 1.2}
                  fill={
                    i === 4
                      ? '#d81e27'
                      : i === 12
                        ? '#00a3ff'
                        : i === 5 || i === 17
                          ? '#e5e5e5'
                          : '#00a3ff'
                  }
                  initial={{ opacity: 0 }}
                  whileInView={{ opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.02 * i }}
                />
              ))}
            </svg>
            <div className="absolute right-4 bottom-4 left-4 flex flex-wrap gap-2">
              <span className="rounded-sm bg-gs-black/60 px-2 py-1 font-mono text-[9px] tracking-wider text-gs-red uppercase">
                Thumb tip
              </span>
              <span className="rounded-sm bg-gs-black/60 px-2 py-1 font-mono text-[9px] tracking-wider text-gs-blue uppercase">
                Mid tip
              </span>
              <span className="rounded-sm bg-gs-black/60 px-2 py-1 font-mono text-[9px] tracking-wider text-gs-silver uppercase">
                Tilt bases
              </span>
            </div>
          </motion.div>
        </div>
      </Container>
    </section>
  )
}
