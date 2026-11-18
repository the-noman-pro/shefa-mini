<script setup>
import { computed, nextTick, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import EmptyArt from '@/components/art/EmptyArt.vue'
import WalletArt from '@/components/art/WalletArt.vue'
import Icon from '@/components/Icon.vue'
import Money from '@/components/Money.vue'
import { api } from '@/lib/api'
import { formatDate } from '@/lib/money'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const transactions = ref([])
const nextPage = ref(null)
const loading = ref(true)
const loadingMore = ref(false)
const error = ref('')

const editing = ref(false)
const nameDraft = ref('')
const nameError = ref('')
const savingName = ref(false)
const nameInput = ref(null)

const initials = computed(() =>
  (auth.user?.name || '')
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0].toUpperCase())
    .join(''),
)

const totals = computed(() => {
  let given = 0
  let count = 0
  for (const t of transactions.value) {
    if (t.kind === 'donation') {
      given += -Number(t.amount)
      count += 1
    }
  }
  return { given, count }
})

async function load(page = 1) {
  const data = await api.transactions(page)
  transactions.value = page === 1 ? data.results : [...transactions.value, ...data.results]
  nextPage.value = data.next ? page + 1 : null
}

async function init() {
  loading.value = true
  error.value = ''
  try {
    await Promise.all([auth.refresh(), load(1)])
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
init()

async function more() {
  loadingMore.value = true
  try {
    await load(nextPage.value)
  } catch (e) {
    error.value = e.message
  } finally {
    loadingMore.value = false
  }
}

async function startEdit() {
  nameDraft.value = auth.user?.name || ''
  nameError.value = ''
  editing.value = true
  await nextTick()
  nameInput.value?.focus()
}

async function saveName() {
  nameError.value = ''
  if (nameDraft.value.trim().length < 2) {
    nameError.value = 'Please enter your full name.'
    return
  }
  savingName.value = true
  try {
    await auth.updateName(nameDraft.value.trim())
    editing.value = false
  } catch (e) {
    nameError.value = e.fields.name || e.message
  } finally {
    savingName.value = false
  }
}

async function logout() {
  await auth.logout()
  router.push({ name: 'cases' })
}

const BRAND = { visa: 'Visa', mastercard: 'Mastercard', mada: 'Mada', amex: 'Amex' }
</script>

<template>
  <div class="container page">
    <h1 class="title">Your account</h1>

    <div class="top">
      <section class="panel profile" aria-labelledby="profile-title">
        <h2 id="profile-title" class="visually-hidden">Profile</h2>
        <div class="who">
          <span class="avatar" aria-hidden="true">{{ initials }}</span>
          <div v-if="!editing" class="who-text">
            <p class="name">{{ auth.user?.name }}</p>
            <p class="email">{{ auth.user?.email }}</p>
          </div>
          <form v-else class="edit" novalidate @submit.prevent="saveName">
            <label class="visually-hidden" for="name-edit">Full name</label>
            <input
              id="name-edit"
              ref="nameInput"
              v-model="nameDraft"
              class="input"
              autocomplete="name"
              :aria-invalid="nameError ? 'true' : undefined"
              aria-describedby="name-edit-error"
            />
            <p v-if="nameError" id="name-edit-error" class="field-error">{{ nameError }}</p>
            <div class="edit-actions">
              <button type="submit" class="btn btn-sm btn-palm" :disabled="savingName">Save</button>
              <button type="button" class="btn btn-sm btn-quiet" @click="editing = false">
                Cancel
              </button>
            </div>
          </form>
        </div>
        <dl class="facts">
          <div>
            <dt>Member since</dt>
            <dd>{{ formatDate(auth.user?.date_joined) }}</dd>
          </div>
          <div>
            <dt>Given so far</dt>
            <dd><Money :value="totals.given" /></dd>
          </div>
          <div>
            <dt>Gifts</dt>
            <dd class="num">{{ totals.count }}</dd>
          </div>
        </dl>
        <div class="profile-actions">
          <button v-if="!editing" type="button" class="link-button" @click="startEdit">
            <Icon name="pencil" :size="16" /> Edit name
          </button>
          <button type="button" class="link-button danger" @click="logout">
            <Icon name="logout" :size="16" /> Log out
          </button>
        </div>
      </section>

      <section class="wallet" aria-labelledby="wallet-title">
        <div class="wallet-copy">
          <h2 id="wallet-title">Wallet</h2>
          <p class="balance" aria-live="polite">
            <Money :value="auth.balance" :count-from="0" :duration="1200" />
          </p>
          <p class="wallet-note">Available to give. Top-ups arrive instantly.</p>
          <RouterLink to="/top-up" class="btn wallet-btn"
            ><Icon name="card" :size="18" /> Top up</RouterLink
          >
        </div>
        <div class="wallet-art"><WalletArt /></div>
      </section>
    </div>

    <section class="history" aria-labelledby="history-title">
      <h2 id="history-title">Activity</h2>

      <div v-if="loading" class="rows">
        <div v-for="n in 4" :key="n" class="skeleton" style="height: 64px" />
      </div>

      <p v-else-if="error" class="alert alert-error" role="alert">
        <Icon name="alert" /> {{ error }}
      </p>

      <div v-else-if="!transactions.length" class="empty">
        <div class="empty-art"><EmptyArt /></div>
        <h3>Nothing here yet</h3>
        <p>Your top-ups and gifts will show up here, each with its own reference.</p>
        <RouterLink to="/" class="btn btn-quiet">Find a case</RouterLink>
      </div>

      <ul v-else class="rows">
        <li v-for="t in transactions" :key="t.id" class="row" :class="`row--${t.kind}`">
          <span class="row-icon" aria-hidden="true">
            <Icon :name="t.kind === 'top_up' ? 'arrow-in' : 'heart'" :size="18" />
          </span>
          <span class="row-main">
            <span class="row-title">
              <template v-if="t.kind === 'top_up'">
                Top-up<span v-if="t.card_brand" class="muted">
                  · {{ BRAND[t.card_brand] || t.card_brand }} •••• {{ t.card_last4 }}</span
                >
              </template>
              <template v-else-if="t.case">
                Gift to
                <RouterLink :to="{ name: 'case', params: { slug: t.case.slug } }">{{
                  t.case.title
                }}</RouterLink>
              </template>
              <template v-else>{{ t.description }}</template>
            </span>
            <span class="row-sub">
              <span class="ref">{{ t.reference }}</span> ·
              {{ formatDate(t.created_at, { withTime: true }) }}
            </span>
          </span>
          <span class="row-amount">
            <Money :value="t.amount" sign class="amount" />
            <small>Balance <Money :value="t.balance_after" /></small>
          </span>
        </li>
      </ul>

      <button
        v-if="nextPage"
        type="button"
        class="btn btn-quiet more"
        :disabled="loadingMore"
        @click="more"
      >
        {{ loadingMore ? 'Loading…' : 'Show older activity' }}
      </button>
    </section>
  </div>
</template>

<style scoped>
.page {
  padding-top: clamp(24px, 4vw, 40px);
}

.title {
  font-size: var(--text-2xl);
  margin-bottom: 20px;
}

.top {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 22px;
  align-items: stretch;
}

.profile {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.who {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.avatar {
  display: grid;
  place-items: center;
  width: 56px;
  height: 56px;
  flex: none;
  border-radius: 50%;
  border: 2px solid var(--ink);
  background: var(--palm);
  color: #fff;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.3rem;
  box-shadow: 2px 3px 0 var(--ink);
}

.who-text {
  min-width: 0;
}

.name {
  font-family: var(--font-display);
  font-weight: 650;
  font-size: var(--text-xl);
  line-height: 1.2;
}

.email {
  color: var(--ink-soft);
  font-size: var(--text-sm);
  overflow-wrap: anywhere;
}

.edit {
  flex: 1;
  display: grid;
  gap: 8px;
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.facts {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin: 0;
  border-top: 1.5px dashed var(--line);
  border-bottom: 1.5px dashed var(--line);
}

.facts div {
  padding: 10px 0;
}

.facts div + div {
  padding-left: 12px;
  border-left: 1.5px dashed var(--line);
}

.facts dt {
  font-size: var(--text-xs);
  color: var(--ink-soft);
  font-weight: 600;
}

.facts dd {
  margin: 0;
  font-weight: 700;
}

.profile-actions {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: auto;
}

.profile-actions .link-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.danger {
  color: var(--clay);
}

.wallet {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.9fr);
  align-items: center;
  gap: 8px;
  padding: 24px;
  border-radius: var(--radius-lg);
  border: 2px solid var(--ink);
  background: var(--palm);
  color: #fff8ee;
  box-shadow: 4px 5px 0 var(--ink);
  overflow: hidden;
}

.wallet::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    135deg,
    rgb(255 255 255 / 0.04) 0 2px,
    transparent 2px 14px
  );
  pointer-events: none;
}

.wallet-copy {
  position: relative;
}

.wallet h2 {
  font-size: var(--text-lg);
  font-weight: 500;
  opacity: 0.9;
}

.balance {
  font-family: var(--font-display);
  font-weight: 650;
  font-size: clamp(2rem, 1.4rem + 2.6vw, 2.9rem);
  line-height: 1.1;
  margin: 4px 0 6px;
}

.balance :deep(.currency) {
  color: var(--saffron-soft);
}

.wallet-note {
  font-size: var(--text-sm);
  opacity: 0.85;
  margin-bottom: 16px;
}

.wallet-btn {
  --btn-bg: var(--saffron);
  --btn-fg: var(--ink);
  --btn-hover: var(--honey);
}

.wallet-art {
  position: relative;
  max-width: 230px;
  justify-self: end;
  width: 100%;
}

.history {
  margin-top: 36px;
}

.history h2 {
  font-size: var(--text-xl);
  margin-bottom: 12px;
}

.rows {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 10px;
}

.row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: var(--radius);
  background: var(--surface);
  border: 1.5px solid var(--line);
}

.row-icon {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  flex: none;
  border-radius: 50%;
  border: 1.5px solid var(--ink);
}

.row--top_up .row-icon {
  background: var(--palm-soft);
  color: var(--palm-deep);
}

.row--donation .row-icon {
  background: var(--clay-soft);
  color: var(--clay);
}

.row-main {
  display: grid;
  gap: 2px;
  min-width: 0;
  flex: 1;
}

.row-title {
  font-weight: 600;
}

.muted {
  color: var(--ink-soft);
  font-weight: 500;
}

.row-sub {
  font-size: var(--text-xs);
  color: var(--ink-muted);
}

.ref {
  font-family: var(--font-mono);
}

.row-amount {
  display: grid;
  justify-items: end;
  text-align: right;
}

.amount {
  font-weight: 700;
  font-size: var(--text-lg);
}

.row--top_up .amount {
  color: var(--palm);
}

.row-amount small {
  font-size: var(--text-xs);
  color: var(--ink-muted);
}

.more {
  margin-top: 14px;
}

.empty {
  display: grid;
  justify-items: center;
  text-align: center;
  gap: 10px;
  padding: 28px 16px;
  border-radius: var(--radius-lg);
  border: 1.5px dashed var(--line-strong);
  color: var(--ink-soft);
}

.empty h3 {
  color: var(--ink);
  font-size: var(--text-xl);
}

.empty-art {
  width: 180px;
}

@media (max-width: 860px) {
  .top {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .wallet {
    grid-template-columns: 1fr;
  }
  .wallet-art {
    position: absolute;
    right: -18px;
    bottom: -14px;
    width: 150px;
    opacity: 0.9;
  }
  .row {
    flex-wrap: wrap;
  }
  .row-main {
    flex-basis: calc(100% - 54px);
  }
  .row-amount {
    margin-left: 54px;
    justify-items: start;
    text-align: left;
  }
}
</style>
