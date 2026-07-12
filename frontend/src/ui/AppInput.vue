<script setup>
defineProps({
  modelValue: String,
  label: String,
  placeholder: String,
  type: {
    type: String,
    default: "text"
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ""
  },
  hint: {
    type: String,
    default: ""
  },
  autocomplete: {
    type: String,
    default: ""
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
      :class="{ 'ui-input--error': error }"
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      :disabled="disabled"
      :autocomplete="autocomplete"
      :aria-invalid="Boolean(error)"
      @input="emit('update:modelValue', $event.target.value)"
    />

    <p v-if="error" class="ui-field__message ui-field__message--error">
      {{ error }}
    </p>

    <p v-else-if="hint" class="ui-field__message">
      {{ hint }}
    </p>
  </div>
</template>
