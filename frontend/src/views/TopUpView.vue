<script setup>
import { computed, reactive, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import CardPreview from '@/components/CardPreview.vue'
import Icon from '@/components/Icon.vue'
import Money from '@/components/Money.vue'
import WalletArt from '@/components/art/WalletArt.vue'
import { api } from '@/lib/api'
import {
  BRAND_LABELS,
  MAX_TOP_UP,
  MIN_TOP_UP,
  amountError,
  cardHolderError,
  cardNumberError,
  cvvError,
  cvvLength,
  detectBrand,
  digitsOnly,
  expiryError,
  formatCardNumber,
  formatExpiry,
  luhnValid,
} from '@/lib/card'
import { prefersReducedMotion, wait } from '@/lib/motion'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()

const QUICK = [50, 100, 250, 500]
const returnSlug = typeof route.query.case === 'string' ? route.query.case : ''
const suggested = Number(route.query.amount)

const form = reactive({
  card_holder: auth.user?.name || '',
  card_number: '',
  expiry: '',
  cvv: '',
  amount:
    Number.isFinite(suggested) && suggested >= MIN_TOP_UP && suggested <= MAX_TOP_UP
      ? String(suggested)
      : '100',
})

const touched = reactive({})
const serverErrors = reactive({})
const cvvFocused = ref(false)
const step = ref('form') // form | processing | approved | declined
const processingStage = ref(0)
const generalError = ref('')
const declineMessage = ref('')
const result = ref(null)
const balanceBefore = ref('0')

const digits = computed(() => digitsOnly(form.card_number))
const brand = computed(() => detectBrand(digits.value))

const errors = computed(() => ({
  card_holder: cardHolderError(form.card_holder),
  card_number: cardNumberError(form.card_number),
  expiry: expiryError(form.expiry),
  cvv: cvvError(form.cvv, brand.value),
  amount: amountError(form.amount),
}))

function shown(field) {
  return serverErrors[field] || (touched[field] ? errors.value[field] : '')
}

// A gentle live hint once enough digits are in, before the field is left.
const numberHint = computed(() => {
  const n = digits.value
  if (n.length < 13) return null
  const full = brand.value === 'amex' ? n.length === 15 : n.length >= 16
  if (!brand.value) return { ok: false, text: 'We accept Visa, Mastercard, Mada and Amex.' }
  if (luhnValid(n)) return { ok: true, text: 'The number checks out.' }
  return full ? { ok: false, text: 'One digit looks off. Check the number.' } : null
})

function onNumber(event) {
  const formatted = formatCardNumber(event.target.value)
  form.card_number = formatted
  event.target.value = formatted
  delete serverErrors.card_number
}

function onExpiry(event) {
  const masked = formatExpiry(event.target.value, form.expiry)
  form.expiry = masked
  event.target.value = masked
  delete serverErrors.expiry
}

function onCvv(event) {
  const clean = digitsOnly(event.target.value).slice(0, cvvLength(brand.value))
  form.cvv = clean
  event.target.value = clean
  delete serverErrors.cvv
}

function pickAmount(value) {
  form.amount = String(value)
  delete serverErrors.amount
}

function touchAll() {
  for (const key of Object.keys(form)) touched[key] = true
}

function firstInvalid() {
  return ['card_holder', 'card_number', 'expiry', 'cvv', 'amount'].find(
    (key) => shown(key) || errors.value[key],
  )
}

async function submit() {
  touchAll()
  generalError.value = ''
  const bad = firstInvalid()
  if (bad) {
    document.getElementById(`f-${bad}`)?.focus()
    return
  }
  step.value = 'processing'
  processingStage.value = 0
  balanceBefore.value = auth.balance

  const minimum = prefersReducedMotion() ? 0 : 1900
  const stageTimer = setInterval(() => {
    processingStage.value = Math.min(2, processingStage.value + 1)
  }, 650)

  try {
    const [response] = await Promise.all([
      api.topUp({
        card_holder: form.card_holder,
        card_number: digits.value,
        expiry: form.expiry,
        cvv: form.cvv,
        amount: form.amount,
      }),
      wait(minimum),
    ])
    result.value = response
    auth.setBalance(response.balance)
    form.cvv = ''
    step.value = 'approved'
  } catch (e) {
    await wait(prefersReducedMotion() ? 0 : 400)
    if (e.status === 402) {
      declineMessage.value = e.message
      step.value = 'declined'
    } else {
      Object.assign(serverErrors, e.fields)
      generalError.value = e.message
      step.value = 'form'
    }
  } finally {
    clearInterval(stageTimer)
  }
}

function tryAnotherCard() {
  form.card_number = ''
  form.cvv = ''
  touched.card_number = false
  touched.cvv = false
  step.value = 'form'
  setTimeout(() => document.getElementById('f-card_number')?.focus(), 50)
}

const STAGES = [
  'Checking the card details',
  'Asking the bank to approve',
  'Adding it to your wallet',
]
</script>

<template>
  <div class="container page">
    <RouterLink
      :to="returnSlug ? { name: 'case', params: { slug: returnSlug } } : { name: 'account' }"
      class="back"
    >
      <Icon name="arrow-left" :size="18" /> {{ returnSlug ? 'Back to the case' : 'Your account' }}
    </RouterLink>

    <div class="wrap">
      <header class="head">
        <h1>Top up your wallet</h1>
        <p class="lede">
          Your wallet holds <strong><Money :value="auth.balance" /></strong>. Add money once, then
          give to any case.
        </p>
      </header>

      <CardPreview
        class="preview"
        :holder="form.card_holder"
        :number="form.card_number"
        :expiry="form.expiry"
        :cvv="form.cvv"
        :flipped="cvvFocused && step === 'form'"
        :state="step"
      />

      <!-- 1. The card form -->
      <form v-if="step === 'form'" class="panel form" novalidate @submit.prevent="submit">
        <p class="alert alert-info demo">
          <Icon name="info" />
          <span>
            <strong>Demo only.</strong> No real card is charged.
            <span class="test-cards">
              <span>Approved: <code>4242 4242 4242 4242</code></span>
              <span>Declined: <code>4000 0000 0000 0002</code></span>
            </span>
          </span>
        </p>

        <p v-if="generalError" class="alert alert-error" role="alert">
          <Icon name="alert" /> {{ generalError }}
        </p>

        <div class="field">
          <label class="field-label" for="f-card_holder">Name on card</label>
          <input
            id="f-card_holder"
            v-model="form.card_holder"
            class="input"
            autocomplete="cc-name"
            :aria-invalid="shown('card_holder') ? 'true' : undefined"
            aria-describedby="e-card_holder"
            @blur="touched.card_holder = true"
            @input="delete serverErrors.card_holder"
          />
          <p v-if="shown('card_holder')" id="e-card_holder" class="field-error">
            <Icon name="alert" :size="16" /> {{ shown('card_holder') }}
          </p>
        </div>

        <div class="field">
          <label class="field-label" for="f-card_number">Card number</label>
          <div class="with-badge">
            <input
              id="f-card_number"
              :value="form.card_number"
              class="input num mono"
              inputmode="numeric"
              autocomplete="cc-number"
              placeholder="1234 5678 9012 3456"
              :maxlength="brand === 'amex' ? 17 : 23"
              :aria-invalid="shown('card_number') ? 'true' : undefined"
              aria-describedby="e-card_number h-card_number"
              @input="onNumber"
              @blur="touched.card_number = true"
            />
            <span class="badge" :class="{ on: brand }" aria-live="polite">
              {{ BRAND_LABELS[brand] || 'Brand' }}
            </span>
          </div>
          <p v-if="shown('card_number')" id="e-card_number" class="field-error">
            <Icon name="alert" :size="16" /> {{ shown('card_number') }}
          </p>
          <p
            v-else-if="numberHint"
            id="h-card_number"
            class="hint-live"
            :class="numberHint.ok ? 'ok' : 'warn'"
          >
            <Icon :name="numberHint.ok ? 'check' : 'info'" :size="16" /> {{ numberHint.text }}
          </p>
        </div>

        <div class="split">
          <div class="field">
            <label class="field-label" for="f-expiry">Expiry</label>
            <input
              id="f-expiry"
              :value="form.expiry"
              class="input num"
              inputmode="numeric"
              autocomplete="cc-exp"
              placeholder="MM/YY"
              maxlength="5"
              :aria-invalid="shown('expiry') ? 'true' : undefined"
              aria-describedby="e-expiry"
              @input="onExpiry"
              @blur="touched.expiry = true"
            />
            <p v-if="shown('expiry')" id="e-expiry" class="field-error">
              <Icon name="alert" :size="16" /> {{ shown('expiry') }}
            </p>
          </div>
          <div class="field">
            <label class="field-label" for="f-cvv">Security code</label>
            <input
              id="f-cvv"
              :value="form.cvv"
              class="input num"
              type="password"
              inputmode="numeric"
              autocomplete="cc-csc"
              :placeholder="brand === 'amex' ? '4 digits' : '3 digits'"
              :maxlength="cvvLength(brand)"
              :aria-invalid="shown('cvv') ? 'true' : undefined"
              aria-describedby="e-cvv"
              @input="onCvv"
              @focus="cvvFocused = true"
              @blur="((cvvFocused = false), (touched.cvv = true))"
            />
            <p v-if="shown('cvv')" id="e-cvv" class="field-error">
              <Icon name="alert" :size="16" /> {{ shown('cvv') }}
            </p>
          </div>
        </div>

        <fieldset class="field amount-field">
          <legend class="field-label">Amount (SAR)</legend>
          <div class="quick">
            <button
              v-for="q in QUICK"
              :key="q"
              type="button"
              class="quick-btn"
              :aria-pressed="form.amount === String(q)"
              @click="pickAmount(q)"
            >
              <span class="num">{{ q }}</span>
            </button>
          </div>
          <label class="amount-input">
            <span class="visually-hidden">Amount in SAR</span>
            <input
              id="f-amount"
              v-model.trim="form.amount"
              class="input num"
              inputmode="decimal"
              :aria-invalid="shown('amount') ? 'true' : undefined"
              aria-describedby="e-amount h-amount"
              @blur="touched.amount = true"
              @input="delete serverErrors.amount"
            />
            <span class="suffix" aria-hidden="true">SAR</span>
          </label>
          <p v-if="shown('amount')" id="e-amount" class="field-error">
            <Icon name="alert" :size="16" /> {{ shown('amount') }}
          </p>
          <p id="h-amount" class="field-hint">
            Between {{ MIN_TOP_UP }} and {{ MAX_TOP_UP.toLocaleString('en-US') }} SAR.
          </p>
        </fieldset>

        <button type="submit" class="btn btn-block submit">
          <Icon name="lock" :size="18" />
          Add <Money :value="Number(form.amount) > 0 ? form.amount : 0" /> to wallet
        </button>
        <p class="fine">
          We keep only the card brand and last four digits. The full number and code are never
          stored.
        </p>
      </form>

      <!-- 2. Processing -->
      <section v-else-if="step === 'processing'" class="panel status" aria-live="polite">
        <h2 class="status-title">Processing your top-up</h2>
        <ol class="stages">
          <li
            v-for="(label, i) in STAGES"
            :key="label"
            :class="{ done: i < processingStage, current: i === processingStage }"
          >
            <span class="dot" aria-hidden="true">
              <Icon v-if="i < processingStage" name="check" :size="14" :stroke-width="2.6" />
            </span>
            {{ label }}<span v-if="i === processingStage" class="ellipsis" aria-hidden="true" />
          </li>
        </ol>
        <p class="fine">Please keep this page open.</p>
      </section>

      <!-- 3. Approved -->
      <section v-else-if="step === 'approved'" class="panel status approved" aria-live="polite">
        <div class="approved-art"><WalletArt /></div>
        <p class="stamp"><Icon name="check" :size="18" :stroke-width="2.6" /> Approved</p>
        <h2 class="status-title">
          <Money :value="result.transaction.amount" /> added to your wallet
        </h2>
        <p class="new-balance">
          <span>New balance</span>
          <strong
            ><Money :value="result.balance" :count-from="balanceBefore" :duration="1400"
          /></strong>
        </p>
        <p class="fine">
          Reference <span class="mono">{{ result.transaction.reference }}</span> ·
          {{ BRAND_LABELS[result.transaction.card_brand] }} •••• {{ result.transaction.card_last4 }}
        </p>
        <div class="status-actions">
          <RouterLink
            v-if="returnSlug"
            :to="{ name: 'case', params: { slug: returnSlug } }"
            class="btn btn-block"
          >
            <Icon name="heart" :size="18" /> Continue to the case
          </RouterLink>
          <RouterLink v-else to="/" class="btn btn-block">
            <Icon name="heart" :size="18" /> Find a case to give to
          </RouterLink>
          <RouterLink to="/account" class="btn btn-quiet btn-block">See your wallet</RouterLink>
        </div>
      </section>

      <!-- 4. Declined -->
      <section v-else class="panel status declined" role="alert">
        <p class="stamp stamp--declined">
          <Icon name="x" :size="18" :stroke-width="2.6" /> Declined
        </p>
        <h2 class="status-title">The card was not accepted</h2>
        <p>{{ declineMessage }} Nothing was charged and your wallet is unchanged.</p>
        <div class="status-actions">
          <button type="button" class="btn btn-block" @click="tryAnotherCard">
            Try another card
          </button>
          <RouterLink to="/account" class="btn btn-quiet btn-block"
            >Back to your account</RouterLink
          >
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding-top: 20px;
}

