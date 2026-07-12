<script setup>
import { computed, ref, watch, onMounted, onBeforeUnmount, nextTick } from "vue"
import { useRoute, useRouter } from "vue-router"
import { FileDown, Pencil, Plus } from "lucide-vue-next"
import api from "../../../src/services/api"
import { t } from "../../i18n"
import { useToast } from "../../ui/AppToast.vue"
import flatpickr from "flatpickr"
import "flatpickr/dist/flatpickr.css"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppSelect from "../../ui/AppSelect.vue"
import StatusPill from "../../ui/StatusPill.vue"
import AppPagination from "../../ui/AppPagination.vue"
import ConfigTable from "../../ui/ConfigTable.vue"
import ConfirmActionModal from "../../ui/ConfirmActionModal.vue"
import FormModal from "../../ui/FormModal.vue"
import PageHeader from "../../ui/PageHeader.vue"
import PageToolbar from "../../ui/PageToolbar.vue"

const route = useRoute()
const router = useRouter()
const toast = useToast()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId
const siteId = route.params.siteId

const search = ref("")
const profileStatusFilter = ref("")
const profileScheduleFilter = ref("")
const showModal = ref(false)
const editingId = ref(null)
const selectedProfile = ref(null)

const saving = ref(false)
const showDownloadModal = ref(false)
const downloadingReport = ref(false)
const profileForDownload = ref(null)
const downloadFormat = ref("default")

const nama = ref("")
const keterangan = ref("")
const executionType = ref("IMMEDIATE")
const cronEnabled = ref(false)

const frequency = ref("")

const cronExpression = ref("")


const selectedDate = ref("")
const selectedTime = ref("")
const showTimeDropdown = ref(false)

// FLATPICKR REF
const dateInput = ref(null)
let fpInstance = null

// =========================
// TIME SLOTS
// =========================
const timeSlots = ref([])

for (let h = 0; h < 24; h++) {
  for (let m of ["00", "30"]) {
    const hour = String(h).padStart(2, "0")
    timeSlots.value.push(`${hour}:${m}`)
  }
}

// =========================
// SITE + DATA
// =========================
const site = ref({
  id: siteId,
  name: t("configuration.profile.defaultName"),
  description: t("configuration.profile.defaultDescription")
})

const profiles = ref([])
const loading = ref(true)

/* DELETE UX */
const showDeleteModal = ref(false)
const deleteConfirmText = ref("")

// =========================
// PAGINATION
// =========================
const currentPage = ref(1)
const pageSize = 10

const tableColumns = [
  { key: "code", label: t("common.code"), width: "100px" },
  { key: "name", label: t("configuration.profile.name") },
  { key: "tasks", label: t("configuration.site.tasksTotal"), width: "140px", nowrap: true },
  { key: "status", label: t("common.status"), width: "140px" },
  { key: "schedule", label: t("schedule.scheduleExecution"), width: "180px", nowrap: true },
  { key: "scheduledTime", label: t("schedule.scheduledTime"), width: "180px", nowrap: true },
  { key: "actions", label: t("common.actions"), width: "140px", align: "center" }
]

const profileStatusFilterOptions = [
  { label: t("filters.allStatuses"), value: "" },
  { label: t("status.notStarted"), value: "belum dimulakan" },
  { label: t("status.inProcess"), value: "in process" },
  { label: t("status.scheduled"), value: "telah dijadualkan" },
  { label: t("status.completed"), value: "execution completed" },
  { label: t("status.failed"), value: "gagal" }
]

const profileScheduleFilterOptions = [
  { label: t("filters.allSchedules"), value: "" },
  { label: t("schedule.immediate"), value: "IMMEDIATE" },
  { label: t("schedule.once"), value: "SCHEDULED" },
  { label: t("schedule.cronJob"), value: "CRON" }
]

const downloadFormatOptions = [
  {
    value: "default",
    label: t("configuration.profile.downloadDefaultLabel"),
    description: t("configuration.profile.downloadDefaultDescription")
  },
  {
    value: "cyclonedx",
    label: t("configuration.profile.downloadCycloneDxLabel"),
    description: t("configuration.profile.downloadCycloneDxDescription")
  }
]

