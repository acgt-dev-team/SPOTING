<script setup>
defineProps({
  modelValue: String,
  label: String,
  placeholder: String,
  type: {
    type: String,
    default: "text"
  }
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>
  <div class="field">
    <label v-if="label" class="label">
      {{ label }}
    </label>

    <input
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      @input="emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
  width: 100%;
}

.label {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
}

input {
  width: 100%;
  height: 54px;
  padding: 0 16px;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  font-size: 15px;
  color: #111827;
  transition: 0.18s ease;
  box-sizing: border-box;
}

input::placeholder {
  color: #9ca3af;
}

input:focus {
  outline: none;
  border-color: #020265;
  background: white;
  box-shadow: 0 0 0 4px rgba(2, 2, 101, 0.12);
}
</style>