<script setup>
import { computed } from 'vue'
import { formatAmount } from '@/lib/money'

const cents = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
import { useCountUp } from '@/composables/useCountUp'

// An amount with a small "SAR" label. `countFrom` animates from that value to `value` on mount.
const props = defineProps({
  value: { type: [String, Number], required: true },
  countFrom: { type: [String, Number], default: undefined },
  sign: { type: Boolean, default: false },
  duration: { type: Number, default: 1100 },
})

const animated = useCountUp(() => props.value, {
  duration: props.duration,
  from: props.countFrom !== undefined ? Number(props.countFrom) : undefined,
})

const text = computed(() => {
  const target = Number(props.value) || 0
  const n = props.countFrom !== undefined ? animated.value : target
  // While counting, keep the final value's precision so the width does not jump.
  const targetHasCents = Math.round(target * 100) % 100 !== 0
  const rounded = targetHasCents ? Math.round(n * 100) / 100 : Math.round(n)
  const body = targetHasCents ? cents.format(Math.abs(rounded)) : formatAmount(Math.abs(rounded))
  if (props.sign) return `${rounded < 0 ? '−' : '+'}${body}`
  return rounded < 0 ? `−${body}` : body
})
</script>

<template>
  <span class="money num"
    >{{ text }}<span class="currency" aria-hidden="true">SAR</span
    ><span class="visually-hidden"> Saudi riyals</span></span
  >
</template>

<style scoped>
.money {
  white-space: nowrap;
}
</style>
