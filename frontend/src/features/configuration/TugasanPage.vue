<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { Plus } from "lucide-vue-next"
import api from "../../../src/services/api.js"
import { t } from "../../i18n"
import { useToast } from "../../ui/AppToast.vue"

import AppSelect from "../../ui/AppSelect.vue"
import StatusPill from "../../ui/StatusPill.vue"
import AppPagination from "../../ui/AppPagination.vue"
import ConfigTable from "../../ui/ConfigTable.vue"
import PageHeader from "../../ui/PageHeader.vue"
import PageToolbar from "../../ui/PageToolbar.vue"
import AssignTugasanModal from "./components/AssignTugasanModal.vue"

const route = useRoute()
const router = useRouter()
const toast = useToast()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId
const siteId = route.params.siteId
const profileId = route.params.profileId

// =========================
// PAGINATION
// =========================
const currentPage = ref(1)
const pageSize = 10

const tableColumns = [
  { key: "number", label: t("common.tableNumber"), width: "50px" },
  { key: "codeName", label: t("configuration.taskList.codeName") },
  { key: "protocol", label: t("configuration.taskList.protocol"), width: "100px" },
  { key: "ipRange", label: t("configuration.taskList.ipRange"), width: "180px" },

  {
    key: "agents",
    label: "Bilangan Ejen",
    width: "120px"
  },

  { key: "status", label: t("common.status"), width: "160px" }
]

// =========================
// STATE
// =========================
const search = ref("")
const taskProtocolFilter = ref("")
const taskStatusFilter = ref("")
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
const loading = ref(true)

const taskProtocolFilterOptions = computed(() => {
  const protocols = Array.from(
    new Set(
      tasks.value
        .map((item) => item.protocol)
        .filter(Boolean)
        .map((item) => String(item).toUpperCase())
    )
  ).sort()

  return [
    { label: t("filters.allProtocols"), value: "" },
    ...protocols.map((item) => ({ label: item, value: item }))
  ]
})

const taskStatusFilterOptions = [
  { label: t("filters.allStatuses"), value: "" },
  { label: t("status.notStarted"), value: "1" },
  { label: t("status.inProcess"), value: "2" },
  { label: t("status.completed"), value: "3" },
  { label: t("status.failed"), value: "4" }
]

const hasTaskFilters = computed(() =>
  Boolean(taskProtocolFilter.value || taskStatusFilter.value)
)

const hasTaskQuery = computed(() =>
  Boolean(search.value.trim() || hasTaskFilters.value)
)

