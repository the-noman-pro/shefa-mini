<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import LogoMark from './art/LogoMark.vue'
import Icon from './Icon.vue'
import Money from './Money.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const initials = computed(() =>
  (auth.user?.name || '')
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join(''),
)
</script>

<template>
  <header class="site-header">
    <div class="container bar">
      <RouterLink to="/" class="logo" aria-label="Shefa mini, all cases">
        <LogoMark />
        <span class="logo-text">Shefa <em>mini</em></span>
      </RouterLink>

      <nav class="nav" aria-label="Main">
        <RouterLink to="/" class="nav-link nav-cases">Cases</RouterLink>
        <template v-if="auth.isAuthenticated">
          <RouterLink to="/account" class="wallet-chip" aria-label="Your wallet balance">
            <Icon name="wallet" :size="18" />
            <Money :value="auth.balance" />
          </RouterLink>
          <RouterLink to="/account" class="avatar" :title="auth.user?.name || 'Account'">
            <span aria-hidden="true">{{ initials || '·' }}</span>
            <span class="visually-hidden">Your account</span>
          </RouterLink>
        </template>
        <template v-else>
          <RouterLink to="/login" class="nav-link">Log in</RouterLink>
          <RouterLink to="/signup" class="btn btn-sm">Sign up</RouterLink>
        </template>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgb(251 245 234 / 0.92);
  backdrop-filter: blur(8px);
  border-bottom: 1.5px solid var(--line);
}

.bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-height: 66px;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--ink);
  text-decoration: none;
}

.logo-text {
  font-family: var(--font-display);
  font-weight: 650;
  font-size: 1.3rem;
  letter-spacing: -0.01em;
}

.logo-text em {
  font-style: italic;
  font-weight: 400;
  color: var(--clay);
}

.nav {
  display: flex;
  align-items: center;
  gap: clamp(8px, 2vw, 18px);
}

.nav-link {
  color: var(--ink);
  font-weight: 600;
  text-decoration: none;
  padding: 6px 2px;
  border-bottom: 2px solid transparent;
}

.nav-link:hover {
  color: var(--ink);
  border-bottom-color: var(--saffron);
}

.nav-link.router-link-exact-active {
  border-bottom-color: var(--clay);
}

.wallet-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1.5px solid var(--ink);
  background: var(--saffron-soft);
  color: var(--ink);
  font-weight: 700;
  font-size: var(--text-sm);
  text-decoration: none;
}

.wallet-chip:hover {
  color: var(--ink);
  background: var(--honey);
}

.avatar {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1.5px solid var(--ink);
  background: var(--palm);
  color: #fff;
  font-weight: 700;
  font-size: 0.85rem;
  text-decoration: none;
}

.avatar:hover {
  color: #fff;
  background: var(--palm-deep);
}

@media (max-width: 420px) {
  .logo-text {
    font-size: 1.12rem;
  }
  .nav-cases {
    display: none;
  }
}
</style>
