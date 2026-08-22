import { motion } from 'framer-motion'
import { Download, Code, Play } from 'lucide-react'
import { Container } from './ui/Container'
import { Button } from './ui/Button'
import { LINKS } from '../lib/constants'
import logo from '../assets/logo.png'

const easeOut = [0.22, 1, 0.36, 1] as const

const fadeUp = {
  hidden: { opacity: 0, y: 28 },
  show: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: 0.08 * i, duration: 0.55, ease: easeOut },
  }),
}

export function Hero() {
  return (
    <section
      id="top"
      className="relative min-h-svh overflow-hidden pt-16"
    >
      <div className="pointer-events-none absolute inset-0 grid-tech opacity-60" />
      <div className="pointer-events-none absolute inset-0 noise-overlay opacity-40" />
      <div
        className="pointer-events-none absolute -left-1/4 top-1/4 size-[520px] rounded-full blur-[120px]"
        style={{ background: 'radial-gradient(circle, rgba(0,163,255,0.18), transparent 70%)' }}
      />
      <div
        className="pointer-events-none absolute -right-1/4 bottom-0 size-[480px] rounded-full blur-[120px]"
        style={{ background: 'radial-gradient(circle, rgba(216,30,39,0.16), transparent 70%)' }}
      />

      <Container className="relative flex min-h-[calc(100svh-4rem)] flex-col justify-center py-16 lg:py-20">
        <div className="grid items-center gap-12 lg:grid-cols-[1.05fr_0.95fr] lg:gap-10">
          <div>
            <motion.p
              custom={0}
              variants={fadeUp}
              initial="hidden"
              animate="show"
              className="mb-5 font-mono text-[11px] tracking-[0.28em] text-gs-blue uppercase"
            >
              Computer vision · Racing control
            </motion.p>

            <motion.h1
              custom={1}
              variants={fadeUp}
              initial="hidden"
              animate="show"
              className="font-display text-[clamp(2.75rem,8vw,5.5rem)] leading-[0.92] font-extrabold tracking-tight text-white uppercase"
            >
              <span className="block text-gs-silver">Your webcam.</span>
              <span className="block text-white">Your hands.</span>
              <span className="block text-gs-red">Your racing wheel.</span>
            </motion.h1>

            <motion.p
              custom={2}
              variants={fadeUp}
              initial="hidden"
              animate="show"
              className="mt-6 max-w-xl text-lg leading-relaxed text-gs-muted sm:text-xl"
            >
              Glove Shift turns real-time hand gestures into racing controls.
            </motion.p>
            <motion.p
              custom={3}
              variants={fadeUp}
              initial="hidden"
              animate="show"
              className="mt-3 max-w-lg text-base leading-relaxed text-gs-dim"
            >
              Control racing games using nothing but your hands and a webcam.
            </motion.p>

            <motion.div
              custom={4}
              variants={fadeUp}
              initial="hidden"
              animate="show"
              className="mt-9 flex flex-wrap gap-3"
            >
              <Button href={LINKS.download}>
                <Download className="size-3.5" />
                Download Glove Shift
              </Button>
              <Button href={LINKS.github} variant="secondary">
                <Code className="size-3.5" />
                View on GitHub
              </Button>
            </motion.div>
          </div>

          <motion.div
            custom={5}
            variants={fadeUp}
            initial="hidden"
            animate="show"
            className="relative mx-auto w-full max-w-md lg:max-w-none"
          >
            <div className="absolute inset-0 -m-6 rounded-full bg-[conic-gradient(from_210deg,#00a3ff,#0a0a0a_35%,#d81e27,#0a0a0a_70%,#00a3ff)] opacity-40 blur-2xl" />
            <div className="border-gradient-ring relative overflow-hidden rounded-2xl bg-gs-surface p-6 sm:p-8">
              <img
                src={logo}
                alt="Glove Shift — Your webcam. Your controller."
                className="mx-auto w-full max-w-sm drop-shadow-[0_20px_50px_rgba(0,0,0,0.65)]"
              />
              <a
                href={LINKS.demo}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-6 flex items-center gap-4 rounded-sm border border-gs-border bg-gs-elevated/80 p-4 transition-colors hover:border-gs-blue/40"
              >
                <span className="flex size-11 shrink-0 items-center justify-center rounded-full bg-gs-blue/15 text-gs-blue">
                  <Play className="size-4 fill-current" />
                </span>
                <span className="text-left">
                  <span className="block font-mono text-[10px] tracking-[0.22em] text-gs-blue uppercase">
                    Watch demo
                  </span>
                  <span className="mt-1 block text-sm text-gs-silver">
                    See hand gestures drive a racing game
                  </span>
                </span>
              </a>
            </div>
          </motion.div>
        </div>
      </Container>
    </section>
  )
}
