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
  <div class="ui-field">
    <label v-if="label" class="ui-field__label">
      {{ label }}
    </label>

    <input
      class="ui-input"
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      @input="emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>
