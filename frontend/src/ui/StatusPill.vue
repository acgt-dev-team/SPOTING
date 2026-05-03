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
  const s = String(props.status).toLowerCase()

  // Numeric mapping
  if (s === "1") return "Belum Bermula"
  if (s === "2") return "Dalam Proses"
  if (s === "3") return "Telah Selesai"
  if (s === "4") return "Gagal"

  // String mapping (Profil page)
  if (s.includes("proses")) return "Dalam Proses"
  if (s.includes("dijadualkan")) return "Telah Dijadualkan"
  if (s.includes("selesai")) return "Telah Selesai"
  if (s.includes("gagal")) return "Gagal"
  if (s.includes("belum")) return "Belum Bermula"

  return "Tidak Diketahui"
})

/* =========================
COLOR CLASS
========================= */
const pillClass = computed(() => {
  const s = String(props.status).toLowerCase()

  if (s === "1" || s.includes("belum")) return "running"
  if (s === "2" || s.includes("proses")) return "pending"
  if (s.includes("dijadualkan")) return "scheduled"
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