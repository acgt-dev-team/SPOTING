<script setup>
import { computed, ref, watch, onMounted, onBeforeUnmount, nextTick } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../../../src/services/api"
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
  name: "Tapak",
  description: "Maklumat tapak"
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

    initFlatpickr() // ✅ replaced inline with helper
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
  return deleteConfirmText.value.trim().toLowerCase() === "padam"
})

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
  if (!nama.value.trim()) return

  try {
    let scheduledAt = null

    if (executionType.value === "SCHEDULED") {
      if (!selectedDate.value || !selectedTime.value) {
        alert("Sila pilih tarikh dan masa")
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

    alert("Gagal memuat turun laporan")
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
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian profil..." />
      </div>

      <button
        class="primary-btn"
        @click="openAddModal"
      >
        <span class="btn-plus">+</span>
        Tambah Profil
      </button>
    </div>

    <!-- Title -->
    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Profil</h1>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width:100px">Kod</th>
              <th>Nama Profil</th>
              <th style="width:140px; white-space: nowrap;">Jumlah Tugasan</th>
              <th style="width:140px">Status</th>
              <th style="width:180px">
                Jadual Pelaksanaan
              </th>
              <th style="width:180px; white-space: nowrap;">Masa Dijadualkan</th>
              <th
                style="
                  width:140px;
                  padding-left:40px;
                "
              >
                Tindakan
              </th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="paginatedProfiles.length === 0">
              <td colspan="6" class="empty-cell">
                Tiada profil dijumpai.
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
      profile.frequency === "DAILY"
        ? "Harian"

      : profile.frequency === "WEEKLY"
        ? "Mingguan"

      : profile.frequency === "MONTHLY"
        ? "Bulanan"

      : profile.frequency === "CUSTOM"
        ? profile.cron_expression

      : "-"
    }}

  </span>

  <span
    v-else-if="
      profile.execution_type ===
      'SCHEDULED'
    "
  >
    Sekali Sahaja
  </span>

  <span v-else>
    Segera
  </span>

</td>

              <td>
                <span v-if="profile.execution_type === 'SCHEDULED' && profile.scheduled_at">
                  {{ formatDateTime(profile.scheduled_at) }}
                </span>
                <span v-else>-</span>
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
                    class="ghost-btn"
                    @click.stop="editProfile(profile)"
                  >
                    ✏️
                  </button>

                  <button
                    class="ghost-btn"
                    @click.stop="generateReport(profile)"
                  >
                    📄
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

      <button class="secondary-btn" @click="goBack">
        ← Kembali
      </button>

      <div class="count-pill">
        Bilangan Profil:
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
                {{ editingId ? "KEMASKINI DATA" : "TAMBAH DATA" }}
              </p>

              <h2>
                {{ editingId ? "Edit Profil" : "Tambah Profil" }}
              </h2>
            </div>

            <button class="close-btn" @click="closeModal">
              ✕
            </button>
          </div>

          <div class="form-area">

            <AppInput
              v-model="nama"
              label="Nama Profil"
              placeholder="Masukkan nama profil"
            />

            <div class="textarea-field">
              <label class="textarea-label">Keterangan</label>

              <textarea
                v-model="keterangan"
                rows="5"
                placeholder="Masukkan penerangan ringkas"
              ></textarea>
            </div>

            <div class="execution-type">
              <label class="field-label">Jenis Pelaksanaan</label>

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
                    Imbas Segera
                    <small>Jalankan serta-merta</small>
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
                      Jadualkan
                      <small>Tetapkan masa pelaksanaan</small>
                    </span>
                  </label>

                  <!-- MOVED HERE -->
                  <div v-show="executionType === 'SCHEDULED'" class="schedule-box">

                    <!-- DATE -->
                    <div class="schedule-field tarikh-field">
                      <label class="field-label">Tarikh</label>

                      <div class="input-wrapper">
                        <input
                          ref="dateInput"
                          type="text"
                          placeholder="Pilih tarikh"
                          class="spoting-input"
                          readonly
                        />
                      </div>
                    </div>

                    <!-- TIME -->
                    <div class="schedule-field masa-field">
                      <label class="field-label">Masa</label>

                      <div 
                        class="custom-select" 
                        :class="{ active: showTimeDropdown }" 
                        @click.stop="openDropdown"
                        >
                        <span :class="{ placeholder: !selectedTime }">
                          {{ selectedTime || "Pilih masa" }}
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
  Cron Job
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
  label="Kekerapan"
  :options="[
    {
      label: 'Harian',
      value: 'DAILY'
    },
    {
      label: 'Mingguan',
      value: 'WEEKLY'
    },
    {
      label: 'Bulanan',
      value: 'MONTHLY'
    },
    {
      label: 'Cron Custom',
      value: 'CUSTOM'
    }
  ]"
/>

<!-- CUSTOM CRON -->

<AppInput
  v-if="cronEnabled && frequency === 'CUSTOM'"
  v-model="cronExpression"
  label='Cron Expression'
  placeholder='0 0 * * *'
/>

                  </div>
                </div>
              </div>
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

          <div class="delete-icon">🗑️</div>

          <h3>
            Padam {{ selectedProfil?.nama }}?
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
        ✅ Profil berjaya dipadam
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

.close-btn{
  width:40px;
  height:40px;
  border:none;
  border-radius:12px;
  background:#F8FAFC;
  cursor:pointer;
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

/* DELETE BUTTON */

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
  content: "▾";
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: #6b7280;
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
  content: "▾";
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: #6b7280;
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