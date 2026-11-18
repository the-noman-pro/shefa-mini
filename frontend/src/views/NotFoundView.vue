<script setup>
import { RouterLink } from 'vue-router'
import EmptyArt from '@/components/art/EmptyArt.vue'
</script>

<template>
  <div class="container wrap">
    <div class="art"><EmptyArt /></div>
    <h1>This page is empty</h1>
    <p>The link may be old or mistyped. The cases are still here.</p>
    <RouterLink to="/" class="btn">Browse cases</RouterLink>
  </div>
</template>

<style scoped>
.wrap {
  display: grid;
  justify-items: center;
  text-align: center;
  gap: 12px;
  padding-top: 48px;
}

.art {
  width: 200px;
}

h1 {
  font-size: var(--text-2xl);
}

p {
  color: var(--ink-soft);
}
</style>
