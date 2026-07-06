<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { Plus, Search } from "lucide-vue-next"
import api from "../../../src/services/api.js"
import { t } from "../../i18n"

import StatusPill from "../../ui/StatusPill.vue"
import AppPagination from "../../ui/AppPagination.vue"
import AssignTugasanModal from "./components/AssignTugasanModal.vue"

const route = useRoute()
const router = useRouter()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId
const siteId = route.params.siteId
const profileId = route.params.profileId

// =========================
// PAGINATION
// =========================
const currentPage = ref(1)
const pageSize = 10

// =========================
// STATE
// =========================
const search = ref("")
const showModal = ref(false)
const selectedTugasanId = ref(null)

const profile = ref({
  id: profileId,
  name: t("configuration.taskList.defaultName"),
  description: t("configuration.taskList.defaultDescription")
})

// =========================
// DATA
// =========================
const tasks = ref([])
const allTugasan = ref([])

// =========================
// FILTER
// =========================
const filteredTasks = computed(() => {
  return tasks.value.filter((item) =>
    item.nama?.toLowerCase().includes(search.value.toLowerCase())
  )
})

// =========================
// PAGINATION LOGIC
// =========================
const paginatedTasks = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredTasks.value.slice(start, start + pageSize)
})

const totalPages = computed(() => {
  return Math.ceil(filteredTasks.value.length / pageSize)
})

// =========================
// API CALLS
// =========================
async function loadTasks() {
  try {
    const res = await api.get(`/tugasan/profil/${profileId}`)
    tasks.value = res.data || []
  } catch (err) {
    console.error("Error loading tasks:", err)
  }
}

async function loadAllTugasan() {
  try {
    const res = await api.get("/tugasan/")
    allTugasan.value = res.data
  } catch (err) {
    console.error("Error loading all tugasan:", err)
  }
}

// =========================
// ASSIGN
// =========================
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
  if (!confirm(t("configuration.taskList.removeConfirm"))) return

  try {
    await api.delete(`/tugasan/profil/${profileId}/${tugasanId}`)
    await loadTasks()
  } catch (err) {
    console.error("Error removing task:", err)
  }
}

// =========================
// MODAL
// =========================
function handleAssigned() {
  loadTasks()
  showModal.value = false
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

// =========================
// NAVIGATION
// =========================
function goBack() {
  router.push(
    `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${siteId}`
  )
}



// =========================
// WATCHERS
// =========================
watch(search, () => {
  currentPage.value = 1
})

watch(filteredTasks, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value || 1
  }
})

// =========================
// INIT
// =========================
onMounted(() => {
  loadTasks()
  loadAllTugasan()
})
</script>

<template>
  <div>

    <!-- Header -->
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>{{ profile.name }}</h2>
        <p class="section-desc">{{ profile.description }}</p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <Search class="search-icon" :size="18" aria-hidden="true" />
        <input
          v-model="search"
          type="text"
          :placeholder="t('configuration.shared.search', { entity: t('configuration.taskList.searchEntity') })"
        />
      </div>

      <button
        class="ui-button ui-button--primary"
        @click="showModal = true"
      >
        <Plus :size="18" aria-hidden="true" />
        {{ t("configuration.taskList.assign") }}
      </button>
    </div>

    <!-- Title -->
    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("configuration.taskList.pageTitle") }}</h1>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width: 50px">{{ t("common.tableNumber") }}</th>
              <th style="width: 35%">{{ t("configuration.taskList.codeName") }}</th>
              <th style="width: 100px">{{ t("configuration.taskList.protocol") }}</th>
              <th style="width: 180px">{{ t("configuration.taskList.ipRange") }}</th>
              <th style="width: 160px">{{ t("common.status") }}</th>
            </tr>
          </thead>

          <tbody>

            <!-- ✅ FIXED EMPTY STATE -->
            <tr v-if="paginatedTasks.length === 0">
              <td colspan="5" class="empty-cell">
                {{ t("configuration.taskList.empty") }}
              </td>
            </tr>

            <!-- ✅ PAGINATED LOOP -->
            <tr
              v-for="(task, index) in paginatedTasks"
              :key="task.id"
              class="clickable-row"
            >
              <!-- Bil -->
              <td>
                {{ (currentPage - 1) * pageSize + index + 1 }}
              </td>

              <!-- Nama -->
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
                  {{ task.protocol || t("common.emptyValue") }}
                </span>
              </td>

              <!-- IP -->
              <td>
                <div class="ip-range">
                  <span>{{ task.ip_start || t("common.emptyValue") }}</span>
                  <span class="ip-sep">→</span>
                  <span>{{ task.ip_end || t("common.emptyValue") }}</span>
                </div>
              </td>

              <!-- ✅ Status -->
              <td>
                <StatusPill :status="task.status" />
              </td>
            </tr>

          </tbody>
        </table>
      </div>
    </div>

    <!-- ✅ PAGINATION -->
    <AppPagination
      :currentPage="currentPage"
      :totalPages="totalPages"
      @update:page="currentPage = $event"
    />

    <!-- Footer -->
    <div class="footer-bar">
      <button class="ui-button ui-button--outline" @click="goBack">
        {{ t("common.back") }}
      </button>

      <div class="count-pill">
        {{ t("configuration.shared.count", { entity: t("configuration.taskList.countEntity") }) }}
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

  </div>
