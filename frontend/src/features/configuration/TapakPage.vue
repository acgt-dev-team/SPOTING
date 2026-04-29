<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../../services/api"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"

const route = useRoute()
const router = useRouter()

const editingId = ref(null)

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId

const organization = ref({
  id: organizationId,
  name: "Organisasi"
})

const subOrganization = ref({
  id: subOrganizationId,
  name: "Sub Organisasi",
  description: ""
})

const search = ref("")
const showModal = ref(false)
const selectedSite = ref(null)

const nama = ref("")
const keterangan = ref("")
const pegawai_tadbir = ref("")
const jawatan = ref("")

const sites = ref([])

/* DELETE UX */
const showDeleteModal = ref(false)
const showToast = ref(false)
const deleteConfirmText = ref("")

// =========================
// LOAD DATA
// =========================
async function loadTapak() {
  try {
    const res = await api.get(`/tapak/sub/${subOrganizationId}`)
    sites.value = res.data || []
  } catch (err) {
    console.error("Failed to load tapak:", err)
  }
}

async function loadSubOrganisasiDetail() {
  try {
    const res = await api.get(`/sub-organisasi/${subOrganizationId}`)

    subOrganization.value = {
      id: res.data.id,
      name: res.data.nama,
      description: res.data.keterangan
    }
  } catch (err) {
    console.error(err)
  }
}

async function loadOrganisasiDetail() {
  try {
    const res = await api.get(`/organisasi/${organizationId}`)

    organization.value = {
      id: res.data.id,
      name: res.data.nama
    }
  } catch (err) {
    console.error(err)
  }
}

// =========================
// FILTER
// =========================
const filteredSites = computed(() => {
  return sites.value
    .filter((site) =>
      site.nama?.toLowerCase().includes(search.value.toLowerCase())
    )
    .sort((a, b) => {
      const kodA = (a.kod || "").toLowerCase()
      const kodB = (b.kod || "").toLowerCase()

      return kodA.localeCompare(kodB, undefined, {
        numeric: true,
        sensitivity: "base"
      })
    })
})

const isEditMode = computed(() => !!selectedSite.value)

const selectedTapak = computed(() => {
  return sites.value.find(
    (item) => Number(item.id) === Number(editingId.value)
  )
})

const canDelete = computed(() => {
  return deleteConfirmText.value.trim().toLowerCase() === "padam"
})

const breadcrumbs = [
  { label: "Organisasi", to: "/admin/configuration" },
  {
    label: "Sub Organisasi",
    to: `/admin/configuration/sub-organisasi/${organizationId}`
  },
  { label: "Tapak" }
]

// preload modal
watch(showModal, (value) => {
  if (value) {
    nama.value = selectedSite.value?.nama || ""
    keterangan.value = selectedSite.value?.keterangan || ""
    pegawai_tadbir.value = selectedSite.value?.pegawai_tadbir || ""
    jawatan.value = selectedSite.value?.jawatan || ""
  }
})

// =========================
// NAVIGATION
// =========================
function goBack() {
  router.push(`/admin/configuration/sub-organisasi/${organizationId}`)
}

function goToProfil(site) {
  router.push(
    `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${site.id}`
  )
}

// =========================
// EDIT
// =========================
function editSite(site) {
  selectedSite.value = site
  editingId.value = site.id
  showModal.value = true
}

// =========================
// MODAL
// =========================
function openAddModal() {
  selectedSite.value = null
  editingId.value = null
  nama.value = ""
  keterangan.value = ""
  pegawai_tadbir.value = ""
  jawatan.value = ""
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedSite.value = null
}

