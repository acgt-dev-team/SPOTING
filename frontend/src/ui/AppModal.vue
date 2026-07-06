<script setup>
import { X } from "lucide-vue-next"
import { t } from "../i18n"

defineProps({
  show: Boolean,
  title: String
})

const emit = defineEmits(["close"])
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="ui-modal-overlay">

      <div class="ui-modal">

        <div class="ui-modal__header">
          <h2>{{ title }}</h2>

          <button
            class="ui-icon-button"
            :title="t('common.close')"
            :aria-label="t('common.close')"
            @click="$emit('close')"
          >
            <X :size="18" aria-hidden="true" />
          </button>
        </div>

        <div class="ui-modal__body">
          <slot />
        </div>

      </div>

    </div>
  </transition>
</template>
