<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import { Pencil, Plus, Search, X } from "lucide-vue-next"
import AddTugasanModal from "./AddTugasanModal.vue"
import api from "../../../services/api"
import { t } from "../../../i18n"
import { useToast } from "../../../ui/AppToast.vue"

const emit = defineEmits(["close", "assigned"])

const route = useRoute()
const profileId = route.params.profileId
const toast = useToast()

const tugasanList = ref([])
const showAdd = ref(false)
const editingTask = ref(null)

const search = ref("")
const selectedIds = ref([])
const originalIds = ref([])

const saving = ref(false)
const loading = ref(false)

async function loadTugasan() {
  try {
    loading.value = true
    const res = await api.get("/tugasan/")
    tugasanList.value = res.data || []
  } catch (err) {
    console.error("Failed to load tugasan:", err)
    toast.error(t("common.loadFailed", { entity: t("configuration.taskList.countEntity") }))
  } finally {
    loading.value = false
  }
}

async function loadAssigned() {
  try {
    const res = await api.get(`/tugasan/profil/${profileId}`)
    selectedIds.value = res.data.map(t => t.id)
    originalIds.value = [...selectedIds.value]
  } catch (err) {
    console.error("Failed to load assigned:", err)
    toast.error(t("common.loadFailed", { entity: t("configuration.taskList.countEntity") }))
  }
}

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()

  if (!q) return tugasanList.value

  return tugasanList.value.filter(t =>
    t.nama?.toLowerCase().includes(q) ||
    t.kod?.toLowerCase().includes(q) ||
    t.protocol?.toLowerCase().includes(q)
  )
})

const allChecked = computed(() => {
  const ids = filtered.value.map(t => t.id)
  return ids.length > 0 && ids.every(id => selectedIds.value.includes(id))
})

const someChecked = computed(() => {
  const ids = filtered.value.map(t => t.id)
  return ids.some(id => selectedIds.value.includes(id)) && !allChecked.value
})

function toggleAll() {
  const ids = filtered.value.map(t => t.id)

  if (allChecked.value) {
    selectedIds.value = selectedIds.value.filter(id => !ids.includes(id))
  } else {
    selectedIds.value = [...new Set([...selectedIds.value, ...ids])]
  }
}

function openAdd() {
  editingTask.value = null
  showAdd.value = true
}

function openEdit(task) {
  showAdd.value = false
  editingTask.value = task
}

function closeSideModal() {
  showAdd.value = false
  editingTask.value = null
}

function onSaved() {
  closeSideModal()
  loadTugasan()
  toast.success(t("common.saveSuccess", { entity: t("configuration.taskList.countEntity") }))
}

async function handleSubmit() {
  try {
    saving.value = true

    const toAdd = selectedIds.value.filter(
      id => !originalIds.value.includes(id)
    )

    const toRemove = originalIds.value.filter(
      id => !selectedIds.value.includes(id)
    )

    for (const id of toAdd) {
      await api.post(`/tugasan/profil/${profileId}`, {
        tugasan_id: id,
        status: -1
      })
    }

    for (const id of toRemove) {
      await api.delete(`/tugasan/profil/${profileId}/${id}`)
    }

    emit("assigned")
    emit("close")

  } catch (err) {
    console.error("Update failed:", err)
    toast.error(t("common.saveFailed", { entity: t("configuration.taskList.countEntity") }))
  } finally {
    saving.value = false
  }
}

function protocolColor(p) {
  const map = {
    TCP: "#2563eb",
    UDP: "#7c3aed",
    HTTP: "#16a34a",
    HTTPS: "#059669",
    ICMP: "#d97706",
    SSH: "#dc2626",
    FTP: "#0891b2",
    SMTP: "#be185d"
  }

  return map[p] || "#64748b"
}

onMounted(() => {
  loadTugasan()
  loadAssigned()
})
</script>

