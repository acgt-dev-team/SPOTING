<script setup>
import { computed, ref, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { Pencil, Plus } from "lucide-vue-next"
import api from "../../services/api"
import { t } from "../../i18n"
import { useToast } from "../../ui/AppToast.vue"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppPagination from "../../ui/AppPagination.vue"
import ConfigTable from "../../ui/ConfigTable.vue"
import ConfirmActionModal from "../../ui/ConfirmActionModal.vue"
import FormModal from "../../ui/FormModal.vue"
import PageHeader from "../../ui/PageHeader.vue"
import PageToolbar from "../../ui/PageToolbar.vue"

const route = useRoute()
const router = useRouter()
const toast = useToast()

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
const loading = ref(true)

/* DELETE UX */
const showDeleteModal = ref(false)
const deleteConfirmText = ref("")

const currentPage = ref(1)
const pageSize = 10

const tableColumns = [
  { key: "code", label: t("common.code"), width: "100px" },
  { key: "name", label: t("configuration.site.name") },
  { key: "officer", label: t("common.officer"), width: "220px" },
  { key: "tasks", label: t("configuration.site.tasksTotal"), width: "150px", nowrap: true },
  { key: "actions", label: t("common.actions"), width: "140px", align: "center" }
]

async function loadTapak() {
  loading.value = true

  try {
    const res = await api.get(`/tapak/sub/${subOrganizationId}`)
    sites.value = res.data || []
  } catch (err) {
    console.error("Failed to load tapak:", err)
    toast.error(t("common.loadFailed", { entity: t("configuration.site.countEntity") }))
  } finally {
    loading.value = false
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

const paginatedSites = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredSites.value.slice(start, start + pageSize)
})

const totalPages = computed(() => {
  return Math.ceil(filteredSites.value.length / pageSize)
})

watch(search, () => {
  currentPage.value = 1
})

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

  if (!nama.value.trim()) {
    toast.warning(t("validation.nameRequired"))
    return
  }

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
    toast.success(t("common.saveSuccess", { entity: t("configuration.site.countEntity") }))

  } catch (err) {
    console.error("Failed to save tapak:", err)
    toast.error(t("common.saveFailed", { entity: t("configuration.site.countEntity") }))
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

    toast.success(t("configuration.site.deleteSuccess"))

  } catch (err) {
    console.error("Delete failed:", err)
    toast.error(t("common.deleteFailed", { entity: t("configuration.site.countEntity") }))
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

    <PageHeader
      :title="subOrganization?.name"
      :description="`${organization?.name} · ${subOrganization?.description || ''}`"
    />

    <PageToolbar
      v-model="search"
      :placeholder="t('configuration.shared.search', { entity: t('configuration.site.searchEntity') })"
      :action-text="t('configuration.site.add')"
      @action="openAddModal"
    >
      <template #action-icon>
        <Plus :size="18" aria-hidden="true" />
      </template>
    </PageToolbar>

    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("configuration.site.pageTitle") }}</h1>
    </div>

    <ConfigTable
      :columns="tableColumns"
      :loading="loading"
      :empty="paginatedSites.length === 0"
      :empty-message="t('configuration.site.empty')"
      :empty-action-text="search.trim() ? '' : t('configuration.site.add')"
      min-width="780px"
      @empty-action="openAddModal"
    >

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

              <td class="table-cell--center">
                <div class="config-row-actions">
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
    </ConfigTable>

    <AppPagination
      :currentPage="currentPage"
      :totalPages="totalPages"
      @update:page="currentPage = $event"
    />

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

    <FormModal
      :show="showModal"
      :eyebrow="editingId ? t('configuration.shared.editData') : t('configuration.shared.addData')"
      :title="editingId ? t('configuration.site.edit') : t('configuration.site.add')"
      @close="closeModal"
    >

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

          <template #actions>

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

          </template>

    </FormModal>

    <ConfirmActionModal
      v-model="deleteConfirmText"
      :show="showDeleteModal"
      :title="t('common.deleteTitle', { name: selectedTapak?.nama || t('common.emptyValue') })"
      :keyword="t('common.deleteKeyword')"
      :disabled="!canDelete"
      @close="closeDeleteModal"
      @confirm="confirmDelete"
    />

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

  border-color:var(--color-focus-border);

  background:white;

  box-shadow:var(--focus-ring);
}

@media(max-width:768px){

  .footer-bar{
    flex-direction:column;
    align-items:stretch;
  }

}

</style>

