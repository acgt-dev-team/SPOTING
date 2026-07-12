<script setup>
import { Trash2, TriangleAlert } from "lucide-vue-next"
import { computed } from "vue"
import { t } from "../i18n"

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ""
  },
  keyword: {
    type: String,
    required: true
  },
  modelValue: {
    type: String,
    default: ""
  },
  placeholder: {
    type: String,
    default: ""
  },
  confirmText: {
    type: String,
    default: ""
  },
  confirmVariant: {
    type: String,
    default: "danger"
  },
  icon: {
    type: String,
    default: "delete"
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(["update:modelValue", "close", "confirm"])

const iconComponent = computed(() => (
  props.icon === "warning" ? TriangleAlert : Trash2
))

const tone = computed(() => (
  props.icon === "warning" ? "warning" : "danger"
))

const confirmButtonClass = computed(() => [
  "ui-button",
  `ui-button--${props.confirmVariant}`
])
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="modal-overlay">
      <div
        class="confirm-action-modal"
        :class="`confirm-action-modal--${tone}`"
      >
        <div class="confirm-action-modal__icon">
          <component :is="iconComponent" :size="28" aria-hidden="true" />
        </div>

        <h3>{{ title }}</h3>

        <p class="confirm-action-modal__desc">
          {{ description || t("common.deleteWarning") }}
        </p>

        <div class="confirm-action-modal__body">
          <label>{{ t("common.typeToConfirm", { keyword }) }}</label>

          <div class="confirm-action-modal__keyword">
            <span>{{ keyword }}</span>
          </div>

          <input
            class="confirm-action-modal__input"
            type="text"
            :value="modelValue"
            :placeholder="placeholder || t('common.typeKeyword', { keyword })"
            @input="emit('update:modelValue', $event.target.value)"
          />
        </div>

        <div class="confirm-action-modal__actions">
          <button
            type="button"
            class="ui-button ui-button--outline"
            @click="emit('close')"
          >
            {{ t("common.cancel") }}
          </button>

          <button
            type="button"
            :class="confirmButtonClass"
            :disabled="disabled"
            @click="emit('confirm')"
          >
            {{ confirmText || t("common.deleteNow") }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>
