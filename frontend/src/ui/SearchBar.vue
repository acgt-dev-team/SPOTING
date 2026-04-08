<script setup>
defineProps({
  modelValue: String,
  placeholder: String
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>
  <div class="search">
    <span class="icon">🔍</span>

    <input
      :type="text"
      :placeholder="placeholder"
      :value="modelValue"
      @input="emit('update:modelValue',$event.target.value)"
    />
  </div>
</template>

<style scoped>
.search {
  display: flex;
  align-items: center;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 10px 12px;
  background: white;
  transition: 0.18s ease;
}

.search:focus-within {
  border-color: #020265;
  box-shadow: 0 0 0 4px rgba(2, 2, 101, 0.08);
}

.icon {
  margin-right: 8px;
  color: #6b7280;
}

input {
  border: none;
  outline: none;
  width: 100%;
  color: #111827;
  background: transparent;
}
</style>