import { onBeforeUnmount, ref, watch } from 'vue'
import { prefersReducedMotion } from '@/lib/motion'

/**
 * A number that eases from its previous value to `source()` whenever the source changes.
 * `from` sets the starting point of the first run (defaults to the target, i.e. no animation).
 */
export function useCountUp(source, { duration = 1100, from } = {}) {
  const initial = Number(source()) || 0
  const display = ref(from ?? initial)
  let frame = 0

  function run(target) {
    cancelAnimationFrame(frame)
    const start = display.value
    if (prefersReducedMotion() || start === target) {
      display.value = target
      return
    }
    const began = performance.now()
    const tick = (now) => {
      const t = Math.min(1, (now - began) / duration)
      const eased = 1 - Math.pow(1 - t, 3)
      display.value = start + (target - start) * eased
      if (t < 1) frame = requestAnimationFrame(tick)
      else display.value = target
    }
    frame = requestAnimationFrame(tick)
  }

  watch(
    () => Number(source()) || 0,
    (target) => run(target),
    { immediate: from !== undefined },
  )

  onBeforeUnmount(() => cancelAnimationFrame(frame))
  return display
}
