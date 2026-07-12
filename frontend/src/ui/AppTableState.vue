<script setup>
import { Inbox, LoaderCircle } from "lucide-vue-next"

defineProps({
  colspan: {
    type: Number,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  actionText: {
    type: String,
    default: ""
  }
})

const emit = defineEmits(["action"])
</script>

<template>
  <tr>
    <td :colspan="colspan" class="table-state-cell">
      <div class="table-state">
        <LoaderCircle
          v-if="loading"
          class="table-state__icon table-state__icon--spin"
          :size="24"
          aria-hidden="true"
        />

        <Inbox
          v-else
          class="table-state__icon"
          :size="24"
          aria-hidden="true"
        />

        <p>{{ message }}</p>

        <button
          v-if="!loading && actionText"
          class="table-state__action"
          type="button"
          @click="emit('action')"
        >
          {{ actionText }}
        </button>
      </div>
    </td>
  </tr>
</template>

<style scoped>
.table-state-cell {
  padding: 0;
}

.table-state {
  min-height: 176px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--color-text-muted);
  text-align: center;
}

.table-state__icon {
  box-sizing: border-box;
  width: 48px;
  height: 48px;
  padding: 12px;
  border-radius: var(--radius-pill);
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.table-state__icon--spin {
  animation: table-state-spin 900ms linear infinite;
}

.table-state p {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
}

.table-state__action {
  min-height: 38px;
  padding: 0 16px;
  border: 1px solid var(--color-primary-soft-hover);
  border-radius: var(--radius-md);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 14px;
  font-weight: var(--font-weight-bold);
  cursor: pointer;
  transition: background var(--transition-base), border-color var(--transition-base);
}

.table-state__action:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-soft-hover);
}

@keyframes table-state-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
