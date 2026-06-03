<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../../../src/services/api"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"
import AppPagination from "../../ui/AppPagination.vue"

const route = useRoute()
const router = useRouter()

const organisasiId = route.params.organizationId

const organisasi = ref({
  id: organisasiId,
  name: "",
  description: ""
})

const search = ref("")
const showModal = ref(false)
const selectedSub = ref(null)
const editingId = ref(null)

const saving = ref(false)

const nama = ref("")
const keterangan = ref("")
const pegawai_tadbir = ref("")
const jawatan = ref("")

const subs = ref([])

const isEditMode = computed(() => !!editingId.value)

/* DELETE UX */
const showDeleteModal = ref(false)
const showToast = ref(false)
const deleteConfirmText = ref("")

// ✅ PAGINATION (added)
const currentPage = ref(1)
const pageSize = 10

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
// FILTER (UNCHANGED)
// =========================
const filteredSubs = computed(() => {
  return subs.value
    .filter((sub) =>
      sub.nama?.toLowerCase().includes(search.value.toLowerCase())
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

// ✅ PAGINATION SLICE
const paginatedSubs = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredSubs.value.slice(start, start + pageSize)
})

// ✅ TOTAL PAGES
const totalPages = computed(() => {
  return Math.ceil(filteredSubs.value.length / pageSize)
})

// ✅ RESET PAGE
watch(search, () => {
  currentPage.value = 1
})

// ✅ PREVENT EMPTY PAGE
watch(filteredSubs, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value || 1
  }
})

const selectedSubRecord = computed(() => {
  return subs.value.find(
    (item) => Number(item.id) === Number(editingId.value)
  )
})

const canDelete = computed(() => {
  return deleteConfirmText.value.trim().toLowerCase() === "padam"
})

watch(showModal, (value) => {
  if (value) {
    nama.value = selectedSub.value?.nama || ""
    keterangan.value = selectedSub.value?.keterangan || ""
    pegawai_tadbir.value = selectedSub.value?.pegawai_tadbir || ""
    jawatan.value = selectedSub.value?.jawatan || ""
  }
})

function goBack() {
  router.push("/admin/configuration")
}

function goToTapak(sub) {
  router.push(`/admin/configuration/sub-organisasi/${organisasiId}/tapak/${sub.id}`)
}

