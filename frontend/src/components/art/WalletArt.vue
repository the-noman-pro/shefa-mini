<script setup>
import Inked from './Inked.vue'
</script>

<template>
  <svg viewBox="0 0 200 140" class="wallet-art" aria-hidden="true" focusable="false">
    <path
      d="M18 96C8 64 34 22 94 18c56-4 92 14 90 56-2 40-40 52-90 52-40 0-68-8-76-30Z"
      fill="rgb(255 255 255 / 0.12)"
    />
    <Inked d="M50 40l8-20 92 10-4 12" fill="var(--saffron)" />
    <path d="M70 26l50 5" stroke="var(--ink)" stroke-width="1.6" stroke-linecap="round" />
    <Inked
      d="M32 52c0-8 6-12 14-12h110c8 0 14 4 14 12v58c0 8-6 12-14 12H46c-8 0-14-4-14-12Z"
      fill="var(--palm-deep)"
      stroke="var(--ink)"
    />
    <path
      d="M42 52v54c0 4 2 6 6 6h104"
      fill="none"
      stroke="var(--saffron-soft)"
      stroke-width="1.6"
      stroke-dasharray="4 5"
      stroke-linecap="round"
    />
    <Inked d="M140 66h36v30h-36c-6 0-10-4-10-10v-10c0-6 4-10 10-10Z" fill="var(--clay)" />
    <path
      d="M150 86.5c-4-2.6-6-4.6-6-6.6a2.8 2.8 0 0 1 6-1.1 2.8 2.8 0 0 1 6 1.1c0 2-2 4-6 6.6Z"
      fill="var(--saffron-soft)"
    />
    <Inked d="M30 120a10 10 0 1 1 0 .1Z" fill="var(--honey)" :offset="2" />
    <Inked d="M50 128a8 8 0 1 1 0 .1Z" fill="var(--saffron)" :offset="2" />
  </svg>
</template>

<style scoped>
.wallet-art {
  width: 100%;
  height: auto;
}
</style>