</template>

<style scoped>
:root{
  --primary:#4F46E5;
  --primary-soft:#EEF2FF;
  --text:#0F172A;
  --muted:#64748B;
  --border:#E2E8F0;
  --bg:#F8FAFC;
}

.page-heading-block{
  margin-bottom:28px;
}

.main-page-title{
  font-size:30px;
  font-weight:800;
  color:var(--text);
  margin:0;
  letter-spacing:-0.03em;
}

/* HERO */

.hierarchy-card{
  background:white;

  border:1px solid var(--border);

  border-radius:20px;

  padding:32px;

  margin-bottom:32px;

  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.hierarchy-left h2{
  margin:0;

  font-size:32px;

  font-weight:800;

  color:var(--text);
}

.section-desc{
  margin-top:8px;

  color:var(--muted);
}

/* TOOLBAR */

.toolbar{
  display:flex;

  justify-content:space-between;

  align-items:center;

  gap:16px;

  margin-bottom:28px;

  flex-wrap:wrap;
}

.search-box{
  width:100%;

  max-width:360px;
}

/* SEARCH */

.search-box{
  width:100%;

  max-width:360px;

  display:flex;

  align-items:center;

  gap:12px;

  background:white;

  border:1px solid var(--border);

  border-radius:14px;

  height:48px;

  padding:0 16px;

  transition:.2s;
}

.search-box:focus-within{
  border-color:var(--primary);

  box-shadow:0 0 0 3px rgba(79,70,229,.08);
}

.search-icon{
  color:#94A3B8;
}

.search-box input{
  border:none;

  background:none;

  width:100%;

  outline:none;

  color:var(--text);
}

/* BUTTON */

.btn-plus{
  font-size:18px;

  font-weight:500;

  line-height:1;

  margin-top:-1px;
}

/* TABLE */

.table-card{
  background:white;

  border:1px solid var(--border);

  border-radius:20px;

  overflow:hidden;

  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.table-scroll{
  overflow:auto;
}

table{
  width:100%;

  border-collapse:collapse;
}

thead{
  background:#F8FAFC;
}

th{
  text-align:left;

  padding:18px 24px;

  font-size:12px;

  color:#64748B;

  text-transform:uppercase;

  letter-spacing:.04em;

  font-weight:700;

  border-bottom:1px solid var(--border);
}

td{
  padding:18px 24px;

  vertical-align:middle;

  border-bottom:1px solid #F1F5F9;

  color:#334155;
}

.clickable-row{
  transition:.15s;
}

.clickable-row:hover{
  background:#F8FAFC;
}

.org-cell{
  display:flex;

  align-items:center;

  gap:14px;

  min-height:40px;
}

.org-avatar{
  width:40px;

  height:40px;

  border-radius:12px;

  background:#312E81;

  color:white;

  font-weight:800;

  display:flex;

  align-items:center;

  justify-content:center;
}

.org-name{
  margin:0;

  font-weight:700;

  color:#1E293B;
}

.org-desc{
  margin-top:4px;

  color:#94A3B8;

  font-size:13px;
}

.pegawai-cell{
  display:flex;

  flex-direction:column;

  justify-content:center;

  min-height:40px;
}

.pegawai-name{
  margin:0;

  font-weight:600;

  color:#334155;
}

.pegawai-jawatan{
  margin-top:4px;

  color:#94A3B8;

  font-size:13px;
}

.empty-cell{
  text-align:center;

  color:#94A3B8;

  padding:50px;
}


/* FOOTER */

.footer-bar{
  display:flex;

  justify-content:space-between;

  align-items:center;

  margin-top:20px;
}

.count-pill{
  background:white;

  border:1px solid var(--border);

  border-radius:14px;

  padding:12px 18px;

  color:#64748B;
}

.count-pill strong{
  color:var(--primary);
}

/* MODAL */

.fade-enter-active,
.fade-leave-active{
  transition:.18s;
}

.fade-enter-from,
.fade-leave-to{
  opacity:0;
}

.modal-overlay{
  position:fixed;
  inset:0;
  background:rgba(15,23,42,.55);
  backdrop-filter:blur(6px);
  display:flex;
  align-items:center;
  justify-content:center;
  z-index:999;
  padding:24px;
  overflow-y:auto;
}

.modal-card{
  max-width:700px;
  width:100%;
  border-radius:20px;
  background:white;
  padding:30px !important;

  max-height:95vh;
  overflow-y:auto;
}

.modal-card::-webkit-scrollbar{
  width:8px;
}

.modal-card::-webkit-scrollbar-thumb{
  background:#CBD5E1;
  border-radius:999px;
}

.modal-card::-webkit-scrollbar-track{
  background:transparent;
}

.modal-header{
  display:flex;
  justify-content:space-between;
  margin-bottom:28px;
}

.modal-header h2{
  font-size:28px;
  font-weight:800;
  color:var(--text);
  margin:0;
}

.eyebrow{
  color:var(--primary);
  font-size:12px;
  letter-spacing:.12em;
  font-weight:700;
}

.form-area{
  width:100%;
}

.textarea-field{
  margin-top:18px;
}

.textarea-label{
  display:block;
  margin-bottom:10px;
  font-weight:600;
}

textarea{
  width:100%;
  border:1px solid var(--border);
  background:#F8FAFC;
  border-radius:14px;
  padding:14px;
  resize:none;
  box-sizing:border-box;
}

textarea:focus{
  outline:none;
  border-color:var(--primary);
  background:white;
}

.modal-actions{
  display:flex;
  justify-content:flex-end;
  align-items:center;
  gap:12px;
  margin-top:32px;
  padding-top:20px;
  border-top:1px solid #F1F5F9;
  flex-wrap:wrap;
}

/* APPBUTTON STYLING */

/* DELETE BUTTON */

/* DELETE MODAL */

.delete-modal{
  background:white;
  border-radius:20px;
  padding:28px;
  width:100%;
  max-width:480px;
  border:1px solid var(--border);
}

.delete-modal h3{
  text-align:center;
  font-size:24px;
  font-weight:900;
  color:#111827;
  margin-bottom:8px;
  width:100%;
}

.delete-icon{
  width:64px;
  height:64px;
  margin:auto;
  border-radius:999px;
  background:#FEF2F2;
  display:flex;
  align-items:center;
  justify-content:center;
}

.delete-desc{
  text-align:center;
  color:#64748B;
  margin-bottom:22px;
}

.confirm-box label{
  display:block;
  margin-bottom:10px;
  font-size:14px;
  font-weight:600;
  color:#334155;
}

.org-delete-name{
  background:#F8FAFC;
  border:1px solid var(--border);
  padding:14px;
  border-radius:12px;
  margin-bottom:12px;
  font-weight:700;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
}

.danger-word{
  text-align:center;
  color:#DC2626;
  font-size:20px;
  font-weight:800;
}

.delete-input{
  width:100%;
  border:1px solid var(--border);
  border-radius:12px;
  padding:14px;
}

.delete-input:focus{
  outline:none;
  border-color:#EF4444;
}

.delete-actions{
  display:flex;
  justify-content:flex-end;
  gap:12px;
  margin-top:24px;
}

/* TOAST */

.toast-success{
  position:fixed;
  right:24px;
  bottom:24px;
  background:white;
  border:1px solid #DCFCE7;
  border-radius:14px;
  padding:14px 18px;
  box-shadow:0 10px 24px rgba(15,23,42,.08);
  z-index:9999;
}

/* RESPONSIVE */

@media(max-width:768px){

  .toolbar{
    flex-direction:column;
    align-items:stretch;
  }

  .search-box{
    max-width:none;
    width:100%;
  }

  .modal-actions,
  .delete-actions,
  .footer-bar{
    flex-direction:column;
    align-items:stretch;
  }

}

.task-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.task-name {
  font-weight: 600;
  font-size: 14px;
  color: #111827;
  margin: 0;
}

.task-code {
  font-size: 12px;
  color: #94a3b8; /* 🔥 softer than current */
  font-weight: 500;
  font-family: inherit;
  margin-top: 2px;
  letter-spacing: 0.02em;
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

.ip-range {
  display: flex;
  gap: 6px;
  font-size: 13px;
  color: #374151;
  font-weight: 500;
  font-family: inherit;
}

.ip-sep {
  color: #9ca3af;
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
