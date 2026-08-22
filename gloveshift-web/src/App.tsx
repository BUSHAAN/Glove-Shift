import { Nav } from './components/Nav'
import { Hero } from './components/Hero'
import { Gestures } from './components/Gestures'
import { Idea } from './components/Idea'
import { Pipeline } from './components/Pipeline'
import { Vision } from './components/Vision'
import { Engineering } from './components/Engineering'
import { Tech } from './components/Tech'
import { DownloadCTA } from './components/DownloadCTA'
import { Explore } from './components/Explore'
import { Footer } from './components/Footer'

function App() {
  return (
    <div className="bg-gs-black text-gs-silver">
      <Nav />
      <main>
        <Hero />
        <Gestures />
        <Idea />
        <Pipeline />
        <Vision />
        <Engineering />
        <Tech />
        <DownloadCTA />
        <Explore />
      </main>
      <Footer />
    </div>
  )
}

export default App
