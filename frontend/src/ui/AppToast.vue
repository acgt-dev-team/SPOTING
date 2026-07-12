<script>
import { readonly, ref } from "vue"

const toasts = ref([])
let nextToastId = 1

export function removeToast(id) {
  toasts.value = toasts.value.filter((toast) => toast.id !== id)
}

export function showToast({ message, type = "info", duration = 3200 } = {}) {
  if (!message) return null

  const id = nextToastId++

  toasts.value = [
    ...toasts.value,
    {
      id,
      message,
      type
    }
  ]

  if (duration > 0) {
    window.setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  return id
}

export function useToast() {
  return {
    toasts: readonly(toasts),
    removeToast,
    showToast,
    success: (message, options = {}) =>
      showToast({ ...options, type: "success", message }),
    error: (message, options = {}) =>
      showToast({ ...options, type: "error", message }),
    warning: (message, options = {}) =>
      showToast({ ...options, type: "warning", message }),
    info: (message, options = {}) =>
      showToast({ ...options, type: "info", message })
  }
}
</script>

<script setup>
import { AlertTriangle, CheckCircle2, Info, X, XCircle } from "lucide-vue-next"
import { t } from "../i18n"

const { toasts, removeToast } = useToast()

const toastIcons = {
  success: CheckCircle2,
  error: XCircle,
  warning: AlertTriangle,
  info: Info
}

function iconFor(type) {
  return toastIcons[type] || Info
}
</script>

<template>
  <Teleport to="body">
    <TransitionGroup
      name="toast"
      tag="div"
      class="toast-stack"
      aria-live="polite"
      aria-atomic="true"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast-card"
        :class="`toast-card--${toast.type}`"
      >
        <component
          :is="iconFor(toast.type)"
          class="toast-card__icon"
          :size="20"
          aria-hidden="true"
        />

        <p class="toast-card__message">
          {{ toast.message }}
        </p>

        <button
          class="toast-card__close"
          type="button"
          :aria-label="t('common.close')"
          @click="removeToast(toast.id)"
        >
          <X :size="16" aria-hidden="true" />
        </button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<style scoped>
.toast-stack {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 9999;
  width: min(360px, calc(100vw - 32px));
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 12px;
  padding: 14px 14px;
  border: 1px solid var(--toast-border, var(--color-border));
  border-radius: 14px;
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: var(--shadow-md);
  pointer-events: auto;
}

.toast-card--success {
  --toast-border: #bbf7d0;
  --toast-accent: var(--color-success);
  background: #f0fdf4;
}

.toast-card--error {
  --toast-border: #fecaca;
  --toast-accent: var(--color-danger);
  background: #fef2f2;
}

.toast-card--warning {
  --toast-border: #fde68a;
  --toast-accent: var(--color-warning);
  background: #fffbeb;
}

.toast-card--info {
  --toast-border: var(--color-primary-soft-hover);
  --toast-accent: var(--color-primary);
  background: var(--color-primary-soft);
}

.toast-card__icon {
  color: var(--toast-accent);
}

.toast-card__message {
  margin: 0;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 700;
  line-height: 1.45;
}

.toast-card__close {
  width: 28px;
  height: 28px;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: var(--color-text-muted);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.toast-card__close:hover {
  background: rgba(15, 23, 42, 0.06);
  color: var(--color-text);
}

.toast-enter-active,
.toast-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.toast-move {
  transition: transform 180ms ease;
}

@media (max-width: 640px) {
  .toast-stack {
    right: 16px;
    bottom: 16px;
    left: 16px;
    width: auto;
  }
}
</style>
