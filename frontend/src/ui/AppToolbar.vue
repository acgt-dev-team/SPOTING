<script setup>
import { t } from "../i18n"

defineProps({
  placeholder: {
    type: String,
    default: ""
  },
  buttonText: String,
  showButton: Boolean
})

const emit = defineEmits(["action"])
</script>

<template>
  <div class="ui-toolbar">
    <input
      class="ui-input ui-toolbar__search"
      :placeholder="placeholder || t('common.search')"
    />

    <button
      v-if="showButton"
      class="ui-button ui-button--primary"
      @click="$emit('action')"
    >
      {{ buttonText }}
    </button>
  </div>
</template>
