import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export function currency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value ?? 0)
}

export function groupSeats(seats = []) {
  return seats.reduce((acc, seat) => {
    const row = seat.row
    if (!acc[row]) acc[row] = []
    acc[row].push(seat)
    return acc
  }, {})
}

export function getYouTubeVideoId(url) {
  if (!url) return ''
  return (
    url.match(/[?&]v=([^&]+)/)?.[1] ||
    url.match(/youtu\.be\/([^?&]+)/)?.[1] ||
    url.match(/embed\/([^?&]+)/)?.[1] ||
    ''
  )
}

export function normalizeTrailerUrl(url) {
  if (!url) return ''
  const videoId = getYouTubeVideoId(url)
  if (!videoId) return url
  return `https://www.youtube.com/embed/${videoId}`
}

export function trailerAutoplayUrl(url) {
  if (!url) return ''
  const videoId = getYouTubeVideoId(url)

  if (!videoId) {
    return `${url}${url.includes('?') ? '&' : '?'}autoplay=1&mute=1&rel=0&playsinline=1`
  }

  return `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&rel=0&playsinline=1`
}

export function moviePaletteStyle(movie) {
  return {
    '--movie-primary': movie?.palette?.primary ?? '#69e6ff',
    '--movie-secondary': movie?.palette?.secondary ?? '#0f172a',
    '--movie-accent': movie?.palette?.accent ?? '#f6c469',
  }
}