const hasProfileFilters = computed(() =>
  Boolean(profileStatusFilter.value || profileScheduleFilter.value)
)

const hasProfileQuery = computed(() =>
  Boolean(search.value.trim() || hasProfileFilters.value)
)

function normalizeProfileStatus(status) {
  const value = String(status || "").toLowerCase().trim()
  return value === "belum" ? "belum dimulakan" : value
}

function getProfileScheduleType(profile) {
  if (profile.cron_enabled) return "CRON"
  return profile.execution_type || "IMMEDIATE"
}

// =========================
// FILTER
// =========================
const filteredProfiles = computed(() => {
  const query = search.value.trim().toLowerCase()

  return profiles.value
    .filter((profile) => {
      const matchesSearch = !query || String(profile.nama || "").toLowerCase().includes(query)
      const matchesStatus =
        !profileStatusFilter.value ||
        normalizeProfileStatus(profile.execution_status) === profileStatusFilter.value
      const matchesSchedule =
        !profileScheduleFilter.value ||
        getProfileScheduleType(profile) === profileScheduleFilter.value

      return matchesSearch && matchesStatus && matchesSchedule
    })
    .sort((a, b) => {
      const kodA = (a.kod || "").toLowerCase()
      const kodB = (b.kod || "").toLowerCase()

      return kodA.localeCompare(kodB, undefined, {
        numeric: true,
        sensitivity: "base"
      })
    })
})

// =========================
// PAGINATION LOGIC
// =========================
const paginatedProfiles = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredProfiles.value.slice(start, start + pageSize)
})

const totalPages = computed(() => {
  return Math.ceil(filteredProfiles.value.length / pageSize)
})

// =========================
// WATCHERS
// =========================
watch([search, profileStatusFilter, profileScheduleFilter], () => {
  currentPage.value = 1
})

function clearProfileFilters() {
  profileStatusFilter.value = ""
  profileScheduleFilter.value = ""
}

watch(filteredProfiles, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value || 1
  }
})

watch(showModal, async (val) => {
  if (val) {
    await nextTick()

    initFlatpickr()
  }
})

watch(executionType, async (val) => {
  if (val === "SCHEDULED") {
    await nextTick()
    initFlatpickr()
  }
})

watch(cronEnabled, (enabled) => {

  if (!enabled) {

    frequency.value = ""

    cronExpression.value = ""

  }

})

function initFlatpickr() {
  if (dateInput.value) {

    if (fpInstance) {
      fpInstance.destroy()
    }

        fpInstance = flatpickr(
  dateInput.value,
  {
    dateFormat: "Y-m-d",

    minDate: "today",

    defaultDate:
      selectedDate.value || new Date(),
      onChange: (dates) => {

  if (!dates[0]) {
    selectedDate.value = ""
    return
  }

  const year = dates[0].getFullYear()
  const month = String(
    dates[0].getMonth() + 1
  ).padStart(2, "0")

  const day = String(
    dates[0].getDate()
  ).padStart(2, "0")

  selectedDate.value =
    `${year}-${month}-${day}`
}
    })
  }
}

function selectTime(time) {
  selectedTime.value = time
  showTimeDropdown.value = false
}

// =========================
// DELETE
// =========================
const selectedProfil = computed(() => {
  return profiles.value.find(
    (item) => Number(item.id) === Number(editingId.value)
  )
})

const canDelete = computed(() => {
  return deleteConfirmText.value.trim().toLowerCase() === t("common.deleteKeyword").toLowerCase()
})

const frequencyOptions = [
  {
    label: t("schedule.daily"),
    value: "DAILY"
  },
  {
    label: t("schedule.weekly"),
    value: "WEEKLY"
  },
  {
    label: t("schedule.monthly"),
    value: "MONTHLY"
  },
  {
    label: t("schedule.cronCustom"),
    value: "CUSTOM"
  }
]