// =========================
// FILTER
// =========================
const filteredTasks = computed(() => {
  const query = search.value.trim().toLowerCase()

  return tasks.value.filter((item) => {
    const searchableValues = [item.nama, item.kod, item.protocol]
    const matchesSearch = !query || searchableValues.some((value) =>
      String(value || "").toLowerCase().includes(query)
    )

    const matchesProtocol =
      !taskProtocolFilter.value ||
      String(item.protocol || "").toUpperCase() === taskProtocolFilter.value
    const matchesStatus =
      !taskStatusFilter.value ||
      String(item.status || "") === taskStatusFilter.value

    return matchesSearch && matchesProtocol && matchesStatus
  })
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
  loading.value = true

  try {
    const res = await api.get(`/tugasan/profil/${profileId}`)
    tasks.value = res.data || []
  } catch (err) {
    console.error("Error loading tasks:", err)
    toast.error(t("common.loadFailed", { entity: t("configuration.taskList.countEntity") }))
  } finally {
    loading.value = false
  }
}

async function loadAllTugasan() {
  try {
    const res = await api.get("/tugasan/")
    allTugasan.value = res.data
  } catch (err) {
    console.error("Error loading all tugasan:", err)
    toast.error(t("common.loadFailed", { entity: t("configuration.taskList.countEntity") }))
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
    toast.success(t("common.saveSuccess", { entity: t("configuration.taskList.countEntity") }))
  } catch (err) {
    console.error("Error assigning task:", err)
    toast.error(t("common.saveFailed", { entity: t("configuration.taskList.countEntity") }))
  }
}

async function removeTask(tugasanId) {
  if (!confirm(t("configuration.taskList.removeConfirm"))) return

  try {
    await api.delete(`/tugasan/profil/${profileId}/${tugasanId}`)
    await loadTasks()
    toast.success(t("common.deleteSuccess", { entity: t("configuration.taskList.countEntity") }))
  } catch (err) {
    console.error("Error removing task:", err)
    toast.error(t("common.deleteFailed", { entity: t("configuration.taskList.countEntity") }))
  }
}

// =========================
// MODAL
// =========================
function handleAssigned() {
  loadTasks()
  showModal.value = false
  toast.success(t("common.saveSuccess", { entity: t("configuration.taskList.countEntity") }))
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
watch([search, taskProtocolFilter, taskStatusFilter], () => {
  currentPage.value = 1
})

function clearTaskFilters() {
  taskProtocolFilter.value = ""
  taskStatusFilter.value = ""
}

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

    <PageHeader
      :title="profile.name"
      :description="profile.description"
    />

    <PageToolbar
      v-model="search"
      :placeholder="t('configuration.shared.search', { entity: t('configuration.taskList.searchEntity') })"
      :action-text="t('configuration.taskList.assign')"
      @action="showModal = true"
    >
      <template #filters>
        <AppSelect
          v-model="taskProtocolFilter"
          :label="t('configuration.taskList.protocol')"
          :options="taskProtocolFilterOptions"
        />

        <AppSelect
          v-model="taskStatusFilter"
          :label="t('common.status')"
          :options="taskStatusFilterOptions"
        />

        <button
          v-if="hasTaskFilters"
          class="ui-button ui-button--outline"
          type="button"
          @click="clearTaskFilters"
        >
          {{ t("filters.clear") }}
        </button>
      </template>

      <template #action-icon>
        <Plus :size="18" aria-hidden="true" />
      </template>
    </PageToolbar>

    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("configuration.taskList.pageTitle") }}</h1>
    </div>

    <ConfigTable
      :columns="tableColumns"
      :loading="loading"
      :empty="paginatedTasks.length === 0"
      :empty-message="t('configuration.taskList.empty')"
      :empty-action-text="hasTaskQuery ? '' : t('configuration.taskList.assign')"
      min-width="760px"
      @empty-action="openAddModal"
    >

            <tr
              v-for="(task, index) in paginatedTasks"
              :key="task.id"
              class="clickable-row"
            >
              <td>
                {{ (currentPage - 1) * pageSize + index + 1 }}
              </td>

              <td>
                <div class="task-info">
                  <p class="task-name">{{ task.nama }}</p>
                  <p class="task-code">{{ task.kod }}</p>
                </div>
              </td>

              <td>
                <span
                  class="protocol-badge"
                  :class="'protocol-' + (task.protocol || 'default').toLowerCase()"
                >
                  {{ task.protocol || t("common.emptyValue") }}
                </span>
              </td>

              <td>
                <div class="ip-range">
                  <span>{{ task.ip_start || t("common.emptyValue") }}</span>
                  <span class="ip-sep">→</span>
                  <span>{{ task.ip_end || t("common.emptyValue") }}</span>
                </div>
              </td>
              
              <td>
                {{ task.completed_agent_count }}/{{ task.agent_count }}
              </td>

              <td>
                <StatusPill :status="task.status" />
              </td>
            </tr>

    </ConfigTable>

    <AppPagination
      :currentPage="currentPage"
      :totalPages="totalPages"
      @update:page="currentPage = $event"
    />

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

.clickable-row{
  transition:.15s;
}

.clickable-row:hover{
  background:#F8FAFC;
}

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

@media(max-width:768px){

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
  color: #94a3b8;
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

tbody tr {
  background: #ffffff;
}

</style>

