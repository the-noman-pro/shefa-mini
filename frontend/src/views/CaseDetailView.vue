<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import CaseArt from '@/components/art/CaseArt.vue'
import Icon from '@/components/Icon.vue'
import Money from '@/components/Money.vue'
import ProgressJar from '@/components/ProgressJar.vue'
import { api } from '@/lib/api'
import { formatAmount, percentOf, timeAgo, toNumber } from '@/lib/money'
import { useAuthStore } from '@/stores/auth'

const MIN_DONATION = 10
const QUICK_AMOUNTS = [25, 50, 100, 250]

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const item = ref(null)
const loading = ref(true)
const loadError = ref('')
const notFound = ref(false)

const selected = ref(50)
const custom = ref('')
const anonymous = ref(false)
const submitting = ref(false)
const formError = ref('')
const amountError = ref('')

async function load() {
  loading.value = true
  loadError.value = ''
  try {
    item.value = await api.caseDetail(route.params.slug)
  } catch (e) {
    if (e.status === 404) notFound.value = true
    else loadError.value = e.message
  } finally {
    loading.value = false
  }
}

load()
if (auth.isAuthenticated) auth.refresh().catch(() => {})

const pct = computed(() => (item.value ? percentOf(item.value.raised, item.value.goal) : 0))
const remaining = computed(() => toNumber(item.value?.remaining))
const isOpen = computed(() => item.value?.status === 'open')
const paragraphs = computed(() => (item.value?.story || '').split(/\n\s*\n/).filter(Boolean))

const quickAmounts = computed(() => QUICK_AMOUNTS.filter((a) => a <= remaining.value))

const amount = computed(() => {
  if (custom.value !== '') return Number(custom.value)
  return selected.value ?? 0
})

const balance = computed(() => toNumber(auth.balance))
const shortBy = computed(() => {
  if (!auth.isAuthenticated || !(amount.value > 0)) return 0
  return Math.max(0, Math.round((amount.value - balance.value) * 100) / 100)
})

const topUpLink = computed(() => ({
  name: 'top-up',
  query: {
    amount: String(Math.max(MIN_DONATION, Math.ceil(shortBy.value))),
    case: route.params.slug,
  },
}))

watch(custom, (value) => {
  amountError.value = ''
  if (value !== '') selected.value = null
})

function choose(value) {
  selected.value = value
  custom.value = ''
  amountError.value = ''
}

function validate() {
  const text = custom.value === '' ? String(selected.value ?? '') : String(custom.value).trim()
  if (!text) return 'Choose or enter an amount.'
  if (!/^\d+(\.\d{1,2})?$/.test(text)) return 'Enter an amount in SAR, up to two decimals.'
  const value = Number(text)
  if (value < MIN_DONATION) return `The minimum donation is ${MIN_DONATION} SAR.`
  if (value > remaining.value)
    return `This case needs only ${formatAmount(remaining.value)} SAR more.`
  return ''
}

