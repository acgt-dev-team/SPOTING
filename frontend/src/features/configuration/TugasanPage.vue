<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../../../src/services/api.js"

import AssignTugasanModal from "./components/AssignTugasanModal.vue"

const route = useRoute()
const router = useRouter()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId
const siteId = route.params.siteId
const profileId = route.params.profileId

const search = ref("")
const showModal = ref(false)



// ✅ NEW: dropdown selection
const selectedTugasanId = ref(null)

const profile = ref({
  id: profileId,
  name: "Profil Operasi",
  description: "Tetapan operasi tapak"
})

// ✅ FROM API
const tasks = ref([])
const allTugasan = ref([])

// 🔍 Filter
const filteredTasks = computed(() => {
  return tasks.value.filter((item) =>
    item.nama.toLowerCase().includes(search.value.toLowerCase())
  )
})

// 🧠 Status mapping
function getStatusLabel(status) {
  if (status === 1) return "Pending"
  if (status === 2) return "Sedang Berjalan"
  if (status === 3) return "Selesai"
  if (status === 4) return "Failed"
  return "Unknown"
}

// 🔥 Load assigned tasks
async function loadTasks() {
  try {
    const res = await api.get(`/tugasan/profil/${profileId}`)
    tasks.value = res.data
  } catch (err) {
    console.error("Error loading tasks:", err)
  }
}

// 🔥 Load all available tugasan (for dropdown)
async function loadAllTugasan() {
  try {
    const res = await api.get("/tugasan/")
    allTugasan.value = res.data
  } catch (err) {
    console.error("Error loading all tugasan:", err)
  }
}

// 🚀 Assign tugasan
async function assignTask() {
  if (!selectedTugasanId.value) return

  try {
    await api.post(`/tugasan/profil/${profileId}/`, {
  tugasan_id: selectedTugasanId.value
})

    await loadTasks()
    closeModal()
  } catch (err) {
    console.error("Error assigning task:", err)
  }
}

async function removeTask(tugasanId) {
  if (!confirm("Buang tugasan ini?")) return

  try {
    await api.delete(`/tugasan/profil/${profileId}/${tugasanId}`)
    await loadTasks()
  } catch (err) {
    console.error("Error removing task:", err)
  }
}

// Modal handling
function handleAssigned() {
  loadTasks()      // 🔥 reload table after assign/unassign
  showModal.value = false
}


async function handleAssign() {
  try {
    // 🔥 current assigned from DB
    const res = await api.get(`/tugasan/profil/${profileId}/`)
    const assignedIds = res.data.map(t => t.id)

    const selectedIds = [...selected.value]

    // ➕ ADD (newly checked)
    for (const id of selectedIds) {
      if (!assignedIds.includes(id)) {
        await api.post(`/tugasan/profil/${profileId}/`, {
  tugasan_id: selectedTugasanId.value
})
      }
    }

    // ❌ REMOVE (unchecked)
    for (const id of assignedIds) {
      if (!selectedIds.includes(id)) {
        await api.delete(`/tugasan/profil/${profileId}/${id}`)
      }
    }

    emit('assigned')

  } catch (err) {
    console.error('Sync failed:', err)
  }
}




watch(showModal, (value) => {
  if (value) {
    selectedTugasanId.value = null
  }
})

function openAddModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

// Navigation
function goBack() {
  router.push(`/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${siteId}`)
}

//scan func
async function runScan(task) {
  try {
    await api.post("/tugasan/execute-scan", {
      profil_tugasan_id: task.profil_tugasan_id,
      penjadualan: false
    })

    alert("Scan started successfully")
  } catch (err) {
    console.error(err)
    alert("Failed to start scan")
  }
}

// 🚀 Load data on mount
onMounted(() => {
  loadTasks()
  loadAllTugasan()
})
</script>

<template>
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>{{ profile.name }}</h2>
        <p class="parent-desc">{{ profile.description }}</p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian tugasan..." />
      </div>

      <button class="primary-btn" @click="showModal = true">
  Tetapkan Tugasan
