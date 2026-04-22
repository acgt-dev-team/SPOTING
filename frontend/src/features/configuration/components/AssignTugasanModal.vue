<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import AddTugasanModal from "./AddTugasanModal.vue"
import api from "../../../services/api"

const emit = defineEmits(["close", "assigned"])

const route = useRoute()
const profileId = route.params.profileId

const tugasanList = ref([])
const showAdd = ref(false)
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

function onSaved() {
  loadTugasan()
  showAdd.value = false
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
  <div class="modal-overlay" @click.self="$emit('close')">

    <div class="modal-shell">

      <!-- MAIN MODAL -->
      <div class="modal-card">

        <!-- HEADER -->
        <div class="modal-header">

          <div>
            <p class="eyebrow">PENGURUSAN TUGASAN</p>
            <h2>Tetapkan Tugasan</h2>
            <p class="subtext">
              Pilih tugasan yang ingin diberikan kepada profil ini.
            </p>
          </div>

          <button class="close-btn" @click="$emit('close')">
            ✕
          </button>

        </div>

        <!-- TOOLBAR -->
        <div class="toolbar">

          <div class="search-box">
            <span class="search-icon">⌕</span>

            <input
              v-model="search"
              type="text"
              placeholder="Carian tugasan..."
            />
          </div>

          <button class="primary-btn" @click="showAdd = true">
            + Tambah Tugasan
          </button>

        </div>

        <!-- COUNT BAR -->
        <div class="selection-bar">
          <span>
            {{ selectedIds.length }} dipilih
          </span>

          <button
            v-if="selectedIds.length"
            class="clear-btn"
            @click="selectedIds = []"
          >
            Kosongkan
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

            <div>Nama Tugasan</div>
            <div>Protokol</div>
            <div>IP Range</div>
            <div>Status</div>

          </div>

          <div class="table-body">

            <div v-if="loading" class="empty-state">
              Memuatkan tugasan...
            </div>

            <div
              v-else-if="filtered.length === 0"
              class="empty-state"
            >
              Tiada tugasan dijumpai.
            </div>

            <label
              v-for="t in filtered"
              :key="t.id"
              class="row-item"
              :class="{ active: selectedIds.includes(t.id) }"
            >

              <div>
                <input
                  type="checkbox"
                  :value="t.id"
                  v-model="selectedIds"
                />
              </div>

              <div class="task-info">
                <p class="task-name">{{ t.nama }}</p>
                <p class="task-code">{{ t.kod || "-" }}</p>
              </div>

              <div>
                <span
                  class="protocol-pill"
                  :style="{
                    color: protocolColor(t.protocol),
                    borderColor: protocolColor(t.protocol) + '30'
                  }"
                >
                  {{ t.protocol || "-" }}
                </span>
              </div>

              <div class="ip-range">
                {{ t.ip_start || "-" }}
                <span>→</span>
                {{ t.ip_end || "-" }}
              </div>

              <div>
                <span :class="t.aktif ? 'success' : 'danger'">
                  {{ t.aktif ? "Aktif" : "Tidak Aktif" }}
                </span>
              </div>

            </label>

          </div>

        </div>

        <!-- FOOTER -->
        <div class="modal-footer">

          <button
            class="outline-btn"
            @click="$emit('close')"
          >
            Batal
          </button>

          <button
            class="save-btn"
            :disabled="saving"
            @click="handleSubmit"
          >
            {{ saving ? "Menyimpan..." : "Tetapkan Tugasan" }}
          </button>

        </div>

      </div>

      <!-- SIDE MODAL -->
      <Transition name="slide">
        <AddTugasanModal
          v-if="showAdd"
          @close="showAdd = false"
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

.modal-card {
  flex: 1;
  background: #ffffff;
  border-radius: 30px;
  border: 1px solid #dbe3ff;
  box-shadow: 0 28px 70px rgba(15, 23, 42, 0.14);
  display: flex;
  flex-direction: column;
  min-height: 760px;
  overflow: hidden;
}

.modal-header {
  padding: 28px 30px 22px;
  display: flex;
  justify-content: space-between;
  gap: 18px;
  border-bottom: 1px solid #eef2ff;
}

.eyebrow {
  font-size: 12px;
  font-weight: 800;
  color: #020265;
  letter-spacing: 0.12em;
  margin-bottom: 10px;
}

.modal-header h2 {
  font-size: 30px;
  font-weight: 900;
  color: #111827;
  margin: 0;
}

.subtext {
  margin-top: 8px;
  color: #6b7280;
  font-size: 14px;
}

.close-btn {
  border: none;
  background: #f3f4f6;
  width: 46px;
  height: 46px;
  border-radius: 999px;
  cursor: pointer;
  font-size: 18px;
}

.toolbar {
  padding: 20px 30px;
  display: flex;
  gap: 14px;
  justify-content: space-between;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 260px;
  height: 54px;
  border: 1px solid #dbe3ff;
  border-radius: 18px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
}

.search-box input {
  border: none;
  outline: none;
  width: 100%;
}

.search-icon {
  color: #6b7280;
}

.primary-btn,
.save-btn {
  border: none;
  background: linear-gradient(135deg, #020265, #0b0b8f);
  color: white;
  padding: 14px 22px;
  border-radius: 16px;
  font-weight: 800;
  cursor: pointer;
}

.outline-btn {
  border: 1px solid #dbe3ff;
  background: white;
  color: #374151;
  padding: 14px 22px;
  border-radius: 16px;
  font-weight: 700;
  cursor: pointer;
}

.selection-bar {
  padding: 0 30px 16px;
  display: flex;
  justify-content: space-between;
  color: #6b7280;
  font-size: 14px;
}

.clear-btn {
  border: none;
  background: transparent;
  color: #020265;
  font-weight: 700;
  cursor: pointer;
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
  grid-template-columns: 60px 1.3fr 140px 1fr 130px;
  gap: 14px;
  align-items: center;
}

.table-head {
  padding: 16px 30px;
  background: #f4f6ff;
  font-size: 12px;
  font-weight: 800;
  color: #374151;
  text-transform: uppercase;
}

.table-body {
  overflow-y: auto;
  flex: 1;
}

.row-item {
  padding: 18px 30px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
}

.row-item:hover {
  background: #f8faff;
}

.row-item.active {
  background: #eef2ff;
}

.task-name {
  margin: 0;
  font-weight: 800;
  color: #111827;
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

.success {
  color: #16a34a;
  font-weight: 800;
}

.danger {
  color: #dc2626;
  font-weight: 800;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #6b7280;
}

.modal-footer {
  padding: 22px 30px;
  border-top: 1px solid #eef2ff;
  display: flex;
  justify-content: flex-end;
  gap: 14px;
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

  .save-btn,
  .outline-btn,
  .primary-btn {
    width: 100%;
  }
}
</style>