function formatFrequency(profile) {
  if (profile.frequency === "DAILY") return t("schedule.daily")
  if (profile.frequency === "WEEKLY") return t("schedule.weekly")
  if (profile.frequency === "MONTHLY") return t("schedule.monthly")
  if (profile.frequency === "CUSTOM") return profile.cron_expression

  return t("common.emptyValue")
}

// =========================
// LOAD
// =========================
async function loadProfiles() {
  loading.value = true

  try {
    const res = await api.get(`/profil/tapak/${siteId}`)
    profiles.value = res.data || []
  } catch (err) {
    console.error("Error loading profiles:", err)
    toast.error(t("common.loadFailed", { entity: t("configuration.profile.countEntity") }))
  } finally {
    loading.value = false
  }
}

async function loadTapakDetail() {
  try {
    const res = await api.get(`/tapak/${siteId}`)

    site.value = {
      id: res.data.id,
      name: res.data.nama,
      description: res.data.keterangan
    }
  } catch (err) {
    console.error(err)
  }
}

// =========================
// SAVE
// =========================
async function saveProfile() {
  if (saving.value) return

  if (!nama.value.trim()) {
    toast.warning(t("validation.nameRequired"))
    return
  }

  try {
    saving.value = true
    let scheduledAt = null

    if (executionType.value === "SCHEDULED") {
      if (!selectedDate.value || !selectedTime.value) {
        toast.warning(t("validation.selectDateTime"))
        return
      }

      scheduledAt = `${selectedDate.value}T${selectedTime.value}:00`
    }

    const payload = {
      tapak_id: siteId,

      nama: nama.value,

      keterangan: keterangan.value,

      execution_type:
        executionType.value,

      scheduled_at:
        scheduledAt,

      is_scheduled:
        executionType.value ===
        "SCHEDULED",

      cron_enabled:
        cronEnabled.value,

      frequency:
        frequency.value,

      cron_expression:
        cronExpression.value
    }

    if (editingId.value) {
      await api.put(`/profil/${editingId.value}`, payload)
    } else {
      await api.post("/profil/", payload)
    }

    await loadProfiles()
    closeModal()
    toast.success(t("common.saveSuccess", { entity: t("configuration.profile.countEntity") }))

  } catch (err) {
    console.error("Error saving profile:", err)
    toast.error(t("common.saveFailed", { entity: t("configuration.profile.countEntity") }))
  }
    finally {
      saving.value = false
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
    await api.delete(`/profil/${editingId.value}`)

    await loadProfiles()

    showDeleteModal.value = false
    closeModal()

    toast.success(t("configuration.profile.deleteSuccess"))

  } catch (err) {
    console.error("Delete failed:", err)
    toast.error(t("common.deleteFailed", { entity: t("configuration.profile.countEntity") }))
  }
}

// =========================
// MODAL
// =========================
function openAddModal() {
  editingId.value = null
  selectedProfile.value = null
  nama.value = ""
  keterangan.value = ""

  executionType.value = "IMMEDIATE"
  selectedDate.value = ""
  selectedTime.value = ""
  cronEnabled.value = false
  frequency.value = ""
  cronExpression.value = ""

  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedProfile.value = null
}

function editProfile(profile) {
  selectedProfile.value = profile
  editingId.value = profile.id
  showModal.value = true

  nama.value = profile.nama || ""
  keterangan.value = profile.keterangan || ""

  executionType.value = profile.execution_type || "IMMEDIATE"

  if (profile.scheduled_at) {
    const dt = new Date(profile.scheduled_at)

    selectedDate.value =
  `${dt.getFullYear()}-${String(
    dt.getMonth() + 1
  ).padStart(2,"0")}-${String(
    dt.getDate()
  ).padStart(2,"0")}`
    selectedTime.value = dt.toTimeString().slice(0, 5)

  } else {
    const now = new Date()

selectedDate.value =
  `${now.getFullYear()}-${String(
    now.getMonth() + 1
  ).padStart(2,"0")}-${String(
    now.getDate()
  ).padStart(2,"0")}`

selectedTime.value =
  `${String(
    now.getHours()
  ).padStart(2,"0")}:${String(
    now.getMinutes()
  ).padStart(2,"0")}`
    nextTick(() => {

  if (
    fpInstance &&
    selectedDate.value
  ) {
    fpInstance.setDate(
      selectedDate.value,
      true
    )
  }

})
  }

  cronEnabled.value = profile.cron_enabled || false
  frequency.value = profile.frequency || ""
  cronExpression.value = profile.cron_expression || ""
}

