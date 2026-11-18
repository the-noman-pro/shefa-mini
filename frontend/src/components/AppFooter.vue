<template>
  <footer class="site-footer">
    <div class="container inner">
      <p>
        <strong>Shefa mini</strong> is a practice project. No real money moves here: top-ups go
        through a simulated card processor and cases are illustrative.
      </p>
      <p class="small">Amounts in Saudi riyals (SAR).</p>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  margin-top: 72px;
  border-top: 1.5px dashed var(--line-strong);
  padding: 28px 0 36px;
  color: var(--ink-soft);
  font-size: var(--text-sm);
}

.inner {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 8px 24px;
}

.inner p:first-child {
  max-width: 62ch;
}

.small {
  color: var(--ink-muted);
}
</style>
