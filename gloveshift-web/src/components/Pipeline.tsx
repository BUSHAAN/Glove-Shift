import { motion } from 'framer-motion'
import { ArrowDown } from 'lucide-react'
import { Container } from './ui/Container'
import { SectionLabel } from './ui/SectionLabel'

const stages = [
  {
    code: 'CAMERA',
    title: 'Webcam',
    body: 'OpenCV captures frames from your webcam and shows a live preview.',
  },
  {
    code: 'VISION',
    title: 'MediaPipe Hands',
    body: 'MediaPipe Hand Landmarker finds 21 landmarks on a single hand.',
  },
  {
    code: 'RECOGNITION',
    title: 'Gesture rules',
    body: 'Landmark geometry determines accelerate, brake, or neutral — plus tilt for steer.',
  },
  {
    code: 'MAPPING',
    title: 'WASD mapping',
    body: 'Gestures become W / A / S / D commands (or your remapped keys).',
  },
  {
    code: 'INPUT',
    title: 'Windows SendInput',
    body: 'KeyboardInput injects press and release events at the OS level.',
  },
  {
    code: 'GAME',
    title: 'Racing game',
    body: 'The focused game receives normal keyboard input — no special support required.',
  },
]

export function Pipeline() {
  return (
    <section id="pipeline" className="relative py-24 sm:py-32">
      <Container>
        <div className="max-w-2xl">
          <SectionLabel>How it works</SectionLabel>
          <h2 className="mt-4 font-display text-4xl font-bold tracking-tight text-white uppercase sm:text-5xl">
            From pixels to keystrokes.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-gs-muted sm:text-lg">
            A cinematic pipeline from camera capture to the racing game —
            matching the real implementation.
          </p>
        </div>

        <div className="mt-14 space-y-0">
          {stages.map((stage, i) => (
            <motion.div
              key={stage.code}
              initial={{ opacity: 0, x: -16 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ duration: 0.4, delay: i * 0.04 }}
              className="relative"
            >
              <div className="grid gap-4 border-t border-gs-border py-6 sm:grid-cols-[140px_1fr] sm:items-start sm:gap-8 md:grid-cols-[160px_200px_1fr]">
                <span className="font-mono text-[11px] tracking-[0.24em] text-gs-blue uppercase">
                  {String(i + 1).padStart(2, '0')} · {stage.code}
                </span>
                <h3 className="font-display text-2xl font-semibold tracking-wide text-white uppercase">
                  {stage.title}
                </h3>
                <p className="text-sm leading-relaxed text-gs-muted sm:text-base md:pt-1">
                  {stage.body}
                </p>
              </div>
              {i < stages.length - 1 && (
                <div className="pointer-events-none absolute -bottom-1 left-[18px] hidden text-gs-dim sm:block md:left-6">
                  <ArrowDown className="size-3.5 opacity-40" />
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </Container>
    </section>
  )
}