function openDropdown() {
  showTimeDropdown.value = true
}

function handleClickOutside(e) {
  if (!e.target.closest(".custom-select")) {
    showTimeDropdown.value = false
  }
}

// =========================
// UTIL
// =========================
function formatDateTime(datetime) {
  if (!datetime) return "-"

  const dt = new Date(datetime)

  const date = dt.toLocaleDateString("ms-MY", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric"
  })

  const time = dt.toLocaleTimeString("ms-MY", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  })

  return `${date} ${time}`
}

// =========================
// NAV
// =========================
function goBack() {
  router.push(
    `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}`
  )
}

function goToTugasan(profile) {
  router.push(
    `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${siteId}/tugasan/${profile.id}`
  )
}

function openDownloadModal(profile) {
  profileForDownload.value = profile
  downloadFormat.value = "default"
  showDownloadModal.value = true
}

function closeDownloadModal() {
  if (downloadingReport.value) return

  showDownloadModal.value = false
  profileForDownload.value = null
  downloadFormat.value = "default"
}

function getReportFilename(response, profile, reportFormat) {
  const contentDisposition = response.headers?.["content-disposition"] || ""
  const filenameMatch = contentDisposition.match(/filename="?([^";]+)"?/i)

  if (filenameMatch?.[1]) {
    return decodeURIComponent(filenameMatch[1])
  }

  return reportFormat === "cyclonedx"
    ? `${profile.nama}-cyclonedx.json`
    : `${profile.nama}.xlsx`
}

async function getReportDownloadError(err) {
  const payload = err.response?.data

  if (payload instanceof Blob) {
    try {
      const errorBody = JSON.parse(await payload.text())
      return errorBody.detail || errorBody.message
    } catch {
      return ""
    }
  }

  return payload?.detail || payload?.message || ""
}

