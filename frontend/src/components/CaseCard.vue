<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import CaseArt from './art/CaseArt.vue'
import Icon from './Icon.vue'
import Money from './Money.vue'
import ProgressJar from './ProgressJar.vue'
import { percentOf } from '@/lib/money'

const props = defineProps({
  item: { type: Object, required: true },
})

const pct = computed(() => percentOf(props.item.raised, props.item.goal))
const funded = computed(() => props.item.status === 'funded')
</script>

<template>
  <article class="case-card" :class="{ 'case-card--funded': funded }">
    <div class="art">
      <CaseArt :name="item.illustration" />
      <span v-if="funded" class="badge"><Icon name="check" :size="15" /> Funded</span>
    </div>
    <div class="body">
      <p class="meta">
        <span class="meta-item"
          ><Icon :name="item.category" :size="16" /> {{ item.category_label }}</span
        >
        <span class="meta-item"><Icon name="pin" :size="16" /> {{ item.city }}</span>
      </p>
      <h3 class="title">
        <RouterLink :to="{ name: 'case', params: { slug: item.slug } }" class="stretched">
          {{ item.title }}
        </RouterLink>
      </h3>
      <p class="summary">{{ item.summary }}</p>
      <div class="progress">
        <ProgressJar :percent="pct" :size="46" />
        <div class="figures">
          <p class="raised"><Money :value="item.raised" /></p>
          <p class="of">
            of <span class="num">{{ Number(item.goal).toLocaleString('en-US') }}</span> ·
            <strong class="num">{{ Math.floor(pct) }}%</strong>
          </p>
          <p class="donors"><Icon name="people" :size="15" /> {{ item.donors_count }} donors</p>
        </div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.case-card {
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border: 1.5px solid var(--line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  transition:
    transform 0.2s var(--ease-out),
    box-shadow 0.2s var(--ease-out),
    border-color 0.2s;
}

.case-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lift);
  border-color: var(--line-strong);
}

.case-card:focus-within {
  border-color: var(--palm);
}

.art {
  position: relative;
  padding: 10px 16px 0;
  background: linear-gradient(var(--paper-deep), var(--paper-deep)) bottom / 100% 1.5px no-repeat;
}

.badge {
  position: absolute;
  top: 12px;
  left: 12px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px 4px 8px;
  border-radius: 999px;
  background: var(--palm);
  color: #fff;
  font-size: var(--text-xs);
  font-weight: 700;
  border: 1.5px solid var(--ink);
}

.body {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px 20px 20px;
  flex: 1;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 14px;
  font-size: var(--text-sm);
  color: var(--ink-soft);
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.title {
  font-size: var(--text-xl);
}

.stretched {
  color: var(--ink);
  text-decoration: none;
}

.stretched::after {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 1;
}

.stretched:focus-visible {
  outline: none;
}

.stretched:focus-visible::after {
  outline: 3px solid var(--focus);
  outline-offset: -3px;
  border-radius: var(--radius-lg);
}

.case-card:hover .stretched {
  text-decoration: underline;
  text-decoration-color: var(--saffron);
  text-decoration-thickness: 2px;
}

.summary {
  color: var(--ink-soft);
  font-size: var(--text-sm);
  flex: 1;
}

.progress {
  display: flex;
  align-items: flex-end;
  gap: 14px;
  margin-top: 8px;
  padding-top: 14px;
  border-top: 1.5px dashed var(--line);
}

.figures {
  display: grid;
  gap: 1px;
}

.raised {
  font-family: var(--font-display);
  font-weight: 650;
  font-size: 1.3rem;
  line-height: 1.1;
}

.of,
.donors {
  font-size: var(--text-sm);
  color: var(--ink-soft);
}

.donors {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
</style>
