<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../../../src/services/api"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"


const route = useRoute()
const router = useRouter()

// ✅ PARAM
const organisasiId = route.params.organizationId

// ✅ SAFE OBJECT
const organisasi = ref({
  id: organisasiId,
  name: "",
  description: ""
})

const search = ref("")
const showModal = ref(false)
const selectedSub = ref(null)
const editingId = ref(null)

const nama = ref("")
const keterangan = ref("")
const kod = ref("")

const subs = ref([])

// ✅ LOAD DATA
async function loadSubOrganisasi() {
  try {
    const res = await api.get(`/sub-organisasi/organisasi/${organisasiId}`)
    subs.value = res.data || []
  } catch (err) {
    console.error("Failed to load sub organisasi:", err)
  }
}

async function loadOrganisasiDetail() {
  try {
    const res = await api.get(`/organisasi/${organisasiId}`)

    organisasi.value = {
      id: res.data.id,
      name: res.data.nama,
      description: res.data.keterangan
    }
  } catch (err) {
    console.error("Failed to load organisasi:", err)
  }
}

// ✅ FILTER SAFE
const filteredSubs = computed(() => {
  return subs.value.filter((item) =>
    item?.nama?.toLowerCase().includes(search.value.toLowerCase())
  )
})

const isEditMode = computed(() => !!selectedSub.value)

const breadcrumbs = [
  { label: "Organisasi", to: "/admin/configuration" },
  { label: "Sub Organisasi" }
]

// preload modal
watch(showModal, (value) => {
  if (value) {
nama.value = selectedSub.value?.nama || ""
keterangan.value = selectedSub.value?.keterangan || ""
kod.value = selectedSub.value?.kod || ""
  }
})

// navigation
function goBack() {
  router.push("/admin/configuration")
}

function goToTapak(sub) {
  router.push(`/admin/configuration/sub-organisasi/${organisasiId}/tapak/${sub.id}`)
}

// modal
function openAddModal() {
  selectedSub.value = null
  editingId.value = null
  nama.value = ""
  keterangan.value = ""
  kod.value = ""
  showModal.value = true
}

function editSub(sub) {
  selectedSub.value = sub
  editingId.value = sub.id
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedSub.value = null
}

// ✅ SAVE
async function saveSub() {
  if (!nama.value.trim()) return

  try {
    if (editingId.value) {
      // UPDATE
      await api.put(`/sub-organisasi/${editingId.value}/`, {
        organisasi_id: organisasiId,
        kod: kod.value || "SUB-" + Date.now(),
        nama: nama.value,
        keterangan: keterangan.value
      })
    } else {
      // CREATE
      await api.post("/sub-organisasi/", {
        organisasi_id: organisasiId,
        kod: kod.value || "SUB-" + Date.now(),
        nama: nama.value,
        keterangan: keterangan.value
      })
    }

    await loadSubOrganisasi()
    closeModal()

  } catch (err) {
    console.error("Failed to save sub organisasi:", err.response?.data || err)
  }
}

async function deleteSub(id) {
  if (!confirm("Padam sub organisasi ini?")) return

  try {
    await api.delete(`/sub-organisasi/${id}`)
    await loadSubOrganisasi()
  } catch (err) {
    console.error("Delete failed:", err)
  }
}

// load on mount
onMounted(() => {
  loadOrganisasiDetail()
  loadSubOrganisasi()
})
</script>