async function give() {
  formError.value = ''
  amountError.value = validate()
  if (amountError.value || shortBy.value > 0) return
  submitting.value = true
  try {
    const receipt = await api.donate(route.params.slug, {
      amount: String(amount.value),
      anonymous: anonymous.value,
    })
    auth.setBalance(receipt.balance_after)
    router.push({ name: 'donation-success', params: { reference: receipt.reference } })
  } catch (e) {
    if (e.fields.amount) amountError.value = e.fields.amount
    else formError.value = e.message
    if (e.code === 'insufficient_balance') auth.refresh().catch(() => {})
    if (e.status === 400 && !e.fields.amount) load()
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="container page">
    <RouterLink to="/" class="back"><Icon name="arrow-left" :size="18" /> All cases</RouterLink>

    <div v-if="loading" class="layout" aria-busy="true">
      <div class="skeleton sk-hero" />
      <div class="skeleton sk-panel" />
    </div>

    <div v-else-if="notFound" class="missing">
      <h1>We could not find this case</h1>
      <p>It may have been closed or the link is mistyped.</p>
      <RouterLink to="/" class="btn btn-quiet">Browse open cases</RouterLink>
    </div>

    <div v-else-if="loadError" class="missing" role="alert">
      <p class="alert alert-error"><Icon name="alert" /> {{ loadError }}</p>
      <button type="button" class="btn btn-quiet" @click="load">Try again</button>
    </div>

    <article v-else-if="item" class="layout">
      <header class="head">
        <div class="hero-art" :class="`tint--${item.category}`">
          <CaseArt :name="item.illustration" :label="`Illustration: ${item.category_label}`" />
        </div>
        <p class="meta">
          <span><Icon :name="item.category" :size="17" /> {{ item.category_label }}</span>
          <span><Icon name="pin" :size="17" /> {{ item.city }}</span>
          <span v-if="item.status === 'funded'" class="funded-tag">
            <Icon name="check" :size="15" /> Fully funded
          </span>
        </p>
        <h1>{{ item.title }}</h1>
        <p class="summary">{{ item.summary }}</p>
      </header>

      <aside class="panel donate" aria-labelledby="donate-title">
        <div class="jar-row">
          <ProgressJar :percent="pct" :size="104" tag />
          <div class="jar-figures">
            <p class="big"><Money :value="item.raised" /></p>
            <p class="muted">
              raised of <span class="num">{{ formatAmount(item.goal) }}</span> SAR goal
            </p>
            <p class="pct num">{{ Math.floor(pct) }}% full</p>
          </div>
        </div>
        <dl class="mini-stats">
          <div>
            <dt>Donors</dt>
            <dd class="num">{{ item.donors_count }}</dd>
          </div>
          <div>
            <dt>Still needed</dt>
            <dd><Money :value="item.remaining" /></dd>
          </div>
        </dl>

        <template v-if="isOpen">
          <h2 id="donate-title" class="panel-title">Give to this case</h2>

          <form v-if="auth.isAuthenticated" novalidate @submit.prevent="give">
            <fieldset class="amounts">
              <legend class="field-label">Amount (SAR)</legend>
              <div class="amount-grid">
                <button
                  v-for="a in quickAmounts"
                  :key="a"
                  type="button"
                  class="amount"
                  :aria-pressed="custom === '' && selected === a"
                  @click="choose(a)"
                >
                  <span class="num">{{ a }}</span><span class="visually-hidden"> SAR</span>
                </button>
              </div>
              <label class="custom">
                <span class="visually-hidden">Other amount in SAR</span>
                <input
                  v-model.trim="custom"
                  class="input"
                  inputmode="decimal"
                  placeholder="Other amount"
                  :aria-invalid="amountError ? 'true' : undefined"
                  aria-describedby="amount-help"
                />
                <span class="suffix" aria-hidden="true">SAR</span>
              </label>
            </fieldset>
            <p v-if="amountError" class="field-error" role="alert">
              <Icon name="alert" :size="16" /> {{ amountError }}
            </p>
            <p id="amount-help" class="field-hint">Minimum {{ MIN_DONATION }} SAR.</p>

            <label class="check">
              <input v-model="anonymous" type="checkbox" />
              <span>Give anonymously <small>(your name is hidden on the case)</small></span>
            </label>

            <div class="wallet-line" :class="{ short: shortBy > 0 }">
              <Icon name="wallet" :size="18" />
              <span>Your wallet: <Money :value="auth.balance" /></span>
              <RouterLink :to="{ name: 'top-up', query: { case: item.slug } }" class="top-up-link"
                >Top up</RouterLink
              >
            </div>

            <div v-if="shortBy > 0" class="short-note" role="status">
              <p>
                You are <strong><Money :value="shortBy" /></strong> short for this gift. Top up
                first, and we will bring you back here.
              </p>
              <RouterLink :to="topUpLink" class="btn btn-palm btn-block">
                Top up <Money :value="Math.max(MIN_DONATION, Math.ceil(shortBy))" /> first
              </RouterLink>
            </div>

            <p v-if="formError" class="alert alert-error" role="alert">
              <Icon name="alert" /> {{ formError }}
            </p>

            <button
              v-if="shortBy <= 0"
              type="submit"
              class="btn btn-block give"
              :disabled="submitting"
            >
              <Icon name="heart" :size="18" />
              <span v-if="submitting">Sending your gift…</span>
              <span v-else-if="amount > 0">Give <Money :value="amount" /></span>
              <span v-else>Give</span>
            </button>
          </form>

          <div v-else class="guest">
            <p>Log in to give from your wallet. It takes a minute to sign up.</p>
            <RouterLink
              :to="{ name: 'login', query: { next: route.fullPath } }"
              class="btn btn-block"
              >Log in to donate</RouterLink
            >
            <p class="muted small">
              New here?
              <RouterLink :to="{ name: 'signup', query: { next: route.fullPath } }"
                >Create an account</RouterLink
              >
            </p>
          </div>
        </template>

        <div v-else class="closed">
          <p>
            <strong>This case is fully funded.</strong> Thank you to everyone who gave. Other
            families still need help.
          </p>
          <RouterLink to="/" class="btn btn-quiet btn-block">See open cases</RouterLink>
        </div>
      </aside>

      <section class="story" aria-labelledby="story-title">
        <h2 id="story-title">The story</h2>
        <p v-for="(para, i) in paragraphs" :key="i">{{ para }}</p>
      </section>

      <section class="recent" aria-labelledby="recent-title">
        <h2 id="recent-title">Recent donations</h2>
        <ul v-if="item.recent_donations.length" class="donations">
          <li v-for="(d, i) in item.recent_donations" :key="i">
            <span class="initial" :class="{ anon: d.name === 'Anonymous' }" aria-hidden="true">
              <Icon v-if="d.name === 'Anonymous'" name="heart" :size="16" />
              <template v-else>{{ d.name[0] }}</template>
            </span>
            <span class="who">
              <strong>{{ d.name }}</strong>
              <small>{{ timeAgo(d.created_at) }}</small>
            </span>
            <Money :value="d.amount" class="how-much" />
          </li>
        </ul>
        <p v-else class="muted">Be the first to give to this case.</p>
      </section>
    </article>
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

.layout {
  display: grid;
  gap: 28px 40px;
  grid-template-columns: minmax(0, 1fr) 380px;
  grid-template-areas:
    'head donate'
    'story donate'
    'recent donate';
  align-items: start;
}

.head {
  grid-area: head;
}
.donate {
  grid-area: donate;
}
.story {
  grid-area: story;
}
.recent {
  grid-area: recent;
}

.hero-art {
  border-radius: var(--radius-lg);
  border: 1.5px solid var(--line);
  background: var(--surface);
  padding: 8px 12%;
  margin-bottom: 18px;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 16px;
  color: var(--ink-soft);
  font-size: var(--text-sm);
  font-weight: 600;
  margin-bottom: 8px;
}

.meta span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.funded-tag {
  color: var(--palm);
}

h1 {
  font-size: var(--text-2xl);
}

.summary {
  margin-top: 10px;
  font-size: var(--text-lg);
  color: var(--ink-soft);
}

.story h2,
.recent h2 {
  font-size: var(--text-xl);
  margin-bottom: 10px;
}

.story p {
  max-width: 65ch;
}

.story p + p {
  margin-top: 14px;
}

.story p:first-of-type::first-letter {
  font-family: var(--font-display);
  float: left;
  font-size: 3.1em;
  line-height: 0.9;
  padding: 4px 8px 0 0;
  color: var(--clay);
  font-weight: 700;
}

.donate {
  position: sticky;
  top: 86px;
  padding: 22px;
}

.jar-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.big {
  font-family: var(--font-display);
  font-weight: 650;
  font-size: 1.8rem;
  line-height: 1.1;
}

.muted {
  color: var(--ink-soft);
  font-size: var(--text-sm);
}

.small {
  font-size: var(--text-sm);
}

.pct {
  display: inline-block;
  margin-top: 6px;
  padding: 2px 10px;
  border-radius: 999px;
  background: var(--saffron-soft);
  font-weight: 700;
  font-size: var(--text-sm);
}

.mini-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin: 18px 0 0;
  border-top: 1.5px dashed var(--line);
  border-bottom: 1.5px dashed var(--line);
}

.mini-stats div {
  padding: 10px 0;
}

.mini-stats div + div {
  border-left: 1.5px dashed var(--line);
  padding-left: 14px;
}

.mini-stats dt {
  font-size: var(--text-xs);
  color: var(--ink-soft);
  font-weight: 600;
}

.mini-stats dd {
  margin: 0;
  font-weight: 700;
  font-size: var(--text-lg);
}

.panel-title {
  font-size: var(--text-lg);
  margin: 18px 0 12px;
}

.amounts {
  border: 0;
  padding: 0;
  margin: 0;
}

.amounts legend {
  margin-bottom: 8px;
}

.amount-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}

