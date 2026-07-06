<script setup>
import { computed } from "vue"
import { t } from "../i18n"

const props = defineProps({
  status: {
    type: [Number, String],
    required: true
  }
})

/* =========================
LABEL (DISPLAY TEXT - MALAY)
========================= */
const label = computed(() => {
  const s = String(props.status).toLowerCase().trim()

  switch (s) {
    case "1":
    case "belum dimulakan":
      return t("status.notStarted")

    case "2":
    case "in process":
      return t("status.inProcess")

    case "3":
    case "execution completed":
      return t("status.completed")

    case "4":
    case "gagal":
      return t("status.failed")

    case "telah dijadualkan":
      return t("status.scheduled")

    default:
      return t("status.unknown")
  }
})

/* =========================
COLOR CLASS
========================= */
const pillClass = computed(() => {
  const s = String(props.status).toLowerCase().trim()

  switch (s) {
    case "1":
    case "belum dimulakan":
      return "ui-status--idle"

    case "2":
    case "in process":
      return "ui-status--pending"

    case "3":
    case "execution completed":
      return "ui-status--success"

    case "4":
    case "gagal":
      return "ui-status--failed"

    case "telah dijadualkan":
      return "ui-status--scheduled"

    default:
      return "ui-status--unknown"
  }
})
</script>

<template>
  <span class="ui-status" :class="pillClass">
    {{ label }}
  </span>
</template>