<template>
  <div class="modal-overlay">

    <div class="modal-shell">

      <!-- MAIN MODAL -->
      <div class="modal-card">

        <!-- HEADER -->
        <div class="modal-header">

          <div>
            <p class="eyebrow">{{ t("tasks.assign.eyebrow") }}</p>
            <h2>{{ t("tasks.assign.title") }}</h2>

            <p class="subtext">
              {{ t("tasks.assign.description") }}
            </p>
          </div>

          <button
            class="ui-icon-button"
            :title="t('common.close')"
            :aria-label="t('common.close')"
            @click="$emit('close')"
          >
            <X :size="18" aria-hidden="true" />
          </button>

        </div>

        <!-- TOOLBAR -->
        <div class="toolbar">

          <div class="search-box">
            <Search class="search-icon" :size="18" aria-hidden="true" />

            <input
              v-model="search"
              type="text"
              :placeholder="t('configuration.shared.search', { entity: t('configuration.taskList.searchEntity') })"
            />
          </div>

          <button class="ui-button ui-button--primary" @click="openAdd">
            <Plus :size="18" aria-hidden="true" />
            {{ t("tasks.assign.add") }}
          </button>

        </div>

        <!-- COUNT BAR -->
        <div class="selection-bar">

          <span>
            {{ t("tasks.assign.selected", { count: selectedIds.length }) }}
          </span>

          <button
            v-if="selectedIds.length"
            class="clear-btn"
            @click="selectedIds = []"
          >
            {{ t("common.clear") }}
          </button>

        </div>

        <!-- TABLE -->
        <div class="table-wrap">

          <div class="table-head">

            <div>
              <input
                type="checkbox"
                :checked="allChecked"
                :indeterminate.prop="someChecked"
                @change="toggleAll"
              />
            </div>

            <div>{{ t("configuration.taskList.name") }}</div>
            <div>{{ t("tasks.protocol") }}</div>
            <div>{{ t("tasks.assign.ipRange") }}</div>
            <div>{{ t("common.status") }}</div>
            <div>{{ t("common.actions") }}</div>

          </div>

          <div class="table-body">

            <div v-if="loading" class="empty-state">
              {{ t("tasks.assign.loading") }}
            </div>

            <div
              v-else-if="filtered.length === 0"
              class="empty-state"
            >
              {{ t("configuration.taskList.empty") }}
            </div>

            <label
              v-for="task in filtered"
              :key="task.id"
              class="row-item"
              :class="{ active: selectedIds.includes(task.id) }"
            >

              <div>
                <input
                  type="checkbox"
                  :value="task.id"
                  v-model="selectedIds"
                />
              </div>

              <div class="task-info">
                <p class="task-name">{{ task.nama }}</p>
                <p class="task-code">{{ task.kod || t("common.emptyValue") }}</p>
              </div>

              <div>
                <span
                  class="protocol-pill"
                  :style="{
                    color: protocolColor(task.protocol),
                    borderColor: protocolColor(task.protocol) + '30'
                  }"
                >
                  {{ task.protocol || t("common.emptyValue") }}
                </span>
              </div>

              <div class="ip-range">
                {{ task.ip_start || t("common.emptyValue") }}
                <span>→</span>
                {{ task.ip_end || t("common.emptyValue") }}
              </div>

              <div>
                <span :class="task.aktif ? 'success' : 'danger'">
                  {{ task.aktif ? t("status.active") : t("status.notActive") }}
                </span>
              </div>

              <div>
                <button
                  class="ui-icon-button edit-btn"
                  :title="t('tasks.add.editTitle')"
                  :aria-label="t('tasks.add.editTitle')"
                  @click.stop="openEdit(task)"
                >
                  <Pencil :size="17" aria-hidden="true" />
                </button>
              </div>

            </label>

          </div>

        </div>

        <!-- FOOTER -->
        <div class="modal-footer">

          <button
            class="ui-button ui-button--outline"
            @click="$emit('close')"
          >
            {{ t("common.cancel") }}
          </button>

          <button
            class="ui-button ui-button--primary"
            :disabled="saving"
            @click="handleSubmit"
          >
            {{ saving ? t("common.saving") : t("tasks.assign.title") }}
          </button>

        </div>

      </div>

      <!-- SIDE MODAL -->
      <Transition name="slide">
        <AddTugasanModal
          v-if="showAdd || editingTask"
          :task="editingTask"
          @close="closeSideModal"
          @saved="onSaved"
        />
      </Transition>

    </div>

  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.18s ease;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  padding: 24px;
}