.amount {
  min-height: 46px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--line-strong);
  background: var(--surface);
  font-weight: 700;
  cursor: pointer;
  transition:
    background-color 0.15s,
    border-color 0.15s,
    transform 0.15s var(--ease-spring);
}

.amount:hover {
  border-color: var(--ink);
}

.amount[aria-pressed='true'] {
  background: var(--saffron-soft);
  border-color: var(--ink);
  box-shadow: inset 0 0 0 1px var(--ink);
  transform: scale(1.03);
}

.custom {
  position: relative;
  display: block;
  margin-top: 8px;
}

.custom .input {
  padding-right: 52px;
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

.field-error {
  margin-top: 8px;
}

.field-hint {
  margin-top: 6px;
}

.check {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  margin: 14px 0;
  font-size: var(--text-sm);
  cursor: pointer;
}

.check input {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  accent-color: var(--palm);
}

.check small {
  color: var(--ink-soft);
}

.wallet-line {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  background: var(--paper);
  border: 1.5px solid var(--line);
  font-size: var(--text-sm);
  margin-bottom: 14px;
}

.wallet-line.short {
  border-color: #ecc888;
  background: var(--saffron-soft);
}

.top-up-link {
  margin-left: auto;
  font-weight: 700;
}

.short-note {
  display: grid;
  gap: 10px;
  font-size: var(--text-sm);
  margin-bottom: 4px;
}

.give {
  margin-top: 4px;
}

.alert {
  margin-bottom: 12px;
}

.guest,
.closed {
  display: grid;
  gap: 12px;
  margin-top: 14px;
}

.closed {
  margin-top: 18px;
}

.donations {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 2px;
  max-width: 560px;
}

.donations li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1.5px dashed var(--line);
}

.initial {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  flex: none;
  border-radius: 50%;
  border: 1.5px solid var(--ink);
  background: var(--rose-soft);
  font-weight: 700;
  font-family: var(--font-display);
}

.initial.anon {
  background: var(--palm-soft);
  color: var(--palm);
}

.who {
  display: grid;
  line-height: 1.25;
}

.who small {
  color: var(--ink-muted);
  font-size: var(--text-xs);
}

.how-much {
  margin-left: auto;
  font-weight: 700;
}

.missing {
  display: grid;
  gap: 12px;
  justify-items: start;
  padding: 40px 0;
}

.sk-hero {
  height: 360px;
  border-radius: var(--radius-lg);
}

.sk-panel {
  height: 420px;
  border-radius: var(--radius-lg);
}

@media (max-width: 900px) {
  .layout {
    grid-template-columns: minmax(0, 1fr);
    grid-template-areas:
      'head'
      'donate'
      'story'
      'recent';
  }

  .donate {
    position: static;
    max-width: var(--form-max);
  }

  .hero-art {
    padding: 6px 4%;
  }
}
</style>
