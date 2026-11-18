<script setup>
import Inked from './Inked.vue'
</script>

<template>
  <svg viewBox="0 0 200 160" class="empty-art" aria-hidden="true" focusable="false">
    <path
      d="M24 112C12 76 42 30 100 28c54-2 84 22 80 62-4 38-36 52-84 52-40 0-62-8-72-30Z"
      fill="var(--paper-deep)"
    />
    <path
      d="M30 144c40-3 100 2 140-2"
      fill="none"
      stroke="var(--ink)"
      stroke-width="2"
      stroke-linecap="round"
      opacity="0.5"
    />
    <Inked
      d="M80 66h40c0 5 2 8 7 12 9 6 13 14 13 25v26c0 7-6 11-13 11H73c-7 0-13-4-13-11v-26c0-11 4-19 13-25 5-4 7-7 7-12Z"
      fill="#fffaf0"
    />
    <Inked d="M76 52h48v14H76Z" fill="var(--clay)" />
    <path
      d="M70 108c-1 8-1 16 0 22"
      fill="none"
      stroke="#fff"
      stroke-width="4"
      stroke-linecap="round"
    />
    <Inked d="M100 24a9 9 0 1 1 0 .1Z" fill="var(--saffron)" :offset="2" />
    <path d="M100 18v12" stroke="var(--ink)" stroke-width="1.6" stroke-linecap="round" />
    <path
      d="M86 8l2 6M114 8l-2 6M100 40v6"
      fill="none"
      stroke="var(--clay)"
      stroke-width="2"
      stroke-linecap="round"
      class="drop"
    />
  </svg>
</template>

<style scoped>
.empty-art {
  width: 100%;
  height: auto;
}
</style>