.back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  text-decoration: none;
  margin-bottom: 16px;
}

.wrap {
  max-width: var(--form-max);
  margin-inline: auto;
  display: grid;
  gap: 22px;
}

.head h1 {
  font-size: var(--text-2xl);
}

.lede {
  margin-top: 6px;
  color: var(--ink-soft);
}

.preview {
  margin-block: 4px 6px;
}

.form,
.status {
  padding: 22px;
}

.demo {
  margin-bottom: 18px;
}

.test-cards {
  display: grid;
  margin-top: 4px;
}

.demo code {
  font-family: var(--font-mono);
  font-size: 0.92em;
  white-space: nowrap;
  font-weight: 700;
}

.form > .alert-error {
  margin-bottom: 16px;
}

.mono {
  font-family: var(--font-mono);
  letter-spacing: 0.04em;
}

.with-badge {
  position: relative;
}

.with-badge .input {
  padding-right: 110px;
}

.badge {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  padding: 3px 10px;
  border-radius: 999px;
  font-size: var(--text-xs);
  font-weight: 700;
  border: 1.5px dashed var(--line-strong);
  color: var(--ink-muted);
  transition: all 0.2s var(--ease-out);
}

.badge.on {
  border-style: solid;
  border-color: var(--ink);
  background: var(--saffron-soft);
  color: var(--ink);
}

