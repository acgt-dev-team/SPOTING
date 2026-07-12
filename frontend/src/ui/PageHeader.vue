<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ""
  }
})
</script>

<template>
  <header class="page-header-card">
    <div class="page-header-card__content">
      <h2>{{ title }}</h2>
      <p v-if="description" class="page-header-card__description">
        {{ description }}
      </p>
    </div>

    <div v-if="$slots.actions" class="page-header-card__actions">
      <slot name="actions" />
    </div>
  </header>
</template>

<style scoped>
.page-header-card {
  margin-bottom: 32px;
  padding: 32px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.page-header-card__content {
  min-width: 0;
}

.page-header-card h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 26px;
  font-weight: var(--font-weight-extrabold);
  line-height: 1.2;
}

.page-header-card__description {
  max-width: 760px;
  margin: 10px 0 0;
  color: var(--color-text-muted);
  font-size: var(--font-size-md);
  line-height: 1.6;
}

.page-header-card__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .page-header-card {
    padding: 24px;
    flex-direction: column;
  }

  .page-header-card__actions {
    width: 100%;
    justify-content: stretch;
  }

  .page-header-card__actions :deep(.ui-button) {
    width: 100%;
  }
}
</style>
