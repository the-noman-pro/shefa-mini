<script setup>
import { onMounted, ref, useId } from 'vue'
import Inked from './Inked.vue'
import { prefersReducedMotion } from '@/lib/motion'

// Two hands holding a heart that fills up, then a ring of sparks.
const id = useId()
const filled = ref(false)

onMounted(() => {
  if (prefersReducedMotion()) filled.value = true
  else setTimeout(() => (filled.value = true), 250)
})

const HEART =
  'M140 160c-36-24-56-44-54-68 2-20 24-28 40-18 6 4 11 10 14 16 3-6 8-12 14-16 16-10 38-2 40 18 2 24-18 44-54 68Z'
</script>

<template>
  <svg
    viewBox="0 0 280 230"
    class="scene"
    :class="{ 'scene--filled': filled }"
    aria-hidden="true"
    focusable="false"
  >
    <defs>
      <clipPath :id="`${id}-heart`">
        <path :d="HEART" />
      </clipPath>
    </defs>

    <path
      d="M30 150C14 96 54 30 140 26c80-4 122 30 116 92-6 58-58 84-128 84-58 0-88-14-98-52Z"
      fill="var(--saffron-soft)"
      opacity="0.75"
    />

    <!-- sparks -->
    <g class="sparks" stroke="var(--clay)" stroke-width="3" stroke-linecap="round" fill="none">
      <path d="M140 40v-16" />
      <path d="M96 52l-9-12" />
      <path d="M184 52l9-12" />
      <path d="M70 84l-14-6" />
      <path d="M210 84l14-6" />
    </g>
    <g class="stars">
      <path d="M62 40c1 6 3 8 9 9-6 1-8 3-9 9-1-6-3-8-9-9 6-1 8-3 9-9Z" fill="var(--saffron)" />
      <path d="M222 120c1 5 2 6 7 7-5 1-6 2-7 7-1-5-2-6-7-7 5-1 6-2 7-7Z" fill="var(--palm)" />
      <path d="M232 36c.8 4 2 5 6 6-4 .8-5 2-6 6-.8-4-2-5-6-6 4-.8 5-2 6-6Z" fill="var(--clay)" />
    </g>

    <!-- heart: empty glass, then the fill rising inside it -->
    <path :d="HEART" fill="#fffaf0" />
    <g :clip-path="`url(#${id}-heart)`">
      <g class="fill">
        <path
          d="M60 0c12 0 12-6 24-6s12 6 24 6 12-6 24-6 12 6 24 6 12-6 24-6 12 6 24 6 12-6 24-6 12 6 24 6V120H60Z"
          fill="var(--clay)"
        />
      </g>
    </g>
    <path :d="HEART" fill="none" stroke="var(--ink)" stroke-width="3" stroke-linejoin="round" />
    <path
      d="M106 92c0-8 6-14 14-14"
      fill="none"
      stroke="#fff"
      stroke-width="4.5"
      stroke-linecap="round"
      opacity="0.8"
    />

    <!-- hands -->
    <Inked
      d="M34 214c6-30 12-56 28-74 8-9 18-8 20 2 2 10-2 18 2 26 8 12 28 20 56 22v24Z"
      fill="var(--rose)"
      :width="2.8"
    />
    <Inked
      d="M246 214c-6-30-12-56-28-74-8-9-18-8-20 2-2 10 2 18-2 26-8 12-28 20-56 22v24Z"
      fill="var(--rose)"
      :width="2.8"
    />
    <path
      d="M82 142c8-6 16-4 18 4M198 142c-8-6-16-4-18 4"
      fill="none"
      stroke="var(--ink)"
      stroke-width="2"
      stroke-linecap="round"
    />
    <path
      d="M60 176c6 4 12 6 18 6M220 176c-6 4-12 6-18 6"
      fill="none"
      stroke="var(--ink)"
      stroke-width="1.6"
      stroke-linecap="round"
      opacity="0.6"
    />
    <Inked d="M26 206l114 6v14l-116-2Z" fill="var(--palm)" :width="2.8" />
    <Inked d="M254 206l-114 6v14l116-2Z" fill="var(--palm)" :width="2.8" />
  </svg>
</template>

<style scoped>
.scene {
  width: 100%;
  height: auto;
  overflow: visible;
}

.fill {
  transform: translateY(166px);
  transition: transform 1.8s var(--ease-out);
}

.scene--filled .fill {
  transform: translateY(62px);
}

.sparks path,
.stars path {
  opacity: 0;
  transform-box: fill-box;
  transform-origin: center;
  transform: scale(0.3);
  transition:
    opacity 0.4s ease,
    transform 0.5s var(--ease-spring);
}

.scene--filled .sparks path,
.scene--filled .stars path {
  opacity: 1;
  transform: scale(1);
  transition-delay: 1.4s;
}

.scene--filled .sparks path:nth-child(2),
.scene--filled .stars path:nth-child(2) {
  transition-delay: 1.5s;
}

.scene--filled .sparks path:nth-child(3),
.scene--filled .stars path:nth-child(3) {
  transition-delay: 1.6s;
}

.scene--filled .sparks path:nth-child(4) {
  transition-delay: 1.7s;
}

.scene--filled .sparks path:nth-child(5) {
  transition-delay: 1.8s;
}
</style>
