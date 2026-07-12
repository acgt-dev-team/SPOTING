<script setup>
import { Search } from "lucide-vue-next"
import { t } from "../i18n"

defineProps({
  modelValue: {
    type: String,
    default: ""
  },
  placeholder: {
    type: String,
    default: ""
  },
  actionText: {
    type: String,
    default: ""
  },
  actionDisabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(["update:modelValue", "action"])
</script>

<template>
  <div class="toolbar page-toolbar">
    <div class="page-toolbar__main">
      <div class="search-box">
        <Search class="search-icon" :size="18" aria-hidden="true" />

        <input
          type="text"
          :value="modelValue"
          :placeholder="placeholder || t('common.search')"
          @input="emit('update:modelValue', $event.target.value)"
        />
      </div>

      <div v-if="$slots.filters" class="page-toolbar__filters">
        <slot name="filters" />
      </div>
    </div>

    <button
      v-if="actionText"
      class="ui-button ui-button--primary"
      type="button"
      :disabled="actionDisabled"
      @click="emit('action')"
    >
      <slot name="action-icon" />
      {{ actionText }}
    </button>
  </div>
</template>

<style scoped>
.page-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.page-toolbar__main {
  min-width: 0;
  flex: 1 1 auto;
  display: flex;
  align-items: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

.page-toolbar__filters {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

.page-toolbar__filters :deep(.ui-field) {
  width: 180px;
  margin-bottom: 0;
}

.page-toolbar__filters :deep(.ui-field__label) {
  font-size: 13px;
}

.page-toolbar__filters :deep(.ui-button) {
  height: 48px;
}

.search-box {
  width: 100%;
  max-width: 360px;
  height: 48px;
  padding: 0 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  display: flex;
  align-items: center;
  gap: 12px;
  transition: border-color var(--transition-base), box-shadow var(--transition-base);
}

.search-box:focus-within {
  border-color: var(--color-focus-border);
  box-shadow: var(--focus-ring);
}

.search-icon {
  color: var(--color-placeholder);
  flex-shrink: 0;
}

.search-box input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--color-text);
  font: inherit;
}

@media (max-width: 768px) {
  .page-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .page-toolbar__main,
  .page-toolbar__filters {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: none;
  }

  .page-toolbar__filters :deep(.ui-field) {
    width: 100%;
  }

  .page-toolbar > .ui-button {
    width: 100%;
  }
}
</style>
