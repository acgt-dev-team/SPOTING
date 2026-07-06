<script setup>
import { computed, ref, watch, onMounted, onBeforeUnmount, nextTick } from "vue"
import { useRoute, useRouter } from "vue-router"
import { FileDown, Pencil, Plus, Search, Trash2, X } from "lucide-vue-next"
import api from "../../../src/services/api"
import { t } from "../../i18n"
import flatpickr from "flatpickr"
import "flatpickr/dist/flatpickr.css"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"
import AppSelect from "../../ui/AppSelect.vue"
import StatusPill from "../../ui/StatusPill.vue"
import AppPagination from "../../ui/AppPagination.vue"

const route = useRoute()
const router = useRouter()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId
const siteId = route.params.siteId

const search = ref("")
const showModal = ref(false)
const editingId = ref(null)
const selectedProfile = ref(null)

const saving = ref(false)

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

/* DELETE UX */
const showDeleteModal = ref(false)
const showToast = ref(false)
const deleteConfirmText = ref("")

// =========================
// PAGINATION
// =========================
const currentPage = ref(1)
const pageSize = 10

// =========================
// FILTER
// =========================
const filteredProfiles = computed(() => {
  return profiles.value
    .filter((profile) =>
      profile.nama?.toLowerCase().includes(search.value.toLowerCase())
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
watch(search, () => {
  currentPage.value = 1
})

watch(filteredProfiles, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value || 1
  }
})

// INIT FLATPICKR WHEN MODAL OPENS (UNCHANGED except 1 line)
watch(showModal, async (val) => {
  if (val) {
    await nextTick()

    initFlatpickr() // âœ… replaced inline with helper
  }
})

/* =========================
 ADDED: WATCH executionType
========================= */
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

/* =========================
 ADDED: HELPER FUNCTION
========================= */
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
  try {
    const res = await api.get(`/profil/tapak/${siteId}`)
    profiles.value = res.data || []
  } catch (err) {
    console.error("Error loading profiles:", err)
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
  if (!nama.value.trim()) return

  try {
    saving.value = true
    let scheduledAt = null

    if (executionType.value === "SCHEDULED") {
      if (!selectedDate.value || !selectedTime.value) {
        alert(t("validation.selectDateTime"))
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

  } catch (err) {
    console.error("Error saving profile:", err)
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

    showToast.value = true

    setTimeout(() => {
      showToast.value = false
    }, 1600)

  } catch (err) {
    console.error("Delete failed:", err)
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

async function generateReport(profile) {

  try {

    const response = await api.post(
      `/report/profil/${profile.id}`,
      {},
      {
        responseType: "blob"
      }
    )

    const blob = new Blob(
      [response.data],
      {
        type:
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      }
    )

    const url =
      window.URL.createObjectURL(blob)

    const link =
      document.createElement("a")

    link.href = url

    link.download =
      `${profile.nama}.xlsx`

    document.body.appendChild(link)

    link.click()

    link.remove()

    window.URL.revokeObjectURL(url)

  } catch (err) {

    console.error(err)

    alert(t("configuration.profile.downloadFailed"))
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

    <!-- Header -->
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>{{ site.name }}</h2>
        <p class="section-desc">{{ site.description }}</p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <Search class="search-icon" :size="18" aria-hidden="true" />
        <input
          v-model="search"
          type="text"
          :placeholder="t('configuration.shared.search', { entity: t('configuration.profile.searchEntity') })"
        />
      </div>

      <button
        class="ui-button ui-button--primary"
        @click="openAddModal"
      >
        <Plus :size="18" aria-hidden="true" />
        {{ t("configuration.profile.add") }}
      </button>
    </div>

    <!-- Title -->
    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("configuration.profile.pageTitle") }}</h1>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width:100px">{{ t("common.code") }}</th>
              <th>{{ t("configuration.profile.name") }}</th>
              <th style="width:140px; white-space: nowrap;">{{ t("configuration.site.tasksTotal") }}</th>
              <th style="width:140px">{{ t("common.status") }}</th>
              <th style="width:180px">
                {{ t("schedule.scheduleExecution") }}
              </th>
              <th style="width:180px; white-space: nowrap;">{{ t("schedule.scheduledTime") }}</th>
              <th
                style="
                  width:140px;
                  padding-left:40px;
                "
              >
                {{ t("common.actions") }}
              </th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="paginatedProfiles.length === 0">
              <td colspan="6" class="empty-cell">
                {{ t("configuration.profile.empty") }}
              </td>
            </tr>

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

              <td style="text-align:center">
                <div
                  style="
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    gap:8px;
                  "
                >
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
                    @click.stop="generateReport(profile)"
                  >
                    <FileDown :size="17" aria-hidden="true" />
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
        {{ t("configuration.shared.count", { entity: t("configuration.profile.countEntity") }) }}
        <strong>
          {{ filteredProfiles.length.toString().padStart(2,"0") }}
        </strong>
      </div>

    </div>

    <!-- MAIN MODAL -->
    <transition name="fade">
      <div
        v-if="showModal"
        class="modal-overlay"
      >
        <AppCard class="modal-card">

          <div class="modal-header">
            <div>
              <p class="eyebrow">
                {{ editingId ? t("configuration.shared.editData") : t("configuration.shared.addData") }}
              </p>

              <h2>
                {{ editingId ? t("configuration.profile.edit") : t("configuration.profile.add") }}
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

              <!-- NEW GRID WRAPPER -->
              <div class="execution-grid">

                <!-- LEFT: IMMEDIATE -->
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

                <!-- RIGHT: SCHEDULED + FIELDS -->
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

                  <!-- MOVED HERE -->
                  <div v-show="executionType === 'SCHEDULED'" class="schedule-box">

                    <!-- DATE -->
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

                    <!-- TIME -->
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
                    <!-- FREQUENCY -->

<AppSelect
  v-if="cronEnabled"
  v-model="frequency"
  :label="t('schedule.frequency')"
  :options="frequencyOptions"
/>

<!-- CUSTOM CRON -->

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
  @click="saveProfile"
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
            {{ t("common.deleteTitle", { name: selectedProfil?.nama || t("common.emptyValue") }) }}
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
        {{ t("configuration.profile.deleteSuccess") }}
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
  padding:24px;
  overflow-y:auto;
}

.modal-card{
  max-width:700px;
  width:100%;
  border-radius:20px;
  background:white;
  padding:30px !important;

  max-height:95vh;
  overflow-y:auto;
}

.modal-card::-webkit-scrollbar{
  width:8px;
}

.modal-card::-webkit-scrollbar-thumb{
  background:#CBD5E1;
  border-radius:999px;
}

.modal-card::-webkit-scrollbar-track{
  background:transparent;
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
  margin:0;
}

.eyebrow{
  color:var(--primary);
  font-size:12px;
  letter-spacing:.12em;
  font-weight:700;
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
  flex-wrap:wrap;
}

/* APPBUTTON STYLING */

/* DELETE BUTTON */

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
  .delete-actions,
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
  accent-color: #020265;
}

/* Hover */
.radio-option:hover {
  background: #f8fafc;
}

/* Active */
.radio-option.active {
  border-color: #020265;
  background: #eef2ff;
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
  border-color: #c7d2fe;
}

/* FOCUS */
.input-wrapper input:focus,
.input-wrapper select:focus {
  outline: none;
  border-color: #020265;
  box-shadow: 0 0 0 3px rgba(2, 2, 101, 0.08);
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
  border-color: #c7d2fe;
}

.custom-select.active {
  border-color: #020265;
  box-shadow: 0 0 0 3px rgba(2, 2, 101, 0.08);
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
