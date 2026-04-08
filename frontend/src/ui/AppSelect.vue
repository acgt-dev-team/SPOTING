<script setup>
defineProps({
  label: String,
  options: Array,
  modelValue: String
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>
  <div class="field">
    <label>{{ label }}</label>

    <select
      :value="modelValue"
      @change="emit('update:modelValue', $event.target.value)"
    >
      <option disabled value="">Pilih</option>

      <option
        v-for="opt in options"
        :key="opt"
        :value="opt"
      >
        {{ opt }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 13px;
  color: #374151;
  font-weight: 600;
}

select {
  height: 44px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  background: white;
  padding: 0 12px;
  color: #111827;
  transition: 0.18s ease;
}

select:focus {
  outline: none;
  border-color: #020265;
  box-shadow: 0 0 0 4px rgba(2, 2, 101, 0.1);
}
</style>