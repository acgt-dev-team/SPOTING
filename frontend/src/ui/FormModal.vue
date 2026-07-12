<script setup>
import { computed } from "vue"
import { X } from "lucide-vue-next"
import { t } from "../i18n"
import AppCard from "./AppCard.vue"

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  eyebrow: {
    type: String,
    default: ""
  },
  title: {
    type: String,
    required: true
  },
  maxWidth: {
    type: String,
    default: "720px"
  }
})

const emit = defineEmits(["close"])

const cardStyle = computed(() => ({
  maxWidth: props.maxWidth
}))
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="modal-overlay">
      <AppCard class="form-modal" :style="cardStyle">
        <div class="form-modal__header">
          <div>
            <p v-if="eyebrow" class="form-modal__eyebrow">
              {{ eyebrow }}
            </p>
            <h2>{{ title }}</h2>
            <p v-if="$slots.description" class="form-modal__description">
              <slot name="description" />
            </p>
          </div>

          <button
            class="ui-icon-button"
            type="button"
            :title="t('common.close')"
            :aria-label="t('common.close')"
            @click="emit('close')"
          >
            <X :size="18" aria-hidden="true" />
          </button>
        </div>

        <div class="form-modal__body">
          <slot />
        </div>

        <div v-if="$slots.actions" class="form-modal__actions">
          <slot name="actions" />
        </div>
      </AppCard>
    </div>
  </transition>
</template>

<style scoped>
.form-modal {
  width: 100%;
  max-height: calc(100vh - 48px);
  overflow: auto;
}

.form-modal__header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.form-modal__eyebrow {
  margin: 0 0 6px;
  color: var(--color-primary);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.form-modal h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 26px;
  font-weight: var(--font-weight-extrabold);
}

.form-modal__description {
  margin: 8px 0 0;
  color: var(--color-text-muted);
  font-size: var(--font-size-md);
  line-height: 1.5;
}

.form-modal__body {
  min-width: 0;
}

.form-modal__actions {
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid var(--color-surface-hover);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .form-modal__actions {
    flex-direction: column;
    align-items: stretch;
  }

  .form-modal__actions :deep(.ui-button) {
    width: 100%;
  }
}
</style>