.hint-live {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-sm);
}

.hint-live.ok {
  color: var(--palm);
}

.hint-live.warn {
  color: #8a5a10;
}

.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 16px;
}

.split .field + .field {
  margin-top: 0;
}

.amount-field {
  border: 0;
  padding: 0;
  margin: 16px 0 0;
}

.amount-field legend {
  margin-bottom: 6px;
}

.quick {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}

.quick-btn {
  min-height: 42px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--line-strong);
  background: var(--surface);
  font-weight: 700;
  cursor: pointer;
}

.quick-btn:hover {
  border-color: var(--ink);
}

.quick-btn[aria-pressed='true'] {
  background: var(--saffron-soft);
  border-color: var(--ink);
  box-shadow: inset 0 0 0 1px var(--ink);
}

.amount-input {
  position: relative;
  display: block;
}

.amount-input .input {
  padding-right: 54px;
}

.suffix {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: var(--text-xs);
  font-weight: 700;
  color: var(--ink-soft);
}

.submit {
  margin-top: 20px;
}

.fine {
  margin-top: 12px;
  font-size: var(--text-xs);
  color: var(--ink-muted);
  text-align: center;
}

.status {
  text-align: center;
  display: grid;
  justify-items: center;
  gap: 10px;
}

.status-title {
  font-size: var(--text-xl);
}

