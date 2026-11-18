<script setup>
import { computed, onBeforeUnmount, onMounted, ref, useId, watch } from 'vue'
import { prefersReducedMotion } from '@/lib/motion'

// A hand-drawn jar that fills to `percent` the first time it scrolls into view.
const props = defineProps({
  percent: { type: Number, default: 0 },
  size: { type: Number, default: 120 },
  tag: { type: Boolean, default: false },
  label: { type: String, default: '' },
})

const id = useId()
const root = ref(null)
const shown = ref(false)
let observer = null

// The liquid can rise from the jar's bottom (y=142) to just under its shoulder (y=46).
const TOP = 46
const BOTTOM = 142
const level = computed(() => {
  const pct = shown.value ? Math.min(100, Math.max(0, props.percent)) : 0
  // A sliver stays visible for tiny percentages so the jar never looks broken.
  const visible = pct > 0 && pct < 3 ? 3 : pct
  return BOTTOM - ((BOTTOM - TOP) * visible) / 100
})

const ariaLabel = computed(
  () => props.label || `${Math.round(Math.min(100, props.percent))} percent of the goal raised`,
)

onMounted(() => {
  if (prefersReducedMotion() || typeof IntersectionObserver === 'undefined') {
    shown.value = true
    return
  }
  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        // Next frame, so the transition from empty actually runs.
        requestAnimationFrame(() => (shown.value = true))
        observer?.disconnect()
      }
    },
    { threshold: 0.35 },
  )
  observer.observe(root.value)
})

watch(
  () => props.percent,
  () => {
    if (!observer) shown.value = true
  },
)

onBeforeUnmount(() => observer?.disconnect())

const BODY =
  'M40 30h40c0 6 2 9 9 14 12 8 17 18 17 32v52c0 9-7 14-16 14H30c-9 0-16-5-16-14V76c0-14 5-24 17-32 7-5 9-8 9-14Z'
</script>

<template>
  <svg
    ref="root"
    class="jar"
    :class="{ 'jar--full': percent >= 100 }"
    :width="size"
    :height="(size * 150) / 120"
    viewBox="0 0 120 150"
    role="img"
    :aria-label="ariaLabel"
  >
    <defs>
      <clipPath :id="`${id}-clip`">
        <path :d="BODY" />
      </clipPath>
    </defs>

    <!-- glass -->
    <path :d="BODY" fill="var(--surface)" transform="translate(2.5 2.5)" opacity="0.9" />
    <path :d="BODY" fill="#fffaf0" />

    <!-- liquid -->
    <g :clip-path="`url(#${id}-clip)`">
      <g class="jar-level" :style="{ transform: `translateY(${level}px)` }">
        <g class="jar-wave">
          <path
            d="M-120 0c15 0 15-5 30-5s15 5 30 5 15-5 30-5 15 5 30 5 15-5 30-5 15 5 30 5 15-5 30-5 15 5 30 5 15-5 30-5 15 5 30 5V120h-240Z"
            fill="var(--honey)"
          />
          <path
            d="M-120 6c15 0 15-4 30-4s15 4 30 4 15-4 30-4 15 4 30 4 15-4 30-4 15 4 30 4 15-4 30-4 15 4 30 4 15-4 30-4 15 4 30 4V120h-240Z"
            fill="var(--saffron)"
          />
        </g>
        <circle class="jar-bubble" cx="44" cy="40" r="3" fill="var(--saffron-soft)" />
        <circle
          class="jar-bubble jar-bubble--late"
          cx="74"
          cy="56"
          r="2.2"
          fill="var(--saffron-soft)"
        />
      </g>
    </g>

    <!-- outline, shine and lid -->
    <path :d="BODY" fill="none" stroke="var(--ink)" stroke-width="2.6" stroke-linejoin="round" />
    <path
      d="M26 70c-2 10-2 34 0 52"
      fill="none"
      stroke="#fff"
      stroke-width="4"
      stroke-linecap="round"
      opacity="0.75"
    />
    <path
      d="M36 10h48a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H36a4 4 0 0 1-4-4V14a4 4 0 0 1 4-4Z"
      fill="var(--clay)"
      transform="translate(2 2)"
    />
    <path
      d="M36 10h48a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H36a4 4 0 0 1-4-4V14a4 4 0 0 1 4-4Z"
      fill="none"
      stroke="var(--ink)"
      stroke-width="2.6"
    />
    <path d="M40 17h40M40 22h40" stroke="var(--ink)" stroke-width="1.4" opacity="0.5" />

    <!-- a paper tag on a string -->
    <g v-if="tag">
      <path d="M86 30c8 4 12 10 12 18" fill="none" stroke="var(--ink)" stroke-width="1.6" />
      <path
        d="M90 48h16l4 6-4 6H90Z"
        fill="var(--paper-deep)"
        stroke="var(--ink)"
        stroke-width="1.8"
        stroke-linejoin="round"
      />
      <path
        d="M98 57.5c-3-2-4.5-3.5-4.5-5a2 2 0 0 1 4.5-.8 2 2 0 0 1 4.5.8c0 1.5-1.5 3-4.5 5Z"
        fill="var(--clay)"
      />
    </g>
  </svg>
</template>

<style scoped>
.jar {
  display: block;
  overflow: visible;
}

.jar-level {
  transition: transform 1.6s var(--ease-out);
  will-change: transform;
}

.jar-wave {
  animation: wave 3.2s linear infinite;
}

@keyframes wave {
  to {
    transform: translateX(60px);
  }
}

.jar-bubble {
  opacity: 0;
  animation: bubble 3.6s ease-in infinite 1.6s;
}

.jar-bubble--late {
  animation-delay: 2.8s;
}

@keyframes bubble {
  0% {
    opacity: 0;
    transform: translateY(40px);
  }
  20% {
    opacity: 0.9;
  }
  100% {
    opacity: 0;
    transform: translateY(-4px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .jar-wave,
  .jar-bubble {
    animation: none;
  }
}
</style>
