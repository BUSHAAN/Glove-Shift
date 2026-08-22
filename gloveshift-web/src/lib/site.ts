export const SITE = {
  name: 'Glove Shift',
  tagline: 'Your Webcam. Your Controller.',
  title: 'Glove Shift — Your Webcam. Your Controller.',
  description:
    'Glove Shift turns your webcam into a racing controller. Real-time hand gestures become WASD input for Windows racing games.',
  url: (import.meta.env.VITE_SITE_URL as string | undefined)?.replace(/\/$/, '') ||
    'https://gloveshift-web.vercel.app',
  locale: 'en_US',
  twitterHandle: '',
  ogImagePath: '/og-image.png',
  themeColor: '#000000',
} as const

export const SITE_URL = SITE.url
export const OG_IMAGE_URL = `${SITE.url}${SITE.ogImagePath}`