</button>
    </div>

    <!-- Title -->
    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Tugasan</h1>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-scroll">
        <table>
  <thead>
    <tr>
      <th style="width: 80px">Bil</th>
      <th>Nama / Kod</th>
      <th style="width: 120px">Protokol</th>
      <th style="width: 200px">IP Range</th>
      <th style="width: 140px">Status</th>
      <th style="width:140px">Tindakan</th>
    </tr>
  </thead>

  <tbody>
    <!-- Empty -->
    <tr v-if="filteredTasks.length === 0">
      <td colspan="6" class="empty-cell">
        Tiada tugasan dijumpai.
      </td>
    </tr>

    <!-- Rows -->
    <tr
      v-for="(task, index) in filteredTasks"
      :key="task.id"
      class="clickable-row"
    >
      <!-- Bil -->
      <td>{{ index + 1 }}</td>

      <!-- Nama + Kod -->
      <td>
        <div class="task-info">
          <p class="task-name">{{ task.nama }}</p>
          <p class="task-code">{{ task.kod }}</p>
        </div>
      </td>

      <!-- Protocol -->
      <td>
        <span
          class="protocol-badge"
          :class="'protocol-' + (task.protocol || 'default').toLowerCase()"
        >
          {{ task.protocol || '-' }}
        </span>
      </td>

      <!-- IP Range -->
      <td>
        <div class="ip-range">
          <span>{{ task.ip_start || '-' }}</span>
          <span class="ip-sep">→</span>
          <span>{{ task.ip_end || '-' }}</span>
        </div>
      </td>

      <!-- Status -->
      <td>
        <span
          class="status-pill"
          :class="{
            running: task.status === -1,
            pending: task.status === 0,
            success: task.status === 1
          }"
        >
          {{ getStatusLabel(task.status) }}
        </span>
      </td>

      <!-- Actions -->
      <td>
  <button
    class="primary-btn small"
    @click.stop="runScan(task)"
  >
    Run Scan
  </button>
</td>
    </tr>
  </tbody>
</table>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer-bar">
      <button class="secondary-btn" @click="goBack">
        ← Kembali
      </button>

      <div class="count-pill">
        Bilangan Tugasan:
        <strong>
          {{ filteredTasks.length.toString().padStart(2, "0") }}
        </strong>
      </div>
    </div>

    <!-- Modal -->
    <AssignTugasanModal
  v-if="showModal"
  @close="showModal = false"
  @assigned="handleAssigned"
/>
</template>

<style scoped>
.page-heading-block {
  margin-bottom: 24px;
}

.main-page-title {
  font-size: 30px;
  font-weight: 700;
  line-height: 1.15;
  color: #1f2937;
  margin: 0;
  letter-spacing: -0.02em;
  font-family: "Proxima Nova", proxima-nova, "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.toolbar,
.footer-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.toolbar {
  margin-bottom: 20px;
}
.footer-bar {
  margin-top: 24px;
}

.search-box {
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #dbe3ff;
  border-radius: 18px;
  padding: 0 16px;
  height: 54px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
}

.search-box:focus-within {
  border-color: #020265;
  box-shadow: 0 0 0 4px rgba(2, 2, 101, 0.08);
}

.search-box input {
  border: none;
  outline: none;
  background: transparent;
  width: 100%;
  font-size: 14px;
  color: #111827;
}

.search-icon {
  color: #6b7280;
  font-size: 18px;
}

.hierarchy-card {
  display: flex;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid #dbe3ff;
  border-radius: 30px;
  padding: 30px;
  margin-bottom: 28px;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.06);
}

