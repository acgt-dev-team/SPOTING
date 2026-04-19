<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../../../src/services/api"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"

const route = useRoute()
const router = useRouter()

// =========================
// PARAM
// =========================
const organisasiId = route.params.organizationId

// =========================
// STATE
// =========================
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
const pegawai_tadbir = ref("")
const jawatan = ref("")

const subs = ref([])

/* DELETE UX */
const showDeleteModal = ref(false)
const showToast = ref(false)
const deleteConfirmText = ref("")

// =========================
// LOAD DATA
// =========================
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

// =========================
// COMPUTED
// =========================
const filteredSubs = computed(() => {
  return subs.value.filter((item) =>
    item?.nama?.toLowerCase().includes(search.value.toLowerCase())
  )
})

const isEditMode = computed(() => !!selectedSub.value)

const selectedSubRecord = computed(() => {
  return subs.value.find(
    (item) => Number(item.id) === Number(editingId.value)
  )
})

const canDelete = computed(() => {
  return deleteConfirmText.value.trim().toLowerCase() === "padam"
})

// =========================
// WATCH
// =========================
watch(showModal, (value) => {
  if (value) {
    nama.value = selectedSub.value?.nama || ""
    keterangan.value = selectedSub.value?.keterangan || ""
    kod.value = selectedSub.value?.kod || ""
    pegawai_tadbir.value = selectedSub.value?.pegawai_tadbir || ""
    jawatan.value = selectedSub.value?.jawatan || ""
  }
})

// =========================
// NAVIGATION
// =========================
function goBack() {
  router.push("/admin/configuration")
}

function goToTapak(sub) {
  router.push(`/admin/configuration/sub-organisasi/${organisasiId}/tapak/${sub.id}`)
}

// =========================
// MODAL
// =========================
function openAddModal() {
  selectedSub.value = null
  editingId.value = null

  nama.value = ""
  keterangan.value = ""
  kod.value = ""
  pegawai_tadbir.value = ""
  jawatan.value = ""

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

// =========================
// SAVE
// =========================
async function saveSub() {
  if (!nama.value.trim()) return

  try {
    const payload = {
      organisasi_id: organisasiId,
      kod: kod.value || "SUB-" + Date.now(),
      nama: nama.value,
      keterangan: keterangan.value,
      pegawai_tadbir: pegawai_tadbir.value,
      jawatan: jawatan.value
    }

    if (editingId.value) {
      await api.put(`/sub-organisasi/${editingId.value}`, payload)
    } else {
      await api.post("/sub-organisasi/", payload)
    }

    await loadSubOrganisasi()
    closeModal()

  } catch (err) {
    console.error("Failed to save sub organisasi:", err.response?.data || err)
  }
}

// =========================
// DELETE
// =========================
function handleDelete() {
  deleteConfirmText.value = ""
  showDeleteModal.value = true
}

function closeDeleteModal() {
  showDeleteModal.value = false
}

async function confirmDelete() {
  if (!editingId.value) return

  try {
    await api.delete(`/sub-organisasi/${editingId.value}`)

    await loadSubOrganisasi()

    showDeleteModal.value = false
    closeModal()

    showToast.value = true

    setTimeout(() => {
      showToast.value = false
    }, 1600)

  } catch (err) {
    console.error("Delete failed:", err)
  }
}

// =========================
// MOUNT
// =========================
onMounted(() => {
  loadOrganisasiDetail()
  loadSubOrganisasi()
})
</script>

<template>

  <!-- Header -->
  <div class="hierarchy-card">
    <div class="hierarchy-left">
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
      <input
        v-model="search"
        type="text"
        placeholder="Carian sub organisasi..."
      />
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
            <th style="width:80px">Bil</th>
            <th>Nama Sub Organisasi</th>
            <th style="width:220px">Pegawai</th>
            <th style="width:180px">Tapak</th>
            <th style="width:140px">Tindakan</th>
          </tr>
        </thead>

        <tbody>

          <tr v-if="filteredSubs.length === 0">
            <td colspan="5" class="empty-cell">
              Tiada sub organisasi dijumpai.
            </td>
          </tr>

          <tr
            v-for="(sub,index) in filteredSubs"
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

            <td>
              <div class="pegawai-cell">
                <p class="pegawai-name">
                  {{ sub.pegawai_tadbir || "-" }}
                </p>
                <p class="pegawai-jawatan">
                  {{ sub.jawatan || "-" }}
                </p>
              </div>
            </td>

            <td>0</td>

            <td>
              <div style="display:flex; gap:8px;">
                <button
                  class="ghost-btn"
                  @click.stop="editSub(sub)"
                >
                  ✏️
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
        {{ filteredSubs.length.toString().padStart(2,"0") }}
      </strong>
    </div>

  </div>

  <!-- Main Modal -->
  <transition name="fade">
    <div
      v-if="showModal"
      class="modal-overlay"
      @click.self="closeModal"
    >

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

          <button class="close-btn" @click="closeModal">
            ✕
          </button>

        </div>

        <div class="form-area">

          <AppInput
            v-model="nama"
            label="Nama Sub Organisasi"
            placeholder="Masukkan nama sub organisasi"
          />

          <AppInput
            v-model="kod"
            label="Kod Sub Organisasi"
            placeholder="Masukkan kod"
          />

          <AppInput
            v-model="pegawai_tadbir"
            label="Pegawai Tadbir"
            placeholder="Masukkan nama pegawai tadbir"
          />

          <AppInput
            v-model="jawatan"
            label="Jawatan"
            placeholder="Masukkan jawatan"
          />

          <div class="textarea-field">
            <label class="textarea-label">Keterangan</label>

            <textarea
              v-model="keterangan"
              rows="5"
              placeholder="Masukkan penerangan ringkas"
            ></textarea>
          </div>

        </div>

        <div class="modal-actions">

          <button
            v-if="editingId"
            class="delete-trigger-btn"
            @click="handleDelete"
          >
            Padam
          </button>

          <AppButton
            text="Batal"
            variant="outline"
            @click="closeModal"
          />

          <AppButton
            :text="isEditMode ? 'Simpan Perubahan' : 'Simpan'"
            variant="primary"
            @click="saveSub"
          />

        </div>

      </AppCard>

    </div>
  </transition>

  <!-- Delete Modal -->
  <transition name="fade">
    <div v-if="showDeleteModal" class="modal-overlay">

      <div class="delete-modal">

        <div class="delete-icon">🗑️</div>

        <h3>
          Padam {{ selectedSubRecord?.nama }}?
        </h3>

        <p class="delete-desc">
          Tindakan ini tidak boleh dibatalkan.
        </p>

        <div class="confirm-box">

          <label>
            Taip <strong>Padam</strong> untuk sahkan:
          </label>

          <div class="org-delete-name danger-word">
            Padam
          </div>

          <input
            v-model="deleteConfirmText"
            class="delete-input"
            type="text"
            placeholder="Taip Padam"
          />

        </div>

        <div class="delete-actions">

          <button
            class="cancel-delete-btn"
            @click="closeDeleteModal"
          >
            Batal
          </button>

          <button
            type="button"
            class="danger-btn"
            :disabled="!canDelete"
            @click="confirmDelete"
          >
            Padam Sekarang
          </button>

        </div>

      </div>

    </div>
  </transition>

  <!-- Toast -->
  <transition name="fade">
    <div v-if="showToast" class="toast-success">
      ✅ Sub organisasi berjaya dipadam
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
  margin: 0;
}

