<script setup>
import { computed } from "vue"

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
      return "Belum Bermula"

    case "2":
    case "in process":
      return "Dalam Proses"

    case "3":
    case "execution completed":
      return "Telah Selesai"

    case "4":
    case "gagal":
      return "Gagal"

    case "telah dijadualkan":
      return "Telah Dijadualkan"

    default:
      return "Tidak Diketahui"
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
      return "running"

    case "2":
    case "in process":
      return "pending"

    case "3":
    case "execution completed":
      return "success"

    case "4":
    case "gagal":
      return "failed"

    case "telah dijadualkan":
      return "scheduled"

    default:
      return "default"
  }
})
</script>

<template>
  <span class="status-pill" :class="pillClass">
    {{ label }}
  </span>
</template>

<style scoped>
.status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

/* Belum Bermula */
.running {
  background: #e5e7eb;
  color: #6b7280;
}

/* Dalam Proses */
.pending {
  background: #fef3c7;
  color: #d97706;
}

/* Telah Dijadualkan */
.scheduled {
  background: #e0e7ff;
  color: #4338ca;
}

/* Telah Selesai */
.success {
  background: #dcfce7;
  color: #16a34a;
}

/* Gagal */
.failed {
  background: #fef2f2;
  color: #dc2626;
}

/* Fallback */
.default {
  background: #f3f4f6;
  color: #6b7280;
}
</style>