.parent-label {
  font-size: 13px;
  font-weight: 800;
  color: #020265;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}

.hierarchy-left h2 {
  font-size: 32px;
  font-weight: 900;
  color: #111827;
  margin-bottom: 8px;
}

.parent-desc,
.org-desc {
  color: #6b7280;
  font-size: 14px;
}

thead {
  background: #f4f6ff;
}

th {
  text-align: left;
  padding: 20px 24px;
  font-size: 13px;
  font-weight: 800;
  color: #24324a;
  border-bottom: 1px solid #e4e9f8;
  text-transform: uppercase;
}

td {
  padding: 18px 24px;
  font-size: 15px;
  border-bottom: 1px solid #f1f5f9;
  color: #111827;
}

.clickable-row:hover {
  background: #f4f6ff;
}

.org-name {
  font-weight: 800;
  color: #111827;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  background: #dcfce7;
  color: #166534;
  font-size: 13px;
  font-weight: 800;
}

.status-pill.draft {
  background: #eef1ff;
  color: #020265;
}

.ghost-btn {
  border: none;
  background: #eef1ff;
  color: #020265;
  padding: 10px 14px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.18s ease;
}

.ghost-btn:hover {
  background: #dde3ff;
}

.primary-btn,
.secondary-btn {
  border: none;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}

.primary-btn {
  padding: 14px 22px;
  background: linear-gradient(135deg, #020265, #0b0b8f);
  color: white;
  box-shadow: 0 14px 28px rgba(2, 2, 101, 0.25);
}

.primary-btn:hover {
  transform: translateY(-1px);
}

.secondary-btn {
  padding: 14px 22px;
  background: white;
  border: 1px solid #dbe3ff;
  color: #111827;
}

.secondary-btn:hover {
  background: #f4f6ff;
  transform: translateY(-1px);
}

.empty-cell {
  text-align: center;
  padding: 52px 20px;
  color: #6b7280;
  background: #ffffff;
}

.count-pill {
  background: white;
  border: 1px solid #dbe3ff;
  border-radius: 18px;
  padding: 16px 20px;
  color: #374151;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

.count-pill strong {
  margin-left: 10px;
  color: #020265;
}

/* Modal */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.18s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 24px;
}

.modal-card {
  width: 100%;
  max-width: 720px;
  padding: 28px !important;
  animation: popIn 0.18s ease;
  box-sizing: border-box;
}

@keyframes popIn {
  from {
    transform: translateY(8px) scale(0.98);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
}

.eyebrow {
  font-size: 12px;
  font-weight: 800;
  color: #020265;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 10px;
}

.modal-header h2 {
  font-size: 26px;
  font-weight: 900;
  color: #111827;
  line-height: 1.15;
}

.close-btn {
  border: none;
  background: #f3f4f6;
  width: 44px;
  height: 44px;
  border-radius: 999px;
  cursor: pointer;
  font-size: 18px;
  color: #374151;
  flex-shrink: 0;
}

.form-area {
  width: 100%;
}

.textarea-field,
.select-field {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
  width: 100%;
}

.textarea-label {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
}

textarea,
select {
  width: 100%;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  border-radius: 18px;
  padding: 16px;
  font-size: 15px;
  outline: none;
  transition: 0.2s ease;
  color: #111827;
  box-sizing: border-box;
  font-family: inherit;
}

textarea {
  min-height: 130px;
  resize: vertical;
}

textarea:focus,
select:focus {
  border-color: #020265;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(2, 2, 101, 0.08);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 14px;
  margin-top: 28px;
  flex-wrap: wrap;
}

.task-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.task-name {
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.task-code {
  font-size: 12px;
  color: #6b7280;
  font-family: monospace;
}

/* Protocol badge */
.protocol-badge {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid;
}

.protocol-tcp {
  background: rgba(59,130,246,0.1);
  color: #3b82f6;
  border-color: #3b82f6;
}

.protocol-udp {
  background: rgba(139,92,246,0.1);
  color: #8b5cf6;
  border-color: #8b5cf6;
}

.protocol-http {
  background: rgba(34,197,94,0.1);
  color: #22c55e;
  border-color: #22c55e;
}

.protocol-ssh {
  background: rgba(239,68,68,0.1);
  color: #ef4444;
  border-color: #ef4444;
}

.protocol-default {
  background: #f3f4f6;
  color: #6b7280;
}

/* IP */
.ip-range {
  display: flex;
  gap: 6px;
  font-family: monospace;
  font-size: 13px;
  color: #374151;
}

.ip-sep {
  color: #9ca3af;
}

/* Status */
.status-pill.running {
  background: #fef3c7;
  color: #d97706;
}

.status-pill.pending {
  background: #e5e7eb;
  color: #6b7280;
}

.status-pill.success {
  background: #dcfce7;
  color: #16a34a;
}

.table-card {
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid #dbe3ff;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.06);
  width: 100%;
}

.table-scroll {
  overflow-x: auto;
  width: 100%;
}

table {
  width: 100%;
  border-collapse: collapse;
}

tbody tr {
  background: #ffffff;
}

</style>