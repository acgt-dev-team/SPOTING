<script setup>
defineProps({
  value: Number,
  label: String,
  color: String
})
</script>

<template>
  <div class="ui-stat-card">
    <div
      class="ui-stat-card__value"
      :style="{ '--ui-stat-color': color || 'var(--color-primary)' }"
    >
      {{ value }}
    </div>

    <div class="ui-stat-card__label">
      {{ label }}
    </div>
  </div>
</template>