<template>

    <!-- Header -->
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <p class="parent-label">Organisasi</p>
        <h2>{{ organisasi?.name }}</h2>
        <p class="parent-desc">
          {{ organisasi?.description }}
        </p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian sub organisasi..." />
      </div>

      <button class="primary-btn" @click="openAddModal">
        Tambah sub organisasi
      </button>
    </div>

    <!-- Title -->
    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Sub Organisasi</h1>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width: 80px">Bil</th>
              <th>Nama Sub Organisasi</th>
              <th style="width: 180px">Tapak</th>
              <th style="width: 140px">Tindakan</th>
            </tr>
          </thead>

          <tbody>
            <!-- Empty -->
            <tr v-if="filteredSubs.length === 0">
              <td colspan="4" class="empty-cell">
                Tiada sub organisasi dijumpai.
              </td>
            </tr>

            <!-- Rows -->
            <tr
              v-for="(sub, index) in filteredSubs"
              :key="sub.id"
              class="clickable-row"
              @click="goToTapak(sub)"
            >
              <td>{{ index + 1 }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar small">
                    {{ sub.nama?.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <p class="org-name">{{ sub.nama }}</p>
                    <p class="org-desc">{{ sub.keterangan }}</p>
                  </div>
                </div>
              </td>

              <!-- Temporary count -->
              <td>0</td>

              <td>
  <div style="display:flex; gap:8px;">
    <button class="ghost-btn" @click.stop="editSub(sub)">
      ✏️
    </button>

    <button class="ghost-btn" @click.stop="deleteSub(sub.id)">
      🗑
    </button>
  </div>
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
        Bilangan Sub Organisasi:
        <strong>
          {{ filteredSubs.length.toString().padStart(2, "0") }}
        </strong>
      </div>
    </div>

    <!-- Modal -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <AppCard class="modal-card">

          <div class="modal-header">
            <div>
              <p class="eyebrow">
                {{ isEditMode ? "KEMASKINI DATA" : "TAMBAH DATA" }}
              </p>
              <h2>
                {{ isEditMode ? "Edit Sub Organisasi" : "Tambah Sub Organisasi" }}
              </h2>
            </div>

            <button class="close-btn" @click="closeModal">✕</button>
          </div>

          <div class="form-area">
            <AppInput
  v-model="kod"
  label="Kod Sub Organisasi"
  placeholder="Masukkan kod"
/>
            <AppInput
              v-model="nama"
              label="Nama Sub Organisasi"
              placeholder="Masukkan nama sub organisasi"
            />

            <div class="textarea-field">
              <label class="textarea-label">Keterangan</label>
              <textarea
                v-model="keterangan"
                rows="5"
                placeholder="Masukkan penerangan ringkas"
              />
            </div>
          </div>

          <div class="modal-actions">
            <AppButton text="Batal" variant="outline" @click="closeModal" />
            <AppButton
              :text="isEditMode ? 'Simpan Perubahan' : 'Simpan'"
              variant="primary"
              @click="saveSub"
            />
          </div>

        </AppCard>
      </div>
    </transition>
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

.toolbar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
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

.search-icon {
  color: #6b7280;
  font-size: 18px;
}

.search-box input {
  border: none;
  outline: none;
  background: transparent;
  width: 100%;
  font-size: 14px;
  color: #111827;
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

.parent-desc {
  color: #6b7280;
  font-size: 15px;
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
  letter-spacing: 0.03em;
}

td {
  padding: 18px 24px;
  font-size: 15px;
  color: #111827;
  border-bottom: 1px solid #f1f5f9;
}

.clickable-row {
  cursor: pointer;
  transition: 0.18s ease;
}

.clickable-row:hover {
  background: #f4f6ff;
}

.org-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.org-avatar.small {
  width: 44px;
  height: 44px;
  border-radius: 15px;
  background: linear-gradient(135deg, #020265, #0b0b8f);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  flex-shrink: 0;
  box-shadow: 0 10px 24px rgba(2, 2, 101, 0.22);
}

.org-name {
  font-weight: 800;
  color: #111827;
}

.org-desc {
  font-size: 13px;
  color: #6b7280;
  margin-top: 2px;
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

.empty-cell {
  text-align: center;
  padding: 52px 20px;
  color: #6b7280;
}

.footer-bar {
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
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

.secondary-btn,
.primary-btn {
  border: none;
  padding: 14px 22px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.2s ease;
}

.secondary-btn {
  background: white;
  border: 1px solid #dbe3ff;
  color: #111827;
}

.secondary-btn:hover {
  background: #f4f6ff;
  transform: translateY(-1px);
}

.primary-btn {
  background: linear-gradient(135deg, #020265, #0b0b8f);
  color: white;
  box-shadow: 0 14px 28px rgba(2, 2, 101, 0.25);
}

.primary-btn:hover {
  transform: translateY(-1px);
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

.textarea-field {
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

textarea {
  width: 100%;
  min-height: 130px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  border-radius: 18px;
  padding: 16px;
  font-size: 15px;
  outline: none;
  transition: 0.2s ease;
  color: #111827;
  resize: vertical;
  box-sizing: border-box;
  font-family: inherit;
}

textarea:focus {
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