async function downloadReport() {
  const profile = profileForDownload.value

  if (!profile || downloadingReport.value) return

  const reportFormat = downloadFormat.value
  let completed = false

  try {
    downloadingReport.value = true

    const response = await api.post(
      `/report/profil/${profile.id}`,
      null,
      {
        params: { format: reportFormat },
        responseType: "blob"
      }
    )

    const blob = new Blob([response.data], {
      type: response.headers?.["content-type"]
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement("a")

    link.href = url
    link.download = getReportFilename(response, profile, reportFormat)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)

    completed = true
    toast.success(t("configuration.profile.downloadSuccess"))
  } catch (err) {
    console.error(err)
    toast.error(
      (await getReportDownloadError(err)) ||
      t("configuration.profile.downloadFailed")
    )
  } finally {
    downloadingReport.value = false

    if (completed) {
      closeDownloadModal()
    }
  }
}


// =========================
// INIT
// =========================
onMounted(() => {
  loadTapakDetail()
  loadProfiles()
  document.addEventListener("click", handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside)
})

</script>

<template>
  <div>

    <PageHeader
      :title="site.name"
      :description="site.description"
    />

    <PageToolbar
      v-model="search"
      :placeholder="t('configuration.shared.search', { entity: t('configuration.profile.searchEntity') })"
      :action-text="t('configuration.profile.add')"
      @action="openAddModal"
    >
      <template #filters>
        <AppSelect
          v-model="profileStatusFilter"
          :label="t('common.status')"
          :options="profileStatusFilterOptions"
        />

        <AppSelect
          v-model="profileScheduleFilter"
          :label="t('filters.schedule')"
          :options="profileScheduleFilterOptions"
        />

        <button
          v-if="hasProfileFilters"
          class="ui-button ui-button--outline"
          type="button"
          @click="clearProfileFilters"
        >
          {{ t("filters.clear") }}
        </button>
      </template>

      <template #action-icon>
        <Plus :size="18" aria-hidden="true" />
      </template>
    </PageToolbar>

    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("configuration.profile.pageTitle") }}</h1>
    </div>

    <ConfigTable
      :columns="tableColumns"
      :loading="loading"
      :empty="paginatedProfiles.length === 0"
      :empty-message="t('configuration.profile.empty')"
      :empty-action-text="hasProfileQuery ? '' : t('configuration.profile.add')"
      min-width="1060px"
      @empty-action="openAddModal"
    >

            <tr
              v-for="(profile,index) in paginatedProfiles"
              :key="profile.id"
              class="clickable-row"
              @click="goToTugasan(profile)"
            >
              <td>{{ profile.kod }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar">
                    {{ profile.nama?.charAt(0).toUpperCase() }}
                  </div>

                  <div>
                    <p class="org-name">{{ profile.nama }}</p>
                    <p class="org-desc">{{ profile.keterangan }}</p>
                  </div>
                </div>
              </td>

              <td>{{ profile.tugasan_count }}</td>

              <td>
                <StatusPill :status="profile.execution_status" />
              </td>

              <td>

  <span
    v-if="profile.cron_enabled"
  >

    {{
      formatFrequency(profile)
    }}

  </span>

  <span
    v-else-if="
      profile.execution_type ===
      'SCHEDULED'
    "
  >
    {{ t("schedule.once") }}
  </span>

  <span v-else>
    {{ t("schedule.immediate") }}
  </span>

</td>

              <td>
                <span v-if="profile.execution_type === 'SCHEDULED' && profile.scheduled_at">
                  {{ formatDateTime(profile.scheduled_at) }}
                </span>
                <span v-else>{{ t("common.emptyValue") }}</span>
              </td>

              <td class="table-cell--center">
                <div class="config-row-actions">
                  <button
                    class="ui-icon-button"
                    :title="t('configuration.profile.edit')"
                    :aria-label="t('configuration.profile.edit')"
                    @click.stop="editProfile(profile)"
                  >
                    <Pencil :size="17" aria-hidden="true" />
                  </button>

                  <button
                    class="ui-icon-button"
                    :title="t('reports.download')"
                    :aria-label="t('reports.download')"
                    @click.stop="openDownloadModal(profile)"
                  >
                    <FileDown :size="17" aria-hidden="true" />
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
        {{ t("configuration.shared.count", { entity: t("configuration.profile.countEntity") }) }}
        <strong>
          {{ filteredProfiles.length.toString().padStart(2,"0") }}
        </strong>
      </div>

    </div>

    <FormModal
      :show="showModal"
      :eyebrow="editingId ? t('configuration.shared.editData') : t('configuration.shared.addData')"
      :title="editingId ? t('configuration.profile.edit') : t('configuration.profile.add')"
      max-width="700px"
      @close="closeModal"
    >

          <div class="form-area">

            <AppInput
              v-model="nama"
              :label="t('configuration.profile.name')"
              :placeholder="t('configuration.profile.namePlaceholder')"
            />

            <div class="textarea-field">
              <label class="textarea-label">{{ t("common.description") }}</label>

              <textarea
                v-model="keterangan"
                rows="5"
                :placeholder="t('configuration.shared.descriptionPlaceholder')"
              ></textarea>
            </div>

            <div class="execution-type">
              <label class="field-label">{{ t("schedule.executionType") }}</label>

              <div class="execution-grid">

                <label class="radio-option" :class="{ active: executionType === 'IMMEDIATE' }">
                  <input
                    type="radio"
                    value="IMMEDIATE"
                    v-model="executionType"
                  />
                  <span class="radio-label">
                    {{ t("schedule.immediate") }}
                    <small>{{ t("schedule.immediateDescription") }}</small>
                  </span>
                </label>

                <div>
                  <label class="radio-option" :class="{ active: executionType === 'SCHEDULED' }">
                    <input
                      type="radio"
                      value="SCHEDULED"
                      v-model="executionType"
                    />
                    <span class="radio-label">
                      {{ t("schedule.scheduled") }}
                      <small>{{ t("schedule.scheduledDescription") }}</small>
                    </span>
                  </label>

                  <div v-show="executionType === 'SCHEDULED'" class="schedule-box">

                    <div class="schedule-field tarikh-field">
                      <label class="field-label">{{ t("schedule.date") }}</label>

                      <div class="input-wrapper">
                        <input
                          ref="dateInput"
                          type="text"
                          :placeholder="t('schedule.pickDate')"
                          class="spoting-input"
                          readonly
                        />
                      </div>
                    </div>

                    <div class="schedule-field masa-field">
                      <label class="field-label">{{ t("schedule.time") }}</label>

                      <div 
                        class="custom-select" 
                        :class="{ active: showTimeDropdown }" 
                        @click.stop="openDropdown"
                        >
                        <span :class="{ placeholder: !selectedTime }">
                          {{ selectedTime || t("schedule.pickTime") }}
                        </span>

                        <div v-if="showTimeDropdown" class="dropdown">
                          <div
                            v-for="time in timeSlots"
                            :key="time"
                            class="dropdown-item"
                            @click.stop="selectTime(time)"
                          >
                            {{ time }}
                          </div>
                        </div>
                      </div>
                    </div>

                    <label class="field-label">
  {{ t("schedule.cronJob") }}
</label>

<label class="switch">
  <input
    type="checkbox"
    v-model="cronEnabled"
  />
  <span class="slider"></span>
</label>
<AppSelect
  v-if="cronEnabled"
  v-model="frequency"
  :label="t('schedule.frequency')"
  :options="frequencyOptions"
/>

<AppInput
  v-if="cronEnabled && frequency === 'CUSTOM'"
  v-model="cronExpression"
  :label="t('schedule.cronExpression')"
  :placeholder="t('schedule.cronPlaceholder')"
/>

                  </div>
                </div>
              </div>
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
  @click="saveProfile"
            />

          </template>

    </FormModal>

    <FormModal
      :show="showDownloadModal"
      :title="t('configuration.profile.downloadFormatTitle')"
      max-width="560px"
      @close="closeDownloadModal"
    >
      <template #description>
        {{ t('configuration.profile.downloadFormatDescription', { name: profileForDownload?.nama || t('common.emptyValue') }) }}
      </template>

      <fieldset class="report-format-options">
        <legend class="sr-only">{{ t('configuration.profile.downloadFormatTitle') }}</legend>

        <label
          v-for="option in downloadFormatOptions"
          :key="option.value"
          class="report-format-option"
          :class="{ 'report-format-option--selected': downloadFormat === option.value }"
        >
          <input
            v-model="downloadFormat"
            type="radio"
            name="report-format"
            :value="option.value"
            :disabled="downloadingReport"
          />

          <span class="report-format-option__content">
            <span class="report-format-option__label">{{ option.label }}</span>
            <span class="report-format-option__description">{{ option.description }}</span>
          </span>
        </label>
      </fieldset>

      <template #actions>
        <AppButton
          :text="t('common.cancel')"
          variant="outline"
          :disabled="downloadingReport"
          @click="closeDownloadModal"
        />

        <AppButton
          :text="downloadingReport ? t('common.loading') : t('reports.download')"
          :disabled="downloadingReport"
          @click="downloadReport"
        >
          <template #icon>
            <FileDown :size="17" aria-hidden="true" />
          </template>
        </AppButton>
      </template>
    </FormModal>

    <ConfirmActionModal
      v-model="deleteConfirmText"
      :show="showDeleteModal"
      :title="t('common.deleteTitle', { name: selectedProfil?.nama || t('common.emptyValue') })"
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

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.report-format-options {
  margin: 0;
  padding: 0;
  border: 0;
  display: grid;
  gap: 12px;
}

.report-format-option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  cursor: pointer;
  transition: border-color 160ms ease, background 160ms ease, box-shadow 160ms ease;
}