.org-desc {
  font-size: 13px;
  color: #6b7280;
  margin-top: 2px;
}

.pegawai-cell {
  display: flex;
  flex-direction: column;
}

.pegawai-name {
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.pegawai-jawatan {
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
  box-sizing: border-box;
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
}

.form-area {
  width: 100%;
}

.textarea-field {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
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
  color: #111827;
  resize: vertical;
  box-sizing: border-box;
  font-family: inherit;
}

textarea:focus {
  outline: none;
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

/* Delete buttons */
.delete-trigger-btn {
  border: none;
  background: #fef2f2;
  color: #dc2626;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 800;
  cursor: pointer;
}

.delete-trigger-btn:hover {
  background: #fee2e2;
}

.delete-modal {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 26px;
  border: 1px solid #e5e7eb;
  padding: 30px;
  box-shadow: 0 30px 80px rgba(15, 23, 42, 0.18);
}

.delete-icon {
  width: 70px;
  height: 70px;
  margin: 0 auto 18px;
  border-radius: 999px;
  background: #fef2f2;
  color: #dc2626;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
}

.delete-modal h3 {
  text-align: center;
  font-size: 24px;
  font-weight: 900;
  color: #111827;
  margin-bottom: 8px;
}

.delete-desc {
  text-align: center;
  color: #6b7280;
  margin-bottom: 24px;
}

.confirm-box label {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 10px;
}

.org-delete-name {
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  padding: 14px;
  border-radius: 14px;
  font-weight: 800;
  margin-bottom: 12px;
  color: #111827;
}

.delete-input {
  width: 100%;
  border: 1px solid #dbe3ff;
  border-radius: 14px;
  padding: 14px;
  font-size: 14px;
  box-sizing: border-box;
}

.delete-input:focus {
  outline: none;
  border-color: #020265;
}

.delete-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-delete-btn {
  border: 1px solid #e5e7eb;
  background: white;
  color: #374151;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
}

.cancel-delete-btn:hover {
  background: #f9fafb;
}

.danger-btn {
  border: none;
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  color: white;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 800;
  cursor: pointer;
}

.danger-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.toast-success {
  position: fixed;
  right: 24px;
  bottom: 24px;
  background: #ffffff;
  color: #111827;
  border: 1px solid #dcfce7;
  padding: 14px 18px;
  border-radius: 16px;
  box-shadow: 0 14px 32px rgba(15, 23, 42, 0.08);
  font-weight: 800;
  z-index: 2000;
}

@media (max-width: 768px) {
  .toolbar,
  .footer-bar,
  .modal-actions,
  .delete-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
  }

  .danger-btn,
  .cancel-delete-btn,
  .delete-trigger-btn {
    width: 100%;
  }
}
</style>