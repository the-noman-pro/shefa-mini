<script setup>
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>

<template>
  <a href="#main" class="skip-link">Skip to content</a>
  <AppHeader />
  <main id="main" tabindex="-1">
    <RouterView v-slot="{ Component, route }">
      <Transition name="page" mode="out-in">
        <component :is="Component" :key="route.name === 'cases' ? 'cases' : route.fullPath" />
      </Transition>
    </RouterView>
  </main>
  <AppFooter />
</template>

<style>
.skip-link {
  position: absolute;
  left: 12px;
  top: -60px;
  z-index: 50;
  padding: 10px 14px;
  border-radius: 10px;
  background: var(--ink);
  color: #fff;
  font-weight: 600;
}

.skip-link:focus {
  top: 12px;
  color: #fff;
}

main {
  display: block;
  min-height: 60vh;
  /* clips decorative overflow (confetti) without creating a scroll container, so sticky still works */
  overflow-x: clip;
}

main:focus {
  outline: none;
}
</style>
