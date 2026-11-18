<script setup>
// Small line icons drawn for this app (24px grid, round strokes). Decorative unless a label is given.
const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 20 },
  label: { type: String, default: '' },
  strokeWidth: { type: [Number, String], default: 1.8 },
})

const PATHS = {
  all: ['M5 5h5v5H5z', 'M14 5h5v5h-5z', 'M5 14h5v5H5z', 'M14 14h5v5h-5z'],
  medical: [
    'M12 20s-7-4.3-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.7-7 10-7 10Z',
    'M7.5 11.5h2.5l1.2-2 1.8 4 1.2-2h2.3',
  ],
  education: [
    'M3.5 6.5C6 5.5 9 5.6 12 7.2c3-1.6 6-1.7 8.5-.7v12c-2.5-1-5.5-.9-8.5.7-3-1.6-6-1.7-8.5-.7z',
    'M12 7.2v12',
  ],
  housing: ['M4 11.5 12 5l8 6.5', 'M6 10v9.5h12V10', 'M10 19.5v-5h4v5'],
  food: [
    'M3.5 10.5h17l-1.8 8.2a1.5 1.5 0 0 1-1.5 1.3H6.8a1.5 1.5 0 0 1-1.5-1.3z',
    'M7 10.5 10 4.5',
    'M17 10.5 14 4.5',
    'M9 14v3M12 14v3M15 14v3',
  ],
  water: [
    'M12 3.5s-6 6.6-6 10.6a6 6 0 0 0 12 0c0-4-6-10.6-6-10.6Z',
    'M9.2 14.5a2.9 2.9 0 0 0 2.6 2.8',
  ],
  debt: [
    'M3.5 14.5c2.5-.2 4.2.6 5.6 1.8h3.4a1.5 1.5 0 0 1 0 3H8.6',
    'M3.5 20.5h5.8l6.7-2.8 4-2.1a1.4 1.4 0 0 0-1.3-2.4l-3.9 1.6',
    'M15 8.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z',
  ],
  wallet: [
    'M4 7.5A2.5 2.5 0 0 1 6.5 5H18v3',
    'M4 7.5v10A2.5 2.5 0 0 0 6.5 20H20V8H6.5A2.5 2.5 0 0 1 4 5.5',
    'M16 14h.01',
  ],
  heart: ['M12 20s-7-4.3-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.7-7 10-7 10Z'],
  'arrow-left': ['M19 12H5', 'M11 6l-6 6 6 6'],
  'arrow-right': ['M5 12h14', 'M13 6l6 6-6 6'],
  'arrow-in': ['M12 4v12', 'M7 11l5 5 5-5', 'M5 20h14'],
  check: ['M5 12.5l4.5 4.5L19 7.5'],
  x: ['M6 6l12 12', 'M18 6 6 18'],
  alert: ['M12 4 2.8 19.5h18.4z', 'M12 10v4.5', 'M12 17.2h.01'],
  info: ['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z', 'M12 11v5.5', 'M12 7.8h.01'],
  lock: ['M6.5 10.5h11v9h-11z', 'M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5'],
  eye: [
    'M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z',
    'M12 14.8a2.8 2.8 0 1 0 0-5.6 2.8 2.8 0 0 0 0 5.6Z',
  ],
  'eye-off': [
    'M4 4l16 16',
    'M10.2 6c.6-.3 1.2-.5 1.8-.5 6 0 9.5 6.5 9.5 6.5a17 17 0 0 1-2.6 3.3',
    'M6.6 7.4C4 9.2 2.5 12 2.5 12s3.5 6.5 9.5 6.5c1.6 0 3-.5 4.2-1.1',
  ],
  share: [
    'M18 8.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z',
    'M6 14.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z',
    'M18 20.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z',
    'M8.2 10.8l7.6-3.6M8.2 13.2l7.6 3.6',
  ],
  copy: ['M9 9h10.5v10.5H9z', 'M15 9V4.5H4.5V15H9'],
  user: ['M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z', 'M4.5 20.5c1-3.5 4-5.5 7.5-5.5s6.5 2 7.5 5.5'],
  pin: [
    'M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11Z',
    'M12 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z',
  ],
  people: [
    'M9 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z',
    'M2.5 20c.8-3.2 3.3-5 6.5-5s5.7 1.8 6.5 5',
    'M16 4.3a3.5 3.5 0 0 1 0 6.4',
    'M18.5 15.2c1.5.8 2.6 2.4 3 4.8',
  ],
  pencil: ['M4 20l1-4.5L15.5 5a2 2 0 0 1 3 0l.5.5a2 2 0 0 1 0 3L8.5 19z', 'M13.5 7l3.5 3.5'],
  logout: ['M14 4.5h4.5v15H14', 'M10 8l-4 4 4 4', 'M6 12h10'],
  sparkle: [
    'M12 3.5c.6 4.4 2.1 5.9 6.5 6.5-4.4.6-5.9 2.1-6.5 6.5-.6-4.4-2.1-5.9-6.5-6.5 4.4-.6 5.9-2.1 6.5-6.5Z',
  ],
  card: ['M3 6.5h18v11H3z', 'M3 10h18', 'M6.5 14.5h4'],
  receipt: ['M6 3.5h12v17l-2-1.4-2 1.4-2-1.4-2 1.4-2-1.4-2 1.4z', 'M9 8h6M9 11.5h6M9 15h3.5'],
}

const paths = () => PATHS[props.name] || []
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    :stroke-width="strokeWidth"
    stroke-linecap="round"
    stroke-linejoin="round"
    :role="label ? 'img' : undefined"
    :aria-label="label || undefined"
    :aria-hidden="label ? undefined : 'true'"
    focusable="false"
    class="icon"
  >
    <path v-for="(d, i) in paths()" :key="i" :d="d" />
  </svg>
</template>

<style scoped>
.icon {
  flex: none;
  display: inline-block;
  vertical-align: middle;
}
</style>
