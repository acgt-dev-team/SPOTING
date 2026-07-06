<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { CircleCheck, Pencil, Plus, Search, Trash2, X } from "lucide-vue-next"
import api from "../../services/api"
import { t } from "../../i18n"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"
import AppPagination from "../../ui/AppPagination.vue"

const route = useRoute()
const router = useRouter()

const editingId = ref(null)

const saving = ref(false)

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId

const organization = ref({
  id: organizationId,
  name: t("dashboard.statLabels.organization")
})

const subOrganization = ref({
  id: subOrganizationId,
  name: t("dashboard.statLabels.subOrganization"),
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

// ✅ PAGINATION
const currentPage = ref(1)
const pageSize = 10

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
// FILTER (UNCHANGED)
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

// ✅ PAGINATION SLICE
const paginatedSites = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredSites.value.slice(start, start + pageSize)
})

// ✅ TOTAL PAGES
const totalPages = computed(() => {
  return Math.ceil(filteredSites.value.length / pageSize)
})

// ✅ RESET PAGE
watch(search, () => {
  currentPage.value = 1
})

// ✅ PREVENT EMPTY PAGE
watch(filteredSites, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value || 1
  }
})

const isEditMode = computed(() => !!selectedSite.value)

const selectedTapak = computed(() => {
  return sites.value.find(
    (item) => Number(item.id) === Number(editingId.value)
  )
})

const canDelete = computed(() => {
  return deleteConfirmText.value.trim().toLowerCase() === t("common.deleteKeyword").toLowerCase()
})

watch(showModal, (value) => {
  if (value) {
    nama.value = selectedSite.value?.nama || ""
    keterangan.value = selectedSite.value?.keterangan || ""
    pegawai_tadbir.value = selectedSite.value?.pegawai_tadbir || ""
    jawatan.value = selectedSite.value?.jawatan || ""
  }
})

function goBack() {
  router.push(`/admin/configuration/sub-organisasi/${organizationId}`)
}

function goToProfil(site) {
  router.push(
    `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${site.id}`
  )
}

function editSite(site) {
  selectedSite.value = site
  editingId.value = site.id
  showModal.value = true
}

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

async function saveSite() {
  if (saving.value) return
  if (!nama.value.trim()) return

  try {
      saving.value = true
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
        <p class="section-desc">
          {{ organization?.name }} · {{ subOrganization?.description }}
        </p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <Search class="search-icon" :size="18" aria-hidden="true" />
        <input
          v-model="search"
          type="text"
          :placeholder="t('configuration.shared.search', { entity: t('configuration.site.searchEntity') })"
        />
      </div>

      <button
        class="ui-button ui-button--primary"
        @click="openAddModal"
      >
        <Plus :size="18" aria-hidden="true" />
        {{ t("configuration.site.add") }}
      </button>

    </div>

    <!-- Title -->
    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("configuration.site.pageTitle") }}</h1>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width:100px">{{ t("common.code") }}</th>
              <th>{{ t("configuration.site.name") }}</th>
              <th style="width:220px">{{ t("common.officer") }}</th>
              <th style="width:150px; white-space: nowrap;">
                {{ t("configuration.site.tasksTotal") }}
              </th>
              <th style="width:140px">{{ t("common.actions") }}</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="paginatedSites.length === 0">
              <td colspan="5" class="empty-cell">
                {{ t("configuration.site.empty") }}
              </td>
            </tr>

            <tr
              v-for="(site,index) in paginatedSites"
              :key="site.id"
              class="clickable-row"
              @click="goToProfil(site)"
            >
              <td>{{ site.kod }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar">
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
                    {{ site.pegawai_tadbir || t("common.emptyValue") }}
                  </p>

                  <p class="pegawai-jawatan">
                    {{ site.jawatan || t("common.emptyValue") }}
                  </p>
                </div>
              </td>

              <td>{{ site.tugasan_count }}</td>

              <td style="text-align:center">
                <div
                  style="
                    display:flex;
                    justify-content:center;
                    align-items:center;
                  "
                >
                  <button
                    class="ui-icon-button"
                    :title="t('configuration.site.edit')"
                    :aria-label="t('configuration.site.edit')"
                    @click.stop="editSite(site)"
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

    <AppPagination
      :currentPage="currentPage"
      :totalPages="totalPages"
      @update:page="currentPage = $event"
    />

    <!-- Footer -->
    <div class="footer-bar">

      <button class="ui-button ui-button--outline" @click="goBack">
        {{ t("common.back") }}
      </button>

      <div class="count-pill">
        {{ t("configuration.shared.count", { entity: t("configuration.site.countEntity") }) }}
        <strong>
          {{ filteredSites.length.toString().padStart(2,"0") }}
        </strong>
      </div>

    </div>

    <!-- MAIN MODAL -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay">

        <AppCard class="modal-card">

          <div class="modal-header">
            <div>
              <p class="eyebrow">
                {{ editingId ? t("configuration.shared.editData") : t("configuration.shared.addData") }}
              </p>

              <h2>
                {{ editingId ? t("configuration.site.edit") : t("configuration.site.add") }}
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
              :label="t('configuration.site.name')"
              :placeholder="t('configuration.site.namePlaceholder')"
            />

            <AppInput
              v-model="pegawai_tadbir"
              :label="t('common.officerAdmin')"
              :placeholder="t('configuration.site.officerPlaceholder')"
            />

            <AppInput
              v-model="jawatan"
              :label="t('common.position')"
              :placeholder="t('common.positionPlaceholder')"
            />

            <div class="textarea-field">
              <label class="textarea-label">
                {{ t("common.description") }}
              </label>

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

          <div class="delete-icon">
            <Trash2 :size="28" aria-hidden="true" />
          </div>

          <h3>
            {{ t("common.deleteTitle", { name: selectedTapak?.nama || t("common.emptyValue") }) }}
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
        {{ t("configuration.site.deleteSuccess") }}
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

/* DELETE BUTTON IN EDIT MODAL */


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

  .modal-actions,
  .delete-actions{
    flex-direction:column;
  }

}

</style>
