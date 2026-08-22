import { defineConfig, loadEnv, type Plugin } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'
import tailwindcss from '@tailwindcss/vite'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const rootDir = path.dirname(fileURLToPath(import.meta.url))

function seoFilesPlugin(siteUrl: string): Plugin {
  const write = (dir: string) => {
    const origin = siteUrl.replace(/\/$/, '')
    fs.mkdirSync(dir, { recursive: true })
    fs.writeFileSync(
      path.join(dir, 'robots.txt'),
      [
        'User-agent: *',
        'Allow: /',
        '',
        `Sitemap: ${origin}/sitemap.xml`,
        '',
      ].join('\n'),
    )
    fs.writeFileSync(
      path.join(dir, 'sitemap.xml'),
      [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        `    <loc>${origin}/</loc>`,
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '</urlset>',
        '',
      ].join('\n'),
    )
  }

  return {
    name: 'gloveshift-seo-files',
    buildStart() {
      write(path.resolve(rootDir, 'public'))
    },
    writeBundle(options) {
      if (options.dir) write(options.dir)
    },
  }
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, rootDir, '')
  const siteUrl =
    env.VITE_SITE_URL?.replace(/\/$/, '') || 'https://gloveshift-web.vercel.app'

  return {
    plugins: [
      react(),
      babel({ presets: [reactCompilerPreset()] }),
      tailwindcss(),
      seoFilesPlugin(siteUrl),
    ],
  }
})
