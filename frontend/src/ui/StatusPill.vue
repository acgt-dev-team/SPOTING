<script setup>
import { computed } from "vue"

const props = defineProps({
  status: {
    type: [Number, String],
    required: true
  }
})

const label = computed(() => {
  if (props.status === 1 || props.status === "1") return "Belum Bermula"
  if (props.status === 2 || props.status === "2") return "Dalam Proses"
  if (props.status === 3 || props.status === "3") return "Telah Selesai"
  if (props.status === 4 || props.status === "4") return "Gagal"

  // ✅ Handle string input (Profil page)
  if (typeof props.status === "string") return props.status

  return "Unknown"
})

const pillClass = computed(() => {
  const s = String(props.status).toLowerCase()

  if (s === "1" || s.includes("belum")) return "running"
  if (s === "2" || s.includes("proses")) return "pending"
  if (s === "3" || s.includes("selesai")) return "success"
  if (s === "4" || s.includes("gagal")) return "failed"

  return "default"
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
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  min-width: 120px;
  letter-spacing: 0.02em;
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