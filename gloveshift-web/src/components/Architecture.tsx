import { motion } from 'framer-motion'
import { Container } from './ui/Container'
import { SectionLabel } from './ui/SectionLabel'

const flow = [
  'Webcam',
  'OpenCV',
  'MediaPipe Hands',
  'VirtualSteering',
  'KeyboardInput',
  'Racing Game',
]

export function Architecture() {
  return (
    <section className="relative border-y border-gs-border bg-gs-charcoal py-24 sm:py-32">
      <Container>
        <div className="max-w-2xl">
          <SectionLabel>Architecture</SectionLabel>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl">
            Modules that matter.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-gs-muted sm:text-lg">
            Real module names from the repository — not a conceptual sketch.
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mt-14 overflow-x-auto pb-2"
        >
          <div className="flex min-w-max flex-col items-stretch gap-3 md:min-w-0 md:flex-row md:flex-wrap md:items-center md:justify-center md:gap-2">
            {flow.map((node, i) => (
              <div key={node} className="flex items-center gap-2 md:contents">
                <div className="rounded-sm border border-gs-border bg-gs-surface px-4 py-3 text-center md:px-5">
                  <span className="font-mono text-[10px] tracking-[0.18em] text-gs-dim uppercase">
                    {i === 3 || i === 4 ? 'Module' : 'Stage'}
                  </span>
                  <p className="mt-1 font-display text-lg font-semibold tracking-wide text-white uppercase sm:text-xl">
                    {node}
                  </p>
                </div>
                {i < flow.length - 1 && (
                  <span
                    aria-hidden
                    className="hidden font-mono text-gs-blue md:inline md:px-1"
                  >
                    →
                  </span>
                )}
                {i < flow.length - 1 && (
                  <span
                    aria-hidden
                    className="self-center font-mono text-gs-blue md:hidden"
                  >
                    ↓
                  </span>
                )}
              </div>
            ))}
          </div>
        </motion.div>

        <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
          <div className="rounded-sm border border-gs-red/40 bg-gs-elevated px-5 py-3 text-center">
            <span className="font-mono text-[10px] tracking-[0.2em] text-gs-red uppercase">
              UI
            </span>
            <p className="mt-1 font-display text-lg font-semibold text-white uppercase">
              app.py · PyQt6
            </p>
          </div>
          <span className="font-mono text-gs-dim">connects to</span>
          <div className="rounded-sm border border-gs-blue/40 bg-gs-elevated px-5 py-3 text-center">
            <span className="font-mono text-[10px] tracking-[0.2em] text-gs-blue uppercase">
              Steering loop
            </span>
            <p className="mt-1 font-display text-lg font-semibold text-white uppercase">
              VirtualSteering
            </p>
          </div>
        </div>

        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { mod: 'app.py', role: 'PyQt6 entry — start/stop, camera, settings' },
            {
              mod: 'VirtualSteering.py',
              role: 'Frame loop, landmark rules, key mapping',
            },
            {
              mod: 'HandTrackingModule.py',
              role: 'MediaPipe wrapper for detection & landmarks',
            },
            {
              mod: 'KeyboardInput.py',
              role: 'SendInput press/release via ctypes',
            },
          ].map((m, i) => (
            <motion.div
              key={m.mod}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="rounded-lg border border-gs-border bg-gs-surface p-4"
            >
              <p className="font-mono text-xs text-gs-blue">{m.mod}</p>
              <p className="mt-2 text-sm text-gs-muted">{m.role}</p>
            </motion.div>
          ))}
        </div>
      </Container>
    </section>
  )
}
