<script setup>
import { ref, computed, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import { CircleCheck, Pencil, Plus, Search, Trash2, X } from "lucide-vue-next"
import api from "../../services/api"
import { t } from "../../i18n"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"
import AppPagination from "../../ui/AppPagination.vue"

const router = useRouter()

const search = ref("")
const showModal = ref(false)
const editingId = ref(null)

const saving = ref(false)

const nama = ref("")
const keterangan = ref("")

const pegawai_tadbir = ref("")
const jawatan = ref("")

const organizations = ref([])

/* DELETE UX */
const showDeleteModal = ref(false)
const showToast = ref(false)
const deleteConfirmText = ref("")

// ✅ PAGINATION (ADDED)
const currentPage = ref(1)
const pageSize = 10

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
// FILTER (UNCHANGED)
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

// ✅ PAGINATION SLICE (ADDED)
const paginatedOrganizations = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredOrganizations.value.slice(start, start + pageSize)
})

// ✅ TOTAL PAGES (ADDED)
const totalPages = computed(() => {
  return Math.ceil(filteredOrganizations.value.length / pageSize)
})

// ✅ RESET PAGE WHEN SEARCH (ADDED)
watch(search, () => {
  currentPage.value = 1
})

// ✅ PREVENT EMPTY PAGE (ADDED)
watch(filteredOrganizations, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value || 1
  }
})

const selectedOrganization = computed(() => {
  return organizations.value.find(
    (item) => Number(item.id) === Number(editingId.value)
  )
})

const canDelete = computed(() => {
  return deleteConfirmText.value.trim().toLowerCase() === t("common.deleteKeyword").toLowerCase()
})

// =========================
// MODAL (UNCHANGED)
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
// ADD / UPDATE (UNCHANGED)
// =========================
async function saveOrganization() {
  if (saving.value) return

  if (!nama.value.trim()) {
    alert(t("validation.organizationNameRequired"))
    return
  }

  try {

    saving.value = true

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
  } finally {
    saving.value = false
  }
}

