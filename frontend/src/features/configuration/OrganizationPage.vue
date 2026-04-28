<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"


const router = useRouter()

const search = ref("")
const showModal = ref(false)
const editingId = ref(null)

const nama = ref("")
const keterangan = ref("")

const pegawai_tadbir = ref("")
const jawatan = ref("")

const organizations = ref([])

/* DELETE UX */
const showDeleteModal = ref(false)
const showToast = ref(false)
const deleteConfirmText = ref("")

// =========================
// LOAD DATA
// =========================
async function loadOrganisasi() {
  try {
    const res = await api.get("/organisasi/pelanggan/1")
    organizations.value = res.data || []
  } catch (err) {
    console.error("Failed to load organisasi:", err)
  }
}

// =========================
// FILTER
// =========================
const filteredOrganizations = computed(() => {
  return organizations.value
    .filter((org) =>
      org.nama?.toLowerCase().includes(search.value.toLowerCase())
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

const selectedOrganization = computed(() => {
  return organizations.value.find(
    (item) => Number(item.id) === Number(editingId.value)
  )
})

const canDelete = computed(() => {
  return deleteConfirmText.value.trim().toLowerCase() === "padam"
})

// =========================
// MODAL
// =========================
function openModal() {
  editingId.value = null
  nama.value = ""
  keterangan.value = ""
  pegawai_tadbir.value = ""
  jawatan.value = ""
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function editOrganization(org) {
  nama.value = org.nama
  keterangan.value = org.keterangan
  pegawai_tadbir.value = org.pegawai_tadbir || ""
  jawatan.value = org.jawatan || ""
  editingId.value = org.id
  showModal.value = true
}

// =========================
// ADD / UPDATE
// =========================
async function saveOrganization() {
  if (!nama.value.trim()) {
    alert("Nama organisasi wajib diisi")
    return
  }

  try {
    const payload = {
      pelanggan_id: 1,
      nama: nama.value,
      keterangan: keterangan.value,
      pegawai_tadbir: pegawai_tadbir.value,
      jawatan: jawatan.value
    }

    if (editingId.value) {
      await api.put(`/organisasi/${editingId.value}`, payload)
    } else {
      await api.post("/organisasi/", payload)
    }

    await loadOrganisasi()
    closeModal()

  } catch (err) {
    console.error("Save failed:", err)
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
    await api.delete(`/organisasi/${editingId.value}`)

    await loadOrganisasi()

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
// NAVIGATION
// =========================
function goToSubOrganisasi(org) {
  router.push(`/admin/configuration/sub-organisasi/${org.id}`)
}

onMounted(() => {
  loadOrganisasi()
})
</script>

<template>
  <div>

    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>Kementerian Dalam Negeri</h2>
        <p class="section-desc">
          Urus organisasi utama dalam sistem Spoting.
        </p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian organisasi..." />
      </div>

      <button class="primary-btn" @click="openModal">
        Tambah organisasi
      </button>
    </div>

    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Organisasi</h1>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width:80px">Kod</th>
              <th>Nama Organisasi</th>
              <th style="width:220px">Pegawai</th>
              <th style="width:180px">Sub Organisasi</th>
              <th style="width:140px">Tapak</th>
              <th style="width:180px">Tugasan</th>
              <th style="width:140px">Tindakan</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="filteredOrganizations.length === 0">
              <td colspan="7" class="empty-cell">
                Tiada organisasi dijumpai.
              </td>
            </tr>

            <tr
              v-for="(org,index) in filteredOrganizations"
              :key="org.id"
              class="clickable-row"
              @click="goToSubOrganisasi(org)"
            >
              <td>{{ org.kod }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar">
                    {{ org.nama?.charAt(0).toUpperCase() }}
                  </div>

                  <div>
                    <p class="org-name">{{ org.nama }}</p>
                    <p class="org-desc">{{ org.keterangan }}</p>
                  </div>
                </div>
              </td>

              <td>
  <div class="pegawai-cell">
    <p class="pegawai-name">
      {{ org.pegawai_tadbir || "-" }}
    </p>
    <p class="pegawai-jawatan">
      {{ org.jawatan || "-" }}
    </p>
  </div>
</td>

<td>{{ org.sub_count }}</td>
<td>{{ org.tapak_count }}</td>

<td>{{ org.tugasan_count }}</td>

              <td>
                <div style="display:flex; gap:8px;">
                  <button class="ghost-btn" @click.stop="editOrganization(org)">
                    ✏️
                  </button>
                </div>
              </td>

            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="footer-bar">
      <div class="count-pill">
        Bilangan Organisasi:
        <strong>
          {{ filteredOrganizations.length.toString().padStart(2,"0") }}
        </strong>
      </div>
    </div>

    <!-- MAIN MODAL -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">

        <AppCard class="modal-card">

          <div class="modal-header">
            <div>
              <p class="eyebrow">TAMBAH DATA</p>
              <h2>
                {{ editingId ? "Kemaskini Organisasi" : "Tambah Organisasi" }}
              </h2>
            </div>

            <button class="close-btn" @click="closeModal">✕</button>
          </div>

          <div class="form-area">

          

            <AppInput
              v-model="nama"
              label="Nama Organisasi"
              placeholder="Masukkan nama organisasi"
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
              :text="editingId ? 'Kemaskini' : 'Simpan'"
              @click="saveOrganization"
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
            Padam {{ selectedOrganization?.nama }}?
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
        ✅ Organisasi berjaya dipadam
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
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid #dbe3ff;
  border-radius: 30px;
  padding: 30px;
  margin-bottom: 28px;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.06);
  flex-wrap: wrap;
}

.hierarchy-left {
  flex: 1;
  min-width: 280px;
}

.hierarchy-left h2 {
  font-size: 32px;
  font-weight: 900;
  color: #111827;
  margin-bottom: 12px;
}

.section-desc {
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

.org-avatar {
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

.success {
  color: #16a34a;
  font-weight: 800;
}

.danger {
  color: #dc2626;
  font-weight: 800;
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
  justify-content: flex-end;
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

.primary-btn {
  border: none;
  padding: 14px 22px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.2s ease;
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

/* Delete trigger inside edit modal */
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

.danger-word {
  text-align: center;
  color: #dc2626;
  font-size: 20px;
  font-weight: 900;
  letter-spacing: 0.04em;
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