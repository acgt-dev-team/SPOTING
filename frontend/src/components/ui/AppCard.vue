<script setup>
</script>

<template>
  <div class="card">
    <slot />
  </div>
</template>

<style scoped>
.card {
  width: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.98);
  padding: 28px;
  border-radius: 28px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.06);
  box-sizing: border-box;
}
</style>