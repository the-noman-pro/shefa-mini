<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CaseCard from '@/components/CaseCard.vue'
import EmptyArt from '@/components/art/EmptyArt.vue'
import Icon from '@/components/Icon.vue'
import { api } from '@/lib/api'
import { formatAmount } from '@/lib/money'

const route = useRoute()
const router = useRouter()

const cases = ref([])
const summary = ref(null)
const loading = ref(true)
const error = ref('')

const category = computed(() =>
  typeof route.query.category === 'string' ? route.query.category : '',
)

const chips = computed(() => {
  const list = summary.value?.categories ?? []
  const total = list.reduce((sum, c) => sum + c.count, 0)
  return [{ key: '', label: 'All cases', count: total }, ...list]
})

async function loadSummary() {
  try {
    summary.value = await api.caseSummary()
  } catch {
    summary.value = null
  }
}

async function loadCases() {
  loading.value = true
  error.value = ''
  try {
    cases.value = await api.cases({ category: category.value })
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function pick(key) {
  router.replace({ query: key ? { category: key } : {} })
}

loadSummary()
watch(category, loadCases, { immediate: true })
</script>

<template>
  <div class="container page">
    <section class="intro" aria-labelledby="intro-title">
      <div class="intro-copy">
        <p class="kicker">Give from your wallet, in a few taps</p>
        <h1 id="intro-title">Small gifts, walked to <span class="underline">real doors</span>.</h1>
        <p class="lede">
          Top up once, then give to the cases that move you. Every riyal shows up in the case's jar
          the moment you give.
        </p>
      </div>
      <dl v-if="summary" class="stats">
        <div class="stat">
          <dt>Raised so far</dt>
          <dd>
            <span class="num">{{ formatAmount(summary.raised) }}</span><span class="currency"
              >SAR</span
            >
          </dd>
        </div>
        <div class="stat">
          <dt>Donors</dt>
          <dd class="num">{{ summary.donors.toLocaleString('en-US') }}</dd>
        </div>
        <div class="stat">
          <dt>Cases funded</dt>
          <dd class="num">{{ summary.funded }}</dd>
        </div>
      </dl>
    </section>

    <div class="filters" role="group" aria-label="Filter by category">
      <button
        v-for="chip in chips"
        :key="chip.key"
        type="button"
        class="chip"
        :aria-pressed="category === chip.key"
        @click="pick(chip.key)"
      >
        <Icon :name="chip.key || 'all'" :size="17" />
        {{ chip.label }}
        <span class="chip-count num">{{ chip.count }}</span>
      </button>
    </div>

    <div v-if="loading" class="grid" aria-busy="true" aria-label="Loading cases">
      <div v-for="n in 6" :key="n" class="skeleton-card">
        <div class="skeleton sk-art" />
        <div class="skeleton sk-line" />
        <div class="skeleton sk-line short" />
      </div>
    </div>

    <div v-else-if="error" class="state" role="alert">
      <p class="alert alert-error"><Icon name="alert" /> {{ error }}</p>
      <button type="button" class="btn btn-quiet" @click="loadCases">Try again</button>
    </div>

    <div v-else-if="!cases.length" class="state">
      <div class="state-art"><EmptyArt /></div>
      <h2>No cases here right now</h2>
      <p>New cases are added every week. Have a look at the other categories meanwhile.</p>
      <button type="button" class="btn btn-quiet" @click="pick('')">See all cases</button>
    </div>

    <TransitionGroup v-else tag="div" name="cards" class="grid">
      <CaseCard
        v-for="(item, index) in cases"
        :key="item.id"
        :item="item"
        :style="{ '--i': index }"
      />
    </TransitionGroup>
  </div>
</template>

<style scoped>
.page {
  padding-top: clamp(24px, 4vw, 44px);
}

.intro {
  display: grid;
  gap: 24px;
  align-items: end;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
  padding-bottom: 28px;
  border-bottom: 1.5px dashed var(--line-strong);
}

.kicker {
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--clay);
  letter-spacing: 0.02em;
  margin-bottom: 8px;
}

h1 {
  font-size: var(--text-3xl);
  max-width: 17ch;
}

.underline {
  position: relative;
  isolation: isolate;
  white-space: nowrap;
}

.underline::after {
  content: '';
  position: absolute;
  left: -2%;
  right: -2%;
  bottom: -0.08em;
  height: 0.34em;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 14' preserveAspectRatio='none'%3E%3Cpath d='M3 9c40-6 90-7 194-3' fill='none' stroke='%23e8a33d' stroke-width='5' stroke-linecap='round'/%3E%3C/svg%3E")
    center / 100% 100% no-repeat;
  z-index: -1;
}

.lede {
  margin-top: 12px;
  color: var(--ink-soft);
  font-size: var(--text-lg);
  max-width: 50ch;
}

.stats {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr) minmax(0, 1fr);
  gap: 10px;
  margin: 0;
}

.stat {
  padding: 14px 14px 12px;
  border-radius: var(--radius);
  background: var(--surface);
  border: 1.5px solid var(--line);
}

.stat:nth-child(1) {
  background: var(--saffron-soft);
  border-color: #ecc888;
}

.stat dt {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--ink-soft);
}

.stat dd {
  margin: 2px 0 0;
  font-family: var(--font-display);
  font-weight: 650;
  font-size: clamp(1.2rem, 1rem + 1vw, 1.55rem);
  white-space: nowrap;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 24px 0 20px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 40px;
  padding: 6px 12px 6px 10px;
  border-radius: 999px;
  border: 1.5px solid var(--line-strong);
  background: var(--surface);
  font-weight: 600;
  font-size: var(--text-sm);
  cursor: pointer;
  transition:
    background-color 0.15s,
    border-color 0.15s;
}

.chip:hover {
  border-color: var(--ink);
}

.chip[aria-pressed='true'] {
  background: var(--ink);
  border-color: var(--ink);
  color: var(--paper);
}

.chip-count {
  font-size: var(--text-xs);
  padding: 1px 7px;
  border-radius: 999px;
  background: var(--paper-deep);
  color: var(--ink-soft);
}

.chip[aria-pressed='true'] .chip-count {
  background: rgb(255 255 255 / 0.18);
  color: var(--paper);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
  gap: 22px;
}

.cards-enter-active {
  transition:
    opacity 0.45s var(--ease-out),
    transform 0.45s var(--ease-out);
  transition-delay: calc(var(--i) * 60ms);
}

.cards-enter-from {
  opacity: 0;
  transform: translateY(14px);
}

.skeleton-card {
  border-radius: var(--radius-lg);
  border: 1.5px solid var(--line);
  background: var(--surface);
  padding: 16px;
  display: grid;
  gap: 12px;
}

.sk-art {
  aspect-ratio: 240 / 150;
}

.sk-line {
  height: 18px;
}

.sk-line.short {
  width: 60%;
}

.state {
  display: grid;
  justify-items: center;
  text-align: center;
  gap: 12px;
  padding: 40px 0;
  color: var(--ink-soft);
}

.state h2 {
  color: var(--ink);
  font-size: var(--text-xl);
}

.state-art {
  width: 200px;
}

@media (max-width: 820px) {
  .intro {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .stats {
    grid-template-columns: 1fr 1fr;
  }
  .stat:first-child {
    grid-column: 1 / -1;
  }
}
</style>
