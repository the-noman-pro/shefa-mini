<script setup>
import { computed } from 'vue'
import { BRAND_LABELS, cvvLength, detectBrand, digitsOnly, formatCardNumber } from '@/lib/card'

// A live picture of the card being typed. It turns over while the CVV field has focus.
const props = defineProps({
  holder: { type: String, default: '' },
  number: { type: String, default: '' },
  expiry: { type: String, default: '' },
  cvv: { type: String, default: '' },
  flipped: { type: Boolean, default: false },
  state: { type: String, default: 'idle' }, // idle | processing | approved | declined
})

const digits = computed(() => digitsOnly(props.number))
const brand = computed(() => detectBrand(digits.value))

const shownNumber = computed(() => {
  const template = brand.value === 'amex' ? '•••• •••••• •••••' : '•••• •••• •••• ••••'
  const typed = formatCardNumber(digits.value)
  return typed + template.slice(typed.length)
})

const shownCvv = computed(() => {
  const length = cvvLength(brand.value)
  return '•'.repeat(Math.min(props.cvv.length, length)).padEnd(length, '○')
})
</script>

<template>
  <div class="card-scene" :class="[`card-scene--${state}`, brand && `brand--${brand}`]">
    <div class="card" :class="{ 'card--flipped': flipped }">
      <div class="face front" aria-hidden="true">
        <svg class="pattern" viewBox="0 0 340 214" preserveAspectRatio="none">
          <path d="M210 0c-10 60 30 110 130 120" />
          <path d="M240 0c-6 44 22 84 100 92" />
          <path d="M270 0c-2 28 14 56 70 62" />
          <path d="M0 170c60-20 120 10 170 44" />
        </svg>
        <div class="top">
          <span class="wordmark">Shefa <em>mini</em></span>
          <span class="brand" :class="{ 'brand--on': brand }">{{
            BRAND_LABELS[brand] || 'Card'
          }}</span>
        </div>
        <svg class="chip" viewBox="0 0 44 34">
          <rect
            x="1"
            y="1"
            width="42"
            height="32"
            rx="6"
            fill="#f1c76a"
            stroke="#2b2420"
            stroke-width="1.6"
          />
          <path
            d="M1 12h12M1 22h12M31 12h12M31 22h12M13 1v32M31 1v32"
            stroke="#2b2420"
            stroke-width="1.2"
            fill="none"
            opacity="0.6"
          />
        </svg>
        <div class="number num">{{ shownNumber }}</div>
        <div class="bottom">
          <div>
            <span class="caption">Card holder</span>
            <span class="value holder">{{ holder.trim() || 'Your name' }}</span>
          </div>
          <div>
            <span class="caption">Valid thru</span>
            <span class="value num">{{ expiry || 'MM/YY' }}</span>
          </div>
        </div>
      </div>
      <div class="face back" aria-hidden="true">
        <div class="strip" />
        <div class="sign">
          <span class="sign-lines" />
          <span class="cvv num">{{ shownCvv }}</span>
        </div>
        <p class="back-note">
          The 3-digit code is on the back; on Amex it is the 4 digits on the front.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-scene {
  perspective: 1200px;
  width: 100%;
  max-width: 340px;
  margin-inline: auto;
}

.card {
  position: relative;
  aspect-ratio: 340 / 214;
  transform-style: preserve-3d;
  transition: transform 0.7s var(--ease-out);
}

.card--flipped {
  transform: rotateY(180deg);
}

.face {
  position: absolute;
  inset: 0;
  border-radius: 18px;
  border: 2px solid var(--ink);
  box-shadow: 4px 5px 0 var(--ink);
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  overflow: hidden;
  color: #fff8ee;
}

.front {
  background: var(--clay);
  padding: 16px 20px;
  display: grid;
  grid-template-rows: auto 1fr auto auto;
  transition: background-color 0.4s;
}

.brand--visa .front {
  background: #2f5f7a;
}
.brand--mastercard .front {
  background: #7a3a2a;
}
.brand--mada .front {
  background: var(--palm);
}
.brand--amex .front {
  background: #4f5b6b;
}

.pattern {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  fill: none;
  stroke: rgb(255 248 238 / 0.18);
  stroke-width: 2;
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.wordmark {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.05rem;
}

.wordmark em {
  font-style: italic;
  font-weight: 400;
  opacity: 0.85;
}

.brand {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1.5px solid rgb(255 248 238 / 0.5);
  opacity: 0.6;
  transition: opacity 0.2s;
}

.brand--on {
  opacity: 1;
  background: rgb(255 248 238 / 0.16);
}

.chip {
  width: 44px;
  align-self: center;
  position: relative;
}

.number {
  position: relative;
  font-family: var(--font-mono);
  font-size: clamp(1.02rem, 4.6vw, 1.32rem);
  letter-spacing: 0.06em;
  white-space: nowrap;
  margin-bottom: 10px;
}

.bottom {
  position: relative;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.caption {
  display: block;
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.75;
}

.value {
  display: block;
  font-weight: 600;
  font-size: 0.92rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.holder {
  max-width: 190px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.back {
  background: #3a302a;
  transform: rotateY(180deg);
  padding-top: 22px;
}

.strip {
  height: 40px;
  background: #1c1714;
}

.sign {
  margin: 18px 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.sign-lines {
  flex: 1;
  height: 34px;
  border-radius: 4px;
  background: repeating-linear-gradient(-45deg, #f6eadb 0 6px, #ead8c2 6px 12px);
}

.cvv {
  background: #fff;
  color: var(--ink);
  font-family: var(--font-mono);
  font-weight: 700;
  padding: 6px 10px;
  border-radius: 4px;
  border: 2px solid var(--saffron);
  letter-spacing: 0.12em;
}

.back-note {
  margin: 14px 20px 0;
  font-size: 0.7rem;
  opacity: 0.75;
}

/* Processing: the card floats gently while we wait */
.card-scene--processing .card {
  animation: float 1.6s ease-in-out infinite;
}

.card-scene--declined .card {
  animation: shake 0.45s ease-in-out;
}

@keyframes float {
  50% {
    transform: translateY(-8px) rotate(-1deg);
  }
}

@keyframes shake {
  20%,
  60% {
    transform: translateX(-8px);
  }
  40%,
  80% {
    transform: translateX(8px);
  }
}
</style>
