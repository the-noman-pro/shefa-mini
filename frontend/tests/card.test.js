import { describe, expect, it } from 'vitest'

import { cardNumberError, cvvError, expiryError, luhnValid } from '../src/lib/card.js'

describe('luhnValid', () => {
  it('accepts a number whose check digit is right', () => {
    expect(luhnValid('4242424242424242')).toBe(true)
  })

  it('handles digits that double past 9', () => {
    expect(luhnValid('5555555555554444')).toBe(true)
  })

  it('rejects the same number with the last digit changed', () => {
    expect(luhnValid('4242424242424241')).toBe(false)
  })

  it('rejects anything that is not only digits', () => {
    expect(luhnValid('4242 4242 4242 4242')).toBe(false)
    expect(luhnValid('')).toBe(false)
  })
})

describe('cardNumberError', () => {
  it('accepts a valid Visa typed with spaces', () => {
    expect(cardNumberError('4242 4242 4242 4242')).toBe('')
  })

  it('accepts a valid 15-digit Amex', () => {
    expect(cardNumberError('378282246310005')).toBe('')
  })

  it('refuses a number that fails the Luhn check', () => {
    expect(cardNumberError('4242424242424241')).toMatch(/not valid/)
  })

  it('refuses a number that is too short', () => {
    expect(cardNumberError('4242')).toMatch(/13 to 19 digits/)
  })
})

describe('expiryError', () => {
  const today = new Date(2026, 10, 25)

  it('accepts a future month', () => {
    expect(expiryError('12/26', today)).toBe('')
  })

  it('accepts the current month, as the card is valid until its end', () => {
    expect(expiryError('11/26', today)).toBe('')
  })

  it('refuses a past month', () => {
    expect(expiryError('10/26', today)).toMatch(/expired/)
  })

  it('refuses a month that does not exist', () => {
    expect(expiryError('13/27', today)).toMatch(/between 01 and 12/)
  })

  it('refuses a value that is not MM/YY', () => {
    expect(expiryError('1226', today)).toMatch(/MM\/YY/)
  })
})

describe('cvvError', () => {
  it('wants 3 digits for Visa', () => {
    expect(cvvError('123', 'visa')).toBe('')
    expect(cvvError('12', 'visa')).toMatch(/3 digits/)
  })

  it('wants 4 digits for Amex', () => {
    expect(cvvError('1234', 'amex')).toBe('')
    expect(cvvError('123', 'amex')).toMatch(/4 digits/)
  })
})
