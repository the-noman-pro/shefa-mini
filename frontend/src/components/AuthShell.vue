<script setup>
import ProgressJar from './ProgressJar.vue'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>

<template>
  <div class="container shell">
    <div class="card panel">
      <div class="art" aria-hidden="true">
        <ProgressJar :percent="64" :size="70" tag label="" />
      </div>
      <h1>{{ title }}</h1>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
      <slot />
    </div>
    <div class="below"><slot name="below" /></div>
  </div>
</template>

<style scoped>
.shell {
  padding-top: clamp(28px, 6vw, 64px);
}

.card {
  max-width: var(--form-max);
  margin-inline: auto;
  padding: 28px clamp(20px, 5vw, 32px) 30px;
  position: relative;
}

.art {
  position: absolute;
  right: 22px;
  top: -30px;
  transform: rotate(6deg);
}

h1 {
  font-size: var(--text-2xl);
  padding-right: 70px;
}

.subtitle {
  margin-top: 6px;
  margin-bottom: 22px;
  color: var(--ink-soft);
}

.below {
  max-width: var(--form-max);
  margin: 18px auto 0;
  text-align: center;
  color: var(--ink-soft);
}
</style>