function openAddModal() {
  selectedSub.value = null
  editingId.value = null

  nama.value = ""
  keterangan.value = ""
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

async function saveSub() {

  if (saving.value) return

  if (!nama.value.trim()) return

  try {
    saving.value = true
    const payload = {
      organisasi_id: organisasiId,
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
  } finally {
    saving.value = false
  }
}

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

onMounted(() => {
  loadOrganisasiDetail()
  loadSubOrganisasi()
})
</script>

<template>
  <div>

    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>{{ organisasi?.name }}</h2>

        <p class="section-desc">
          {{ organisasi?.description }}
        </p>
      </div>
    </div>
    
    <div class="toolbar">

      <div class="search-box">
        <span class="search-icon">⌕</span>

        <input
          v-model="search"
          type="text"
          placeholder="Carian sub organisasi..."
        />
      </div>

      <button
        class="primary-btn"
        @click="openAddModal"
      >
        <span class="btn-plus">+</span>
        Tambah Sub Organisasi
      </button>

    </div>

    <div class="page-heading-block">
      <h1 class="main-page-title">
        Senarai Sub Organisasi
      </h1>
    </div>

    <div class="table-card">

      <div class="table-scroll">

        <table>

          <thead>
            <tr>
              <th style="width:100px">Kod</th>
              <th>Nama Sub Organisasi</th>
              <th style="width:220px">Pegawai</th>
              <th style="width:150px">Tapak</th>
              <th style="width:140px">Tindakan</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="paginatedSubs.length === 0">

              <td colspan="5" class="empty-cell">
                Tiada sub organisasi dijumpai.
              </td>

            </tr>

            <tr
              v-for="(sub,index) in paginatedSubs"
              :key="sub.id"
              class="clickable-row"
              @click="goToTapak(sub)"
            >

              <td>{{ sub.kod }}</td>

              <td>

                <div class="org-cell">

                  <div class="org-avatar">
                    {{ sub.nama?.charAt(0).toUpperCase() }}
                  </div>

                  <div>

                    <p class="org-name">
                      {{ sub.nama }}
                    </p>

                    <p class="org-desc">
                      {{ sub.keterangan }}
                    </p>

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

              <td>
                {{ sub.tapak_count }}
              </td>

              <td style="text-align:center">
                <div
                  style="
                    display:flex;
                    justify-content:center;
                    align-items:center;
                  "
                >
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

    <AppPagination
      :currentPage="currentPage"
      :totalPages="totalPages"
      @update:page="currentPage = $event"
    />

    <div class="footer-bar">

      <button
        class="secondary-btn"
        @click="goBack"
      >
        ← Kembali
      </button>

      <div class="count-pill">

        Bilangan Sub Organisasi:

        <strong>
          {{ filteredSubs.length.toString().padStart(2,"0") }}
        </strong>

      </div>

    </div>

    <transition name="fade">

      <div
        v-if="showModal"
        class="modal-overlay"
      >

        <AppCard class="modal-card">

          <div class="modal-header">

            <div>

              <p class="eyebrow">
                {{ isEditMode ? "KEMASKINI DATA" : "TAMBAH DATA" }}
              </p>

              <h2>
                {{ isEditMode ? "Kemaskini Sub Organisasi" : "Tambah Sub Organisasi" }}
              </h2>

            </div>

            <button
              class="close-btn"
              @click="closeModal"
            >
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

              <label class="textarea-label">
                Keterangan
              </label>

              <textarea
                v-model="keterangan"
                rows="5"
                placeholder="Masukkan penerangan ringkas"
              />

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
  :text="saving
    ? 'Menyimpan...'
    : editingId
      ? 'Kemaskini'
      : 'Simpan'"
  :disabled="saving"
  @click="saveSub"
/>


          </div>

        </AppCard>

      </div>

    </transition>

    <transition name="fade">

      <div
        v-if="showDeleteModal"
        class="modal-overlay"
      >

        <div class="delete-modal">

          <div class="delete-icon">
            🗑️
          </div>

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

    <transition name="fade">

      <div
        v-if="showToast"
        class="toast-success"
      >
        ✅ Sub organisasi berjaya dipadam
      </div>

    </transition>

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

.primary-btn{
  border:none;

  background:var(--primary);

  color:white;

  padding:0 22px;

  min-height:48px;

  border-radius:12px;

  font-size:14px;

  font-weight:700;

  cursor:pointer;

  transition:.18s;

  display:inline-flex;

  align-items:center;

  justify-content:center;

  gap:8px;

  white-space:nowrap;
}

.primary-btn:hover{
  background:#4338CA;
}

.btn-plus{
  font-size:18px;

  font-weight:500;

  line-height:1;

  margin-top:-1px;
}

.secondary-btn{
  background:white;

  border:1px solid var(--border);

  color:#111827;

  padding:12px 18px;

  border-radius:12px;

  cursor:pointer;

  transition:.18s;
}

.secondary-btn:hover{
  background:#F8FAFC;
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

.ghost-btn{
  width:36px;

  height:36px;

  display:flex;

  align-items:center;

  justify-content:center;

  border:none;

  border-radius:10px;

  background:transparent;

  color:#64748B;

  cursor:pointer;

  transition:.15s;
}

.ghost-btn:hover{
  background:var(--primary-soft);

  color:var(--primary);
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
}

.modal-card{
  max-width:700px;

  width:100%;

  border-radius:20px;

  background:white;

  padding:30px !important;
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
}

.eyebrow{
  color:var(--primary);

  font-size:12px;

  letter-spacing:.12em;

  font-weight:700;
}

.close-btn{
  width:40px;

  height:40px;

  border:none;

  border-radius:12px;

  background:#F8FAFC;

  cursor:pointer;
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
}

/* APPBUTTON STYLING */

.modal-actions :deep(button){
  min-height:46px;

  border-radius:14px;

  font-weight:700;

  padding:0 20px;

  transition:.18s;
}

.modal-actions :deep(button:not(.delete-trigger-btn):not(.outline)){
  background:#4F46E5;

  color:white;

  box-shadow:
  0 8px 18px rgba(79,70,229,.18);
}

.modal-actions :deep(button:not(.delete-trigger-btn):not(.outline):hover){
  background:#4338CA;
}

.modal-actions :deep(.outline){
  background:white;

  border:1px solid #E2E8F0;

  color:#475569;
}

.modal-actions :deep(.outline:hover){
  background:#F8FAFC;
}

/* DELETE BUTTON IN EDIT MODAL */

.delete-trigger-btn{
  background:#FEF2F2;

  color:#DC2626;

  border:none;

  border-radius:14px;

  padding:12px 18px;

  font-weight:700;

  cursor:pointer;

  transition:.18s;
}

.delete-trigger-btn:hover{
  background:#FEE2E2;
}


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

.cancel-delete-btn{
  border:1px solid var(--border);

  background:white;

  border-radius:12px;

  padding:12px 18px;

  cursor:pointer;
}

.danger-btn{
  background:linear-gradient(135deg,#DC2626,#B91C1C);

  color:white;

  border:none;

  border-radius:12px;

  padding:12px 18px;

  font-weight:700;

  cursor:pointer;

  transition:.18s;
}

.danger-btn:disabled{
  background:#E5E7EB;

  color:#9CA3AF;

  cursor:not-allowed;

  opacity:1;
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

  .primary-btn{
    width:100%;
    justify-content:center;
  }

  .modal-actions,
  .delete-actions{
    flex-direction:column;
  }

}

</style>