// Display helpers. Amounts arrive from the API as decimal strings ("1250.00").

const whole = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 })
const cents = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

export function toNumber(value) {
  const n = Number(value)
  return Number.isFinite(n) ? n : 0
}

/** "1,250" or "1,250.50": cents only when there are cents. */
export function formatAmount(value) {
  const n = toNumber(value)
  return Math.round(n * 100) % 100 === 0 ? whole.format(n) : cents.format(n)
}

export function formatSAR(value) {
  return `${formatAmount(value)} SAR`
}

export function percentOf(raised, goal) {
  const g = toNumber(goal)
  if (g <= 0) return 0
  return Math.min(100, Math.max(0, (toNumber(raised) / g) * 100))
}

export function formatDate(iso, { withTime = false } = {}) {
  if (!iso) return ''
  const date = new Date(iso)
  return date.toLocaleString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    ...(withTime ? { hour: '2-digit', minute: '2-digit' } : {}),
  })
}

const relative = new Intl.RelativeTimeFormat('en', { numeric: 'auto' })

export function timeAgo(iso) {
  if (!iso) return ''
  const seconds = Math.round((new Date(iso).getTime() - Date.now()) / 1000)
  const steps = [
    [60, 'second'],
    [60, 'minute'],
    [24, 'hour'],
    [7, 'day'],
    [4.35, 'week'],
    [12, 'month'],
    [Infinity, 'year'],
  ]
  let value = seconds
  for (const [size, unit] of steps) {
    if (Math.abs(value) < size) return relative.format(Math.round(value), unit)
    value /= size
  }
  return ''
}
