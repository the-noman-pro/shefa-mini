<script setup>
import { onMounted, ref } from 'vue'
import { prefersReducedMotion } from '@/lib/motion'

// A one-off burst of paper pieces (petals, hearts, dots) from the centre of its container.
const pieces = ref([])
const COLOURS = ['var(--clay)', 'var(--saffron)', 'var(--palm)', 'var(--rose)', 'var(--sky)']
const SHAPES = ['petal', 'dot', 'heart', 'dash']

onMounted(() => {
  if (prefersReducedMotion()) return
  pieces.value = Array.from({ length: 34 }, (_, i) => {
    const angle = (Math.PI * 2 * i) / 34 + Math.random() * 0.4
    const distance = 110 + Math.random() * 130
    return {
      id: i,
      shape: SHAPES[i % SHAPES.length],
      colour: COLOURS[i % COLOURS.length],
      x: Math.cos(angle) * distance,
      y: Math.sin(angle) * distance * 0.75 - 40,
      rotate: Math.round(Math.random() * 540 - 270),
      delay: 1.2 + Math.random() * 0.35,
      size: 8 + Math.random() * 8,
    }
  })
})
</script>

<template>
  <div class="burst" aria-hidden="true">
    <span
      v-for="p in pieces"
      :key="p.id"
      class="piece"
      :class="`piece--${p.shape}`"
      :style="{
        '--x': `${p.x}px`,
        '--y': `${p.y}px`,
        '--r': `${p.rotate}deg`,
        '--c': p.colour,
        '--s': `${p.size}px`,
        animationDelay: `${p.delay}s`,
      }"
    />
  </div>
</template>

<style scoped>
.burst {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: visible;
}

.piece {
  position: absolute;
  left: 50%;
  top: 46%;
  width: var(--s);
  height: var(--s);
  background: var(--c);
  opacity: 0;
  animation: fly 1.6s var(--ease-out) forwards;
}

.piece--petal {
  border-radius: 0 70% 0 70%;
}

.piece--dot {
  border-radius: 50%;
  width: calc(var(--s) * 0.7);
  height: calc(var(--s) * 0.7);
}

.piece--dash {
  height: 4px;
  width: calc(var(--s) * 1.4);
  border-radius: 4px;
}

.piece--heart {
  background: none;
}

.piece--heart::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--c);
  clip-path: path('M6 11C2 8.4 0 6.4 0 4A3 3 0 0 1 6 2.4 3 3 0 0 1 12 4C12 6.4 10 8.4 6 11Z');
}

@keyframes fly {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.4) rotate(0deg);
  }
  12% {
    opacity: 1;
  }
  80% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y) + 60px)) scale(1)
      rotate(var(--r));
  }
}
</style>