.stages {
  list-style: none;
  margin: 8px 0 0;
  padding: 0;
  display: grid;
  gap: 12px;
  text-align: left;
}

.stages li {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--ink-muted);
  transition: color 0.2s;
}

.stages li.current,
.stages li.done {
  color: var(--ink);
}

.dot {
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid var(--line-strong);
  flex: none;
}

.current .dot {
  border-color: var(--saffron);
  border-top-color: transparent;
  animation: spin 0.8s linear infinite;
}

.done .dot {
  background: var(--palm);
  border-color: var(--palm);
  color: #fff;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.ellipsis::after {
  content: '…';
  display: inline-block;
  animation: blink 1.2s steps(2) infinite;
}

@keyframes blink {
  50% {
    opacity: 0.2;
  }
}

.approved-art {
  width: 150px;
  animation: pop 0.6s var(--ease-spring);
}

@keyframes pop {
  from {
    transform: scale(0.6) rotate(-6deg);
    opacity: 0;
  }
}

.stamp {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 14px;
  border-radius: 999px;
  border: 2px solid var(--palm);
  color: var(--palm);
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-size: var(--text-sm);
  transform: rotate(-3deg);
}

.stamp--declined {
  border-color: var(--danger);
  color: var(--danger);
}

.new-balance {
  display: grid;
  min-width: 220px;
  gap: 2px;
  margin-top: 4px;
  padding: 12px 22px;
  border-radius: var(--radius);
  background: var(--saffron-soft);
}

.new-balance span {
  font-size: var(--text-sm);
  color: var(--ink-soft);
}

.new-balance strong {
  font-family: var(--font-display);
  font-size: 2rem;
  line-height: 1.1;
}

.status-actions {
  width: 100%;
  display: grid;
  gap: 10px;
  margin-top: 8px;
}

.declined p {
  color: var(--ink-soft);
}

@media (max-width: 380px) {
  .split {
    grid-template-columns: 1fr;
  }
}
</style>