// =========================
// SAVE
// =========================
async function saveSite() {
  if (!nama.value.trim()) return

  try {
    const payload = {
      sub_organisasi_id: subOrganizationId,
      nama: nama.value,
      pegawai_tadbir: pegawai_tadbir.value,
      jawatan: jawatan.value,
      keterangan: keterangan.value
    }

    if (editingId.value) {
      await api.put(`/tapak/${editingId.value}`, payload)
    } else {
      await api.post("/tapak/", payload)
    }

    await loadTapak()
    closeModal()

  } catch (err) {
    console.error("Failed to save tapak:", err)
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
    await api.delete(`/tapak/${editingId.value}`)

    await loadTapak()

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
// LOAD
// =========================
onMounted(() => {
  loadOrganisasiDetail()
  loadSubOrganisasiDetail()
  loadTapak()
})
</script>

<template>
  <div>

    <!-- Header -->
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>{{ subOrganization?.name }}</h2>
        <p class="parent-desc">
          {{ organization?.name }} · {{ subOrganization?.description }}
        </p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian tapak..." />
      </div>

      <button class="primary-btn" @click="openAddModal">
        Tambah tapak
      </button>
    </div>

    <!-- Title -->
    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Tapak</h1>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width:100px">Kod</th>
              <th>Nama Tapak</th>
              <th style="width:220px">Pegawai</th>
              <th style="width:180px">Jumlah Tugasan</th>
              <th style="width:140px">Tindakan</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="filteredSites.length === 0">
              <td colspan="5" class="empty-cell">
                Tiada tapak dijumpai.
              </td>
            </tr>

            <tr
              v-for="(site,index) in filteredSites"
              :key="site.id"
              class="clickable-row"
              @click="goToProfil(site)"
            >
              <td>{{ site.kod }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar small">
                    {{ site.nama?.charAt(0).toUpperCase() }}
                  </div>

                  <div>
                    <p class="org-name">{{ site.nama }}</p>
                    <p class="org-desc">{{ site.keterangan }}</p>
                  </div>
                </div>
              </td>

              <td>
                <div class="pegawai-cell">
                  <p class="pegawai-name">
                    {{ site.pegawai_tadbir || "-" }}
                  </p>

                  <p class="pegawai-jawatan">
                    {{ site.jawatan || "-" }}
                  </p>
                </div>
              </td>

              <td>{{ site.tugasan_count }}</td>

              <td>
                <div style="display:flex; gap:8px;">
                  <button
                    class="ghost-btn"
                    @click.stop="editSite(site)"
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
        Bilangan Tapak:
        <strong>
          {{ filteredSites.length.toString().padStart(2,"0") }}
        </strong>
      </div>

    </div>

    <!-- MAIN MODAL -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">

        <AppCard class="modal-card">

          <div class="modal-header">
            <div>
              <p class="eyebrow">
                {{ editingId ? "KEMASKINI DATA" : "TAMBAH DATA" }}
              </p>

              <h2>
                {{ editingId ? "Edit Tapak" : "Tambah Tapak" }}
              </h2>
            </div>

            <button class="close-btn" @click="closeModal">
              ✕
            </button>
          </div>

          <div class="form-area">

            <AppInput
              v-model="nama"
              label="Nama Tapak"
              placeholder="Masukkan nama tapak"
            />

            <AppInput
              v-model="pegawai_tadbir"
              label="Pegawai Tadbir"
              placeholder="Masukkan pegawai"
            />

            <AppInput
              v-model="jawatan"
              label="Jawatan"
              placeholder="Masukkan jawatan"
            />

            <div class="textarea-field">
              <label class="textarea-label">
                Keterangan
              </label>

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
              :text="editingId ? 'Simpan Perubahan' : 'Simpan'"
              @click="saveSite"
            />

          </div>

        </AppCard>

      </div>
    </transition>

    <!-- DELETE MODAL -->
    <transition name="fade">
      <div v-if="showDeleteModal" class="modal-overlay">

        <div class="delete-modal">

          <div class="delete-icon">🗑️</div>

          <h3>
            Padam {{ selectedTapak?.nama }}?
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

    <!-- TOAST -->
    <transition name="fade">
      <div v-if="showToast" class="toast-success">
        ✅ Tapak berjaya dipadam
      </div>
    </transition>

  </div>
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
}

.close-btn {
  border: none;
  background: #f3f4f6;
  width: 44px;
  height: 44px;
  border-radius: 999px;
  cursor: pointer;
  font-size: 18px;
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
  background: #fff;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 14px;
  margin-top: 28px;
  flex-wrap: wrap;
}

/* Delete trigger */
.delete-trigger-btn {
  border: none;
  background: #fef2f2;
  color: #dc2626;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.18s ease;
}

.delete-trigger-btn:hover {
  background: #fee2e2;
}

/* Delete modal */
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
}

.danger-word {
  text-align: center;
  color: #dc2626;
  font-size: 20px;
  font-weight: 900;
  letter-spacing: 0.04em;
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
  .main-page-title {
    font-size: 25px;
  }

  .toolbar {
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
  }

  .modal-actions,
  .delete-actions {
    flex-direction: column;
  }

  .danger-btn,
  .cancel-delete-btn,
  .delete-trigger-btn {
    width: 100%;
  }
}
</style>