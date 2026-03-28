<script setup>
defineEmits(["click"])

defineProps({
  text: String,
  variant: {
    type: String,
    default: "primary"
  },
  full: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <button
    :class="['btn', variant, { full }]"
    @click="$emit('click')"
    type="button"
  >
    {{ text }}
  </button>
</template>

<style scoped>
.btn {
  min-height: 52px;
  padding: 14px 22px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  border: none;
  transition: 0.18s ease;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn:hover {
  transform: translateY(-1px);
}

.full {
  width: 100%;
}

.primary {
  background: linear-gradient(135deg, #7c3aed, #c026d3);
  color: white;
  box-shadow: 0 14px 28px rgba(147, 51, 234, 0.25);
}

.outline {
  background: white;
  border: 1px solid #d1d5db;
  color: #111827;
}

.outline:hover {
  border-color: #c4b5fd;
  background: #faf5ff;
}

.secondary {
  background: #f3f4f6;
  color: #111827;
}

.secondary:hover {
  background: #e5e7eb;
}

.link {
  background: none;
  color: #9333ea;
  text-decoration: underline;
  padding: 0;
  min-height: auto;
  border-radius: 0;
  box-shadow: none;
}
</style>