.modal-shell {
  width: 100%;
  max-width: 1200px;
  display: flex;
  gap: 18px;
  align-items: stretch;
}

.modal-card{
  flex:1;
  background:white;
  border:1px solid var(--border);
  border-radius:20px;
  box-shadow:0 1px 2px rgba(15,23,42,.04);
  display:flex;
  flex-direction:column;
  min-height:760px;
  max-height:90vh;
  overflow:hidden;
}

.modal-header{
  padding:28px;
  display:flex;
  justify-content:space-between;
  gap:18px;
  border-bottom:1px solid #F1F5F9;
}

.eyebrow{
  font-size:12px;
  font-weight:700;
  color:#4F46E5;
  letter-spacing:.12em;
  margin-bottom:10px;
}

.modal-header h2{
  font-size:28px;
  font-weight:800;
  color:#0F172A;
  margin:0;
}

.subtext{
  margin-top:8px;
  color:#64748B;
  font-size:14px;
}

.toolbar {
  padding: 20px 30px;
  display: flex;
  gap: 14px;
  justify-content: space-between;
  flex-wrap: wrap;
}

.search-box{
  flex:1;
  min-width:260px;
  height:48px;
  border:1px solid #E2E8F0;
  border-radius:14px;
  display:flex;
  align-items:center;
  gap:12px;
  padding:0 16px;
  background:white;
}

.search-box:focus-within{
  border-color:var(--color-focus-border);
  box-shadow:var(--focus-ring);
}

.search-box input {
  border: none;
  outline: none;
  width: 100%;
}

.search-icon {
  color: #94A3B8;
}

.selection-bar{
  padding:0 28px 18px;
  display:flex;
  justify-content:space-between;
  color:#64748B;
  font-size:14px;
}

.clear-btn{
  border:1px solid #FECACA;

  background:#FEF2F2;
  color:#DC2626;

  height:36px;
  padding:0 14px;

  border-radius:10px;

  font-size:13px;
  font-weight:700;

  cursor:pointer;

  transition:.15s ease;

  display:flex;
  align-items:center;
  justify-content:center;
}

.clear-btn:hover{
  background:#FEE2E2;
  border-color:#FCA5A5;
}

.table-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.table-head,
.row-item {
  display: grid;
  grid-template-columns:
    50px
    minmax(250px, 2fr)
    120px
    minmax(180px, 1.2fr)
    120px
    90px;

  gap: 16px;
  align-items: center;
}

.table-head {
  padding: 16px 30px;
  background: #F8FAFC;
  font-size: 12px;
  font-weight: 700;
  color: #64748B;
  text-transform: uppercase;
}

.table-body {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.row-item {
  padding: 18px 30px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
}

.row-item:hover{
  background:#F8FAFC;
}

.row-item.active{
  background:#EEF2FF;
}

.task-info{
  display:flex;
  flex-direction:column;
  min-width:0;
}

.task-name{
  margin:0;
  font-weight:700;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.task-code {
  margin-top: 4px;
  font-size: 12px;
  color: #6b7280;
}

.protocol-pill {
  padding: 8px 10px;
  border: 1px solid;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
}

.ip-range {
  font-size: 13px;
  color: #374151;
}

.success,
.danger{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding:6px 10px;
  border-radius:999px;
  font-size:12px;
  font-weight:700;
}

.success{
  background:#ECFDF5;
  color:#16A34A;
}

.danger{
  background:#FEF2F2;
  color:#DC2626;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #6b7280;
}

.modal-footer{
  padding:22px 30px;
  border-top:1px solid #F1F5F9;
  display:flex;
  justify-content:flex-end;
  gap:12px;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

@media (max-width: 1100px) {
  .modal-shell {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .table-head,
  .row-item {
    grid-template-columns: 50px 1fr;
  }

  .table-head div:nth-child(n+3),
  .row-item div:nth-child(n+3) {
    display: none;
  }

  .modal-footer {
    flex-direction: column;
  }

  .edit-btn {
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  }
}
</style>
