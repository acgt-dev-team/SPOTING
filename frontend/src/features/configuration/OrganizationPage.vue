<script setup>
import { ref, computed, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
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

const router = useRouter()
const toast = useToast()

const search = ref("")
const showModal = ref(false)
const editingId = ref(null)

const saving = ref(false)

const nama = ref("")
const keterangan = ref("")

const pegawai_tadbir = ref("")
const jawatan = ref("")

const organizations = ref([])
const loading = ref(true)

/* DELETE UX */
const showDeleteModal = ref(false)
const deleteConfirmText = ref("")

const currentPage = ref(1)
const pageSize = 10

const tableColumns = [
  { key: "code", label: t("common.code"), width: "80px" },
  { key: "name", label: t("configuration.organization.name") },
  { key: "officer", label: t("common.officer"), width: "220px" },
  { key: "subOrganizations", label: t("dashboard.statLabels.subOrganization"), width: "180px", nowrap: true },
  { key: "sites", label: t("dashboard.statLabels.site"), width: "140px" },
  { key: "tasks", label: t("dashboard.statLabels.task"), width: "180px" },
  { key: "actions", label: t("common.actions"), width: "140px" }
]

// =========================
// LOAD DATA
// =========================
async function loadOrganisasi() {
  loading.value = true

  try {
    const res = await api.get("/organisasi/pelanggan/1")
    organizations.value = res.data || []
  } catch (err) {
    console.error("Failed to load organisasi:", err)
    toast.error(t("common.loadFailed", { entity: t("configuration.organization.countEntity") }))
  } finally {
    loading.value = false
  }
}

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

const paginatedOrganizations = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredOrganizations.value.slice(start, start + pageSize)
})

const totalPages = computed(() => {
  return Math.ceil(filteredOrganizations.value.length / pageSize)
})

watch(search, () => {
  currentPage.value = 1
})

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

async function saveOrganization() {
  if (saving.value) return

  if (!nama.value.trim()) {
    toast.warning(t("validation.organizationNameRequired"))
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
    toast.success(t("common.saveSuccess", { entity: t("configuration.organization.countEntity") }))

  } catch (err) {
    console.error("Save failed:", err)
    toast.error(t("common.saveFailed", { entity: t("configuration.organization.countEntity") }))
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
    await api.delete(`/organisasi/${editingId.value}`)

    await loadOrganisasi()

    showDeleteModal.value = false
    closeModal()

    toast.success(t("configuration.organization.deleteSuccess"))

  } catch (err) {
    console.error("Delete failed:", err)
    toast.error(t("common.deleteFailed", { entity: t("configuration.organization.countEntity") }))
  }
}

function goToSubOrganisasi(org) {
  router.push(`/admin/configuration/sub-organisasi/${org.id}`)
}

onMounted(() => {
  loadOrganisasi()
})
</script>

<template>
  <div>

    <PageHeader
      :title="t('configuration.organization.title')"
      :description="t('configuration.organization.description')"
    />

    <PageToolbar
      v-model="search"
      :placeholder="t('configuration.shared.search', { entity: t('configuration.organization.searchEntity') })"
      :action-text="t('configuration.organization.add')"
      @action="openModal"
    >
      <template #action-icon>
        <Plus :size="18" aria-hidden="true" />
      </template>
    </PageToolbar>

    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("configuration.organization.pageTitle") }}</h1>
    </div>

    <ConfigTable
      :columns="tableColumns"
      :loading="loading"
      :empty="paginatedOrganizations.length === 0"
      :empty-message="t('configuration.organization.empty')"
      :empty-action-text="search.trim() ? '' : t('configuration.organization.add')"
      min-width="1080px"
      @empty-action="openModal"
    >

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
                <div class="config-row-actions">
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
    </ConfigTable>

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

    <FormModal
      :show="showModal"
      :eyebrow="t('configuration.shared.addData')"
      :title="editingId ? t('configuration.organization.edit') : t('configuration.organization.add')"
      @close="closeModal"
    >

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
  @click="saveOrganization"
/>

          </template>

    </FormModal>

    <ConfirmActionModal
      v-model="deleteConfirmText"
      :show="showDeleteModal"
      :title="t('common.deleteTitle', { name: selectedOrganization?.nama || t('common.emptyValue') })"
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

