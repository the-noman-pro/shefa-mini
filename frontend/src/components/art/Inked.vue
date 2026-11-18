<script setup>
// One hand-printed shape: a flat colour block slightly off-register, with the ink outline on top.
defineProps({
  d: { type: String, required: true },
  fill: { type: String, default: 'none' },
  offset: { type: Number, default: 2.5 },
  stroke: { type: String, default: 'var(--ink)' },
  width: { type: Number, default: 2.4 },
})
</script>

<template>
  <g>
    <path
      v-if="fill !== 'none'"
      :d="d"
      :fill="fill"
      :transform="`translate(${offset} ${offset})`"
    />
    <path
      :d="d"
      fill="none"
      :stroke="stroke"
      :stroke-width="width"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </g>
</template>
