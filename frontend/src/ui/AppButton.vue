<script setup>
import { computed } from "vue"

defineEmits(["click"])

const props = defineProps({
  text: String,
  variant: {
    type: String,
    default: "primary"
  },
  full: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const classes = computed(() => [
  "ui-button",
  ...props.variant.split(" ").map((variant) => `ui-button--${variant}`),
  { "ui-button--full": props.full }
])
</script>

<template>
  <button
    :class="classes"
    :disabled="disabled"
    @click="$emit('click')"
    type="button"
  >
    <slot name="icon" />
    {{ text }}
  </button>
</template>
