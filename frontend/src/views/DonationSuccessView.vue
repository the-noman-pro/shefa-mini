<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import Celebration from '@/components/Celebration.vue'
import Icon from '@/components/Icon.vue'
import Money from '@/components/Money.vue'
import SuccessScene from '@/components/art/SuccessScene.vue'
import { api } from '@/lib/api'
import { formatDate, percentOf } from '@/lib/money'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()

const receipt = ref(null)
const error = ref('')
const copied = ref('')

async function load() {
  try {
    receipt.value = await api.receipt(route.params.reference)
  } catch (e) {
    error.value = e.status === 404 ? 'We could not find this receipt.' : e.message
  }
}
load()

const pct = computed(() =>
  receipt.value ? Math.floor(percentOf(receipt.value.case.raised, receipt.value.case.goal)) : 0,
)
const caseUrl = computed(() =>
  receipt.value ? `${window.location.origin}/cases/${receipt.value.case.slug}` : '',
)

async function copy(text, what) {
  try {
    await navigator.clipboard.writeText(text)
    copied.value = what
    setTimeout(() => (copied.value = ''), 2200)
  } catch {
    copied.value = ''
  }
}

async function share() {
  const data = {
    title: receipt.value.case.title,
    text: `I just gave to "${receipt.value.case.title}" on Shefa mini. Every bit helps.`,
    url: caseUrl.value,
  }
  if (navigator.share) {
    try {
      await navigator.share(data)
      return
    } catch (e) {
      if (e?.name === 'AbortError') return
    }
  }
  copy(caseUrl.value, 'link')
}
</script>

<template>
  <div class="container page">
    <div v-if="error" class="center" role="alert">
      <p class="alert alert-error"><Icon name="alert" /> {{ error }}</p>
      <RouterLink to="/account" class="btn btn-quiet">See your donations</RouterLink>
    </div>

    <div v-else-if="!receipt" class="center" aria-busy="true">
      <div class="skeleton" style="width: 260px; height: 220px" />
    </div>

    <div v-else class="success">
      <div class="scene-wrap">
        <SuccessScene />
        <Celebration />
      </div>

      <h1>Thank you, {{ auth.firstName || 'friend' }}.</h1>
      <p class="lede">
        Your <strong><Money :value="receipt.amount" /></strong> is on its way to
        <RouterLink :to="{ name: 'case', params: { slug: receipt.case.slug } }">{{
          receipt.case.title
        }}</RouterLink>. The jar is now <strong class="num">{{ pct }}%</strong> full.
      </p>

      <section class="ticket" aria-labelledby="receipt-title">
        <h2 id="receipt-title" class="ticket-title"><Icon name="receipt" :size="20" /> Receipt</h2>
        <dl>
          <div class="row">
            <dt>Reference</dt>
            <dd>
              <span class="ref">{{ receipt.reference }}</span>
              <button
                type="button"
                class="icon-btn"
                :aria-label="copied === 'ref' ? 'Reference copied' : 'Copy reference'"
                @click="copy(receipt.reference, 'ref')"
              >
                <Icon :name="copied === 'ref' ? 'check' : 'copy'" :size="17" />
              </button>
            </dd>
          </div>
          <div class="row">
            <dt>Amount</dt>
            <dd><Money :value="receipt.amount" /></dd>
          </div>
          <div class="row">
            <dt>Case</dt>
            <dd class="case-name">{{ receipt.case.title }}, {{ receipt.case.city }}</dd>
          </div>
          <div class="row">
            <dt>Shown as</dt>
            <dd>{{ receipt.anonymous ? 'Anonymous' : receipt.donor_name }}</dd>
          </div>
          <div class="row">
            <dt>Date</dt>
            <dd>{{ formatDate(receipt.created_at, { withTime: true }) }}</dd>
          </div>
        </dl>
        <div class="ticket-foot">
          <span>Wallet balance now</span>
          <strong><Money :value="receipt.balance_after" /></strong>
        </div>
      </section>

      <div class="actions">
        <button type="button" class="btn" @click="share">
          <Icon name="share" :size="18" /> Share this case
        </button>
        <RouterLink
          :to="{ name: 'case', params: { slug: receipt.case.slug } }"
          class="btn btn-quiet"
        >
          Back to the case
        </RouterLink>
      </div>
      <p class="more">
        <RouterLink to="/">Find another case <Icon name="arrow-right" :size="16" /></RouterLink>
      </p>
      <p class="visually-hidden" role="status">{{ copied ? 'Copied to clipboard' : '' }}</p>
      <Transition name="toast">
        <p v-if="copied === 'link'" class="toast">Link copied. Paste it anywhere to share.</p>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding-top: 24px;
}

.center {
  display: grid;
  justify-items: center;
  gap: 14px;
  padding: 60px 0;
}

.success {
  max-width: 560px;
  margin-inline: auto;
  text-align: center;
  display: grid;
  justify-items: center;
}

.scene-wrap {
  position: relative;
  width: min(300px, 82vw);
}

h1 {
  margin-top: 8px;
  font-size: var(--text-3xl);
}

.lede {
  margin-top: 10px;
  font-size: var(--text-lg);
  color: var(--ink-soft);
  max-width: 46ch;
}

.ticket {
  position: relative;
  width: 100%;
  max-width: 460px;
  margin-top: 26px;
  text-align: left;
  background: var(--surface);
  border: 1.5px solid var(--line-strong);
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  padding: 18px 20px 0;
}

.ticket::before,
.ticket::after {
  content: '';
  position: absolute;
  bottom: 54px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--paper);
  border: 1.5px solid var(--line-strong);
}

.ticket::before {
  left: -12px;
  clip-path: inset(0 0 0 50%);
}

.ticket::after {
  right: -12px;
  clip-path: inset(0 50% 0 0);
}

.ticket-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: var(--text-lg);
  margin-bottom: 8px;
}

dl {
  margin: 0;
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 9px 0;
  border-bottom: 1px solid var(--line);
  font-size: var(--text-sm);
}

.row:last-child {
  border-bottom: 0;
}

dt {
  color: var(--ink-soft);
}

dd {
  margin: 0;
  font-weight: 600;
  text-align: right;
  display: flex;
  align-items: center;
  gap: 6px;
}

.case-name {
  max-width: 64%;
}

.ref {
  font-family: var(--font-mono);
  letter-spacing: 0.04em;
}

.icon-btn {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1.5px solid var(--line-strong);
  background: var(--paper);
  cursor: pointer;
}

.icon-btn:hover {
  border-color: var(--ink);
}

.ticket-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px -20px 0;
  padding: 14px 20px;
  border-top: 2px dashed var(--line-strong);
  background: var(--saffron-soft);
  border-radius: 0 0 var(--radius) var(--radius);
  font-size: var(--text-sm);
}

.ticket-foot strong {
  font-size: var(--text-lg);
}

.actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 26px;
}

.more {
  margin-top: 16px;
}

.more a {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}

.toast {
  position: fixed;
  left: 50%;
  bottom: 24px;
  transform: translateX(-50%);
  padding: 10px 16px;
  border-radius: 999px;
  background: var(--ink);
  color: var(--paper);
  font-size: var(--text-sm);
  font-weight: 600;
  z-index: 30;
}

.toast-enter-active,
.toast-leave-active {
  transition:
    opacity 0.2s,
    transform 0.2s;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 8px);
}
</style>