.report-format-option:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
}

.report-format-option--selected {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  box-shadow: var(--focus-ring);
}

.report-format-option input {
  width: 16px;
  height: 16px;
  margin: 2px 0 0;
  accent-color: var(--color-primary);
}

.report-format-option input:disabled {
  cursor: not-allowed;
}

.report-format-option__content {
  min-width: 0;
  display: grid;
  gap: 4px;
}

.report-format-option__label {
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
}

.report-format-option__description {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  line-height: 1.45;
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

.form-area{
  width:100%;
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
  box-sizing:border-box;
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

/* Field wrapper */
.field {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

/* Label */
.field-label {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
}

/* Select wrapper (for styling + arrow control) */
.select-wrapper {
  position: relative;
}

/* RADIO GROUP (SPOTING STYLE) */
.radio-group {
  display: flex;
  gap: 12px;
  margin-top: 6px;
}

.radio-option {
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 12px;
  cursor: pointer;
  background: #ffffff;
  transition: 0.18s ease;
}

/* Hide default radio */
.radio-option input {
  margin-top: 3px;
  accent-color: var(--primary);
}

/* Hover */
.radio-option:hover {
  background: #f8fafc;
  border-color: var(--color-focus-border);
}

/* Active */
.radio-option.active {
  border-color: var(--color-focus-border);
  background: var(--primary-soft);
  box-shadow: 0 0 0 1px rgba(79, 70, 229, 0.08);
}

.radio-option.active .radio-label {
  color: var(--primary);
}

/* Text */
.radio-label {
  display: flex;
  flex-direction: column;
  font-weight: 700;
  color: #111827;
}

.radio-label small {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
}

/* SCHEDULE BOX */
.schedule-box {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.execution-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  align-items: start;
}

/* stack Tarikh + Masa under Jadualkan */
.schedule-box {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* FIELD */
.schedule-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* INPUT WRAPPER */
.input-wrapper {
  position: relative;
}

/* DATE + SELECT */
.input-wrapper input,
.input-wrapper select {
  width: 100%;
  height: 44px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 0 12px;
  font-size: 14px;
  color: #111827;
  background: #ffffff;
  transition: 0.18s ease;
  cursor: pointer;
}

/* HOVER */
.input-wrapper input:hover,
.input-wrapper select:hover {
  border-color: var(--color-focus-border);
}

/* FOCUS */
.input-wrapper input:focus,
.input-wrapper select:focus {
  outline: none;
  border-color: var(--color-focus-border);
  box-shadow: var(--focus-ring);
}

/* CUSTOM SELECT ARROW */
.input-wrapper select {
  appearance: none;
  padding-right: 34px;
}

/* Arrow icon */
.input-wrapper::after {
  content: "";
  position: absolute;
  right: 10px;
  top: 50%;
  width: 6px;
  height: 6px;
  border-right: 2px solid #6b7280;
  border-bottom: 2px solid #6b7280;
  transform: translateY(-70%) rotate(45deg);
  pointer-events: none;
}

/* DATE ICON CLEANUP (optional subtle fix) */
input[type="date"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.6;
}

/* =========================
CUSTOM TIME DROPDOWN (FIX)
========================= */
.custom-select {
  position: relative;
  width: 100%;
  height: 44px;

  border: 1px solid #e5e7eb;
  border-radius: 12px;

  padding: 0 12px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  background: #ffffff;
  cursor: pointer;

  font-size: 14px;
  color: #111827;

  transition: 0.18s ease;
}

.custom-select::after {
  content: "";
  position: absolute;
  right: 10px;
  top: 50%;
  width: 6px;
  height: 6px;
  border-right: 2px solid #6b7280;
  border-bottom: 2px solid #6b7280;
  transform: translateY(-70%) rotate(45deg);
  pointer-events: none;
}

.custom-select:hover {
  border-color: var(--color-focus-border);
}

.custom-select.active {
  border-color: var(--color-focus-border);
  box-shadow: var(--focus-ring);
}

.custom-select span.placeholder {
  color: #9ca3af;
}

.custom-select span {
  color: #111827;
}

.dropdown {
  position: absolute;
  top: 48px;
  left: 0;
  right: 0;

  max-height: 140px;
  overflow-y: auto;

  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;

  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);

  z-index: 999;
}

/* Items */
.dropdown-item {
  padding: 10px 12px;
  font-size: 14px;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #eef2ff;
}

</style>