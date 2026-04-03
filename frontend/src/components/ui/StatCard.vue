<script setup>
defineProps({
  value: Number,
  label: String,
  color: String
})
</script>

<template>
  <div class="card">
    <div class="value" :style="{ color: color || '#020265' }">
      {{ value }}
    </div>

    <div class="label">
      {{ label }}
    </div>
  </div>
</template>

<style scoped>
.card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  width: 140px;
  text-align: center;
  border: 1px solid #e5e7eb;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
}

.value {
  font-size: 30px;
  font-weight: 700;
}

.label {
  font-size: 12px;
  color: #6b7280;
}
</style>