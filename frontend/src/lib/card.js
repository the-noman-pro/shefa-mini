// Card rules for the simulated top-up, used for live feedback in the form.
// The server (backend/apps/wallets/cards.py) applies the same rules again.

export const MIN_TOP_UP = 10
export const MAX_TOP_UP = 10000
export const DECLINED_TEST_CARD = '4000000000000002'

const MADA_PREFIXES = [
  '440647', '440795', '446404', '457865', '457997', '474491', '588845', '588846',
  '588847', '588848', '588849', '588850', '588851', '588982', '589005', '604906',
  '636120', '968201', '968202', '968203', '968204', '968205', '968206', '968207',
  '968208', '968209', '968210', '968211',
] // prettier-ignore

export const BRAND_LABELS = { visa: 'Visa', mastercard: 'Mastercard', mada: 'Mada', amex: 'Amex' }

export function digitsOnly(value) {
  return String(value ?? '').replace(/\D/g, '')
}

export function luhnValid(number) {
  if (!/^\d+$/.test(number)) return false
  let total = 0
  for (let i = 0; i < number.length; i++) {
    let digit = Number(number[number.length - 1 - i])
    if (i % 2 === 1) {
      digit *= 2
      if (digit > 9) digit -= 9
    }
    total += digit
  }
  return total % 10 === 0
}

/** "mada" | "visa" | "mastercard" | "amex" | "" from the leading digits. */
export function detectBrand(number) {
  if (!number) return ''
  if (MADA_PREFIXES.some((prefix) => number.startsWith(prefix))) return 'mada'
  if (number.startsWith('4')) return 'visa'
  if (/^3[47]/.test(number)) return 'amex'
  const two = Number(number.slice(0, 2))
  if (number.length >= 2 && two >= 51 && two <= 55) return 'mastercard'
  const four = Number(number.slice(0, 4))
  if (number.length >= 4 && four >= 2221 && four <= 2720) return 'mastercard'
  return ''
}

export function maxDigits(brand) {
  return brand === 'amex' ? 15 : 19
}

/** Groups digits the way they are printed: Amex 4-6-5, everything else in fours. */
export function formatCardNumber(value) {
  const number = digitsOnly(value)
  const brand = detectBrand(number)
  const digits = number.slice(0, maxDigits(brand))
  if (brand === 'amex') {
    return [digits.slice(0, 4), digits.slice(4, 10), digits.slice(10, 15)].filter(Boolean).join(' ')
  }
  return digits.replace(/(\d{4})(?=\d)/g, '$1 ')
}

export function cardNumberError(value) {
  const number = digitsOnly(value)
  if (!number) return 'Enter the card number.'
  if (number.length < 13 || number.length > 19) return 'A card number has 13 to 19 digits.'
  const brand = detectBrand(number)
  if (!brand) return 'We accept Visa, Mastercard, Mada and Amex.'
  if (brand === 'amex' && number.length !== 15) return 'An Amex number has 15 digits.'
  if (!luhnValid(number)) return 'This card number is not valid. Check the digits.'
  return ''
}

/** Masks typing into "MM/YY": "1" -> "1", "12" -> "12/", "125" -> "12/5", "4" -> "04/". */
export function formatExpiry(value, previous = '') {
  let digits = digitsOnly(value).slice(0, 4)
  if (digits.length === 1 && Number(digits) > 1) digits = `0${digits}`
  const deleting = String(value).length < String(previous).length
  if (digits.length >= 3) return `${digits.slice(0, 2)}/${digits.slice(2)}`
  if (digits.length === 2 && !deleting) return `${digits}/`
  return digits
}

export function expiryError(value, today = new Date()) {
  const match = /^\s*(\d{2})\s*\/\s*(\d{2})\s*$/.exec(value || '')
  if (!match) return 'Use the format MM/YY.'
  const month = Number(match[1])
  const year = 2000 + Number(match[2])
  if (month < 1 || month > 12) return 'The month must be between 01 and 12.'
  const nowYear = today.getFullYear()
  const nowMonth = today.getMonth() + 1
  if (year < nowYear || (year === nowYear && month < nowMonth)) return 'This card has expired.'
  if (year > nowYear + 20) return 'Check the expiry year.'
  return ''
}

export function cvvLength(brand) {
  return brand === 'amex' ? 4 : 3
}

export function cvvError(value, brand) {
  const length = cvvLength(brand)
  if (!new RegExp(`^\\d{${length}}$`).test(value || ''))
    return `The security code is ${length} digits.`
  return ''
}

export function cardHolderError(value) {
  const name = String(value || '')
    .trim()
    .replace(/\s+/g, ' ')
  if (name.length < 2 || !/^[A-Za-z][A-Za-z .'-]*$/.test(name)) {
    return 'Enter the name as printed on the card.'
  }
  return ''
}

export function amountError(value, { min = MIN_TOP_UP, max = MAX_TOP_UP } = {}) {
  const text = String(value ?? '').trim()
  if (!text) return 'Enter an amount in SAR.'
  if (!/^\d+(\.\d{1,2})?$/.test(text)) {
    return /^\d+\.\d{3,}$/.test(text)
      ? 'Use at most two decimal places.'
      : 'Enter an amount in SAR.'
  }
  const amount = Number(text)
  if (amount < min) return `The minimum is ${min.toLocaleString('en-US')} SAR.`
  if (amount > max) return `The maximum is ${max.toLocaleString('en-US')} SAR.`
  return ''
}
