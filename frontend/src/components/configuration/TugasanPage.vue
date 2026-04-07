<script setup>
import { computed, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"
import AppCard from "../ui/AppCard.vue"
import ConfigurationLayout from "./ConfigurationLayout.vue"

const route = useRoute()
const router = useRouter()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId
const siteId = route.params.siteId
const profileId = route.params.profileId

const search = ref("")
const showModal = ref(false)

const nama = ref("")
const keterangan = ref("")
const status = ref("Aktif")

const profile = ref({
  id: profileId,
  name: "Profil Operasi",
  description: "Tetapan operasi tapak"
})

const tasks = ref([
  { id: 1, name: "Pengesahan akses", description: "Semakan akses pengguna", status: "Aktif" },
  { id: 2, name: "Audit tapak", description: "Pemeriksaan berkala", status: "Aktif" },
  { id: 3, name: "Semakan konfigurasi", description: "Validasi tetapan semasa", status: "Draf" }
])

const filteredTasks = computed(() => {
  return tasks.value.filter((item) =>
    item.name.toLowerCase().includes(search.value.toLowerCase())
  )
})

watch(showModal, (value) => {
  if (value) {
    nama.value = ""
    keterangan.value = ""
    status.value = "Aktif"
  }
})

function goBack() {
  router.push(`/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${siteId}`)
}

function openAddModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function saveTask() {
  if (!nama.value.trim()) return

  tasks.value.unshift({
    id: Date.now(),
    name: nama.value,
    description: keterangan.value,
    status: status.value
  })

  closeModal()
}
</script>

<template>
  <ConfigurationLayout>
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <p class="parent-label">Profil</p>
        <h2>{{ profile.name }}</h2>
        <p class="parent-desc">{{ profile.description }}</p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian tugasan..." />
      </div>

      <button class="primary-btn" @click="openAddModal">Tambah tugasan</button>
    </div>

    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Tugasan</h1>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width: 80px">Bil</th>
              <th>Nama Tugasan</th>
              <th style="width: 180px">Status</th>
              <th style="width: 140px">Tindakan</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="filteredTasks.length === 0">
              <td colspan="4" class="empty-cell">Tiada tugasan dijumpai.</td>
            </tr>

            <tr v-for="(task, index) in filteredTasks" :key="task.id" class="clickable-row">
              <td>{{ index + 1 }}</td>

              <td>
                <div>
                  <p class="org-name">{{ task.name }}</p>
                  <p class="org-desc">{{ task.description }}</p>
                </div>
              </td>

              <td>
                <span class="status-pill" :class="{ draft: task.status === 'Draf' }">
                  {{ task.status }}
                </span>
              </td>

              <td>
                <button class="ghost-btn">
                  Buka →
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="footer-bar">
      <button class="secondary-btn" @click="goBack">← Kembali</button>

      <div class="count-pill">
        Bilangan Tugasan:
        <strong>{{ filteredTasks.length.toString().padStart(2, "0") }}</strong>
      </div>
    </div>

    <!-- Modal -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <AppCard class="modal-card">
          <div class="modal-header">
            <div>
              <p class="eyebrow">TAMBAH DATA</p>
              <h2>Tambah Tugasan</h2>
            </div>

            <button class="close-btn" @click="closeModal">✕</button>
          </div>

          <div class="form-area">
            <AppInput
              v-model="nama"
              label="Nama Tugasan"
              placeholder="Masukkan nama tugasan"
            />

            <div class="textarea-field">
              <label class="textarea-label">Keterangan</label>
              <textarea
                v-model="keterangan"
                rows="5"
                placeholder="Masukkan penerangan ringkas"
              />
            </div>

            <div class="select-field">
              <label class="textarea-label">Status</label>
              <select v-model="status">
                <option value="Aktif">Aktif</option>
                <option value="Draf">Draf</option>
              </select>
            </div>
          </div>

          <div class="modal-actions">
            <AppButton text="Batal" variant="outline" @click="closeModal" />
            <AppButton text="Simpan" variant="primary" @click="saveTask" />
          </div>
        </AppCard>
      </div>
    </transition>
  </ConfigurationLayout>
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
  font-family: "Trebuchet MS", "Segoe UI", "Inter", sans-serif;
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

.table-card {
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid #dbe3ff;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.06);
}

.table-scroll {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
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
</style>