// =========================
// DELETE (UNCHANGED)
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
// NAVIGATION (UNCHANGED)
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
        <h2>{{ t("configuration.organization.title") }}</h2>
        <p class="section-desc">
          {{ t("configuration.organization.description") }}
        </p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <Search class="search-icon" :size="18" aria-hidden="true" />
        <input
          v-model="search"
          type="text"
          :placeholder="t('configuration.shared.search', { entity: t('configuration.organization.searchEntity') })"
        />
      </div>

      <button class="ui-button ui-button--primary" @click="openModal">
        <Plus :size="18" aria-hidden="true" />
        {{ t("configuration.organization.add") }}
      </button>
    </div>

    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("configuration.organization.pageTitle") }}</h1>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width:80px">{{ t("common.code") }}</th>
              <th>{{ t("configuration.organization.name") }}</th>
              <th style="width:220px">{{ t("common.officer") }}</th>
              <th style="width:180px">{{ t("dashboard.statLabels.subOrganization") }}</th>
              <th style="width:140px">{{ t("dashboard.statLabels.site") }}</th>
              <th style="width:180px">{{ t("dashboard.statLabels.task") }}</th>
              <th style="width:140px">{{ t("common.actions") }}</th>
            </tr>
          </thead>

          <tbody>

            <!-- ✅ FIXED -->
            <tr v-if="paginatedOrganizations.length === 0">
              <td colspan="7" class="empty-cell">
                {{ t("configuration.organization.empty") }}
              </td>
            </tr>

            <!-- ✅ PAGINATION LOOP -->
            <tr
              v-for="(org,index) in paginatedOrganizations"
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
                    {{ org.pegawai_tadbir || t("common.emptyValue") }}
                  </p>
                  <p class="pegawai-jawatan">
                    {{ org.jawatan || t("common.emptyValue") }}
                  </p>
                </div>
              </td>

              <td>{{ org.sub_count }}</td>
              <td>{{ org.tapak_count }}</td>
              <td>{{ org.tugasan_count }}</td>

              <td>
                <div style="display:flex; gap:8px;">
                  <button
                    class="ui-icon-button"
                    :title="t('configuration.organization.edit')"
                    :aria-label="t('configuration.organization.edit')"
                    @click.stop="editOrganization(org)"
                  >
                    <Pencil :size="17" aria-hidden="true" />
                  </button>
                </div>
              </td>

            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ✅ PAGINATION ADDED -->
    <AppPagination
      :currentPage="currentPage"
      :totalPages="totalPages"
      @update:page="currentPage = $event"
    />

    <div class="footer-bar">
      <div class="count-pill">
        {{ t("configuration.shared.count", { entity: t("configuration.organization.countEntity") }) }}
        <strong>
          {{ filteredOrganizations.length.toString().padStart(2,"0") }}
        </strong>
      </div>
    </div>

    <!-- MAIN MODAL -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay">

        <AppCard class="modal-card">

          <div class="modal-header">
            <div>
              <p class="eyebrow">{{ t("configuration.shared.addData") }}</p>
              <h2>
                {{ editingId ? t("configuration.organization.edit") : t("configuration.organization.add") }}
              </h2>
            </div>

            <button
              class="ui-icon-button"
              :title="t('common.close')"
              :aria-label="t('common.close')"
              @click="closeModal"
            >
              <X :size="18" aria-hidden="true" />
            </button>
          </div>

          <div class="form-area">

            <AppInput
              v-model="nama"
              :label="t('configuration.organization.name')"
              :placeholder="t('configuration.organization.namePlaceholder')"
            />

            <AppInput
              v-model="pegawai_tadbir"
              :label="t('common.officerAdmin')"
              :placeholder="t('configuration.organization.officerPlaceholder')"
            />

            <AppInput
              v-model="jawatan"
              :label="t('common.position')"
              :placeholder="t('common.positionPlaceholder')"
            />

            <div class="textarea-field">
              <label class="textarea-label">{{ t("common.description") }}</label>

              <textarea
                v-model="keterangan"
                rows="5"
                :placeholder="t('configuration.shared.descriptionPlaceholder')"
              ></textarea>
            </div>

          </div>

          <div class="modal-actions">

            <button
              v-if="editingId"
              class="ui-button ui-button--outline ui-button--danger"
              @click="handleDelete"
            >
              {{ t("common.delete") }}
            </button>

            <AppButton
              :text="t('common.cancel')"
              variant="outline"
              @click="closeModal"
            />

            <AppButton
  :text="saving
    ? t('common.saving')
    : editingId
      ? t('common.update')
      : t('common.save')"
  :disabled="saving"
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

          <div class="delete-icon">
            <Trash2 :size="28" aria-hidden="true" />
          </div>

          <h3>
            {{ t("common.deleteTitle", { name: selectedOrganization?.nama || t("common.emptyValue") }) }}
          </h3>

          <p class="delete-desc">
            {{ t("common.deleteWarning") }}
          </p>

          <div class="confirm-box">

            <label>
              {{ t("common.typeToConfirm", { keyword: t("common.deleteKeyword") }) }}
            </label>

            <div class="org-delete-name danger-word">
              {{ t("common.deleteKeyword") }}
            </div>

            <input
              v-model="deleteConfirmText"
              class="delete-input"
              type="text"
              :placeholder="t('common.typeKeyword', { keyword: t('common.deleteKeyword') })"
            />

          </div>

          <div class="delete-actions">

            <button
              class="ui-button ui-button--outline"
              @click="closeDeleteModal"
            >
              {{ t("common.cancel") }}
            </button>

            <button
              type="button"
              class="ui-button ui-button--danger"
              :disabled="!canDelete"
              @click="confirmDelete"
            >
              {{ t("common.deleteNow") }}
            </button>

          </div>

        </div>

      </div>
    </transition>

    <!-- TOAST -->
    <transition name="fade">
      <div v-if="showToast" class="toast-success">
        <CircleCheck :size="18" aria-hidden="true" />
        {{ t("configuration.organization.deleteSuccess") }}
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

.toolbar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:16px;
  margin-bottom:28px;
  flex-wrap:wrap;
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
  text-align:left;

  padding:18px 24px;

  border-bottom:1px solid #F1F5F9;

  color:#334155;
}

.clickable-row{
  transition:.15s;
}

.clickable-row:hover{
  background:#F8FAFC;
}

/* ORG */

.org-cell{
  display:flex;

  align-items:center;

  gap:14px;
}

.org-avatar{
  width:40px;

  height:40px;

  border-radius:12px;

  background:var(--primary);

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

  justify-content:flex-end;

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

/* Normal AppButton only */

/* Save / Update */

/* Batal */

/* KEEP PADAM RED */

/* DELETE BUTTON INSIDE EDIT MODAL */

/* DELETE MODAL */

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

.delete-actions{
  display:flex;

  justify-content:flex-end;

  gap:12px;

  margin-top:24px;
}

/* DELETE */

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

@media(max-width:768px){

.toolbar{
flex-direction:column;
align-items:stretch;
}

.search-box{
max-width:none;
}

.modal-actions,
.delete-actions{
flex-direction:column;
}

}

</style>
