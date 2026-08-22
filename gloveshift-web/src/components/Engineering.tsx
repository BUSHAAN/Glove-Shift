import { motion } from 'framer-motion'
import { Camera, Hand, Keyboard, AppWindow } from 'lucide-react'
import { Container } from './ui/Container'
import { SectionLabel } from './ui/SectionLabel'

const features = [
  {
    icon: Camera,
    title: 'Real-time vision',
    body: 'OpenCV captures and processes webcam frames with a live preview of the tracked hand.',
    accent: 'text-gs-blue',
  },
  {
    icon: Hand,
    title: 'Gesture logic',
    body: 'Hand landmarks are interpreted with finger and tilt rules — accelerate, brake, steer left/right.',
    accent: 'text-gs-red',
  },
  {
    icon: Keyboard,
    title: 'Native input',
    body: 'Windows SendInput generates real keyboard events so any WASD racing game can respond.',
    accent: 'text-gs-blue',
  },
  {
    icon: AppWindow,
    title: 'Desktop application',
    body: 'PyQt6 provides start/stop controls, hand preference, sensitivity, and custom key mapping.',
    accent: 'text-gs-red',
  },
]

export function Engineering() {
  return (
    <section className="relative py-24 sm:py-32">
      <Container>
        <div className="max-w-2xl">
          <SectionLabel accent="red">Engineering</SectionLabel>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl">
            Built to ship on Windows.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-gs-muted sm:text-lg">
            Four layers that turn a webcam stream into OS-level keystrokes.
          </p>
        </div>

        <div className="mt-14 grid gap-5 md:grid-cols-2">
          {features.map((f, i) => (
            <motion.article
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{ delay: i * 0.05, duration: 0.4 }}
              className="group rounded-lg border border-gs-border bg-gs-surface p-7 transition-colors hover:border-gs-blue/30 sm:p-8"
            >
              <f.icon className={`size-7 ${f.accent}`} strokeWidth={1.5} />
              <h3 className="mt-6 font-display text-2xl font-semibold tracking-wide text-white uppercase">
                {f.title}
              </h3>
              <p className="mt-3 max-w-md text-sm leading-relaxed text-gs-muted sm:text-base">
                {f.body}
              </p>
            </motion.article>
          ))}
        </div>
      </Container>
    </section>
  )
}
