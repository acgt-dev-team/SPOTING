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
const showTemplateModal = ref(false)
const selectedTemplateProfile = ref(null)

const nama = ref("")
const keterangan = ref("")
const executionType = ref("IMMEDIATE")
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

/* =========================
 ADDED: HELPER FUNCTION
========================= */
function initFlatpickr() {
  if (dateInput.value) {
    if (fpInstance) {
      fpInstance.destroy()
    }

        flatpickr(dateInput.value, {
      dateFormat: "Y-m-d",
      minDate: "today",
      onChange: (dates) => {
        selectedDate.value = dates[0]
          ? dates[0].toISOString().split("T")[0]
          : ""
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
      execution_type: executionType.value,
      scheduled_at: scheduledAt,
      is_scheduled: executionType.value === "SCHEDULED"
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

    selectedDate.value = dt.toISOString().split("T")[0]
    selectedTime.value = dt.toTimeString().slice(0, 5)
  } else {
    selectedDate.value = ""
    selectedTime.value = ""
  }
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

function generateReport(profile) {
  selectedTemplateProfile.value = profile
  showTemplateModal.value = true
}

async function downloadReport(template) {

  try {

    const profile =
      selectedTemplateProfile.value

    const response = await api.post(
      `/report/profil/${profile.id}`,
      {
        template
      },
      {
        responseType: "blob"
      }
    )

    const blob = new Blob([response.data], {
      type:
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    })

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

    showTemplateModal.value = false

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
        <p class="parent-desc">{{ site.description }}</p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian profil..." />
      </div>

      <button class="primary-btn" @click="openAddModal">
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
              <th style="width:180px; white-space: nowrap;">Masa Dijadualkan</th>
              <th style="width:200px">Tindakan</th>
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
                <span v-if="profile.execution_type === 'SCHEDULED' && profile.scheduled_at">
                  {{ formatDateTime(profile.scheduled_at) }}
                </span>
                <span v-else>-</span>
              </td>

              <td>
                <div style="display:flex; gap:8px;">
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
        @click.self="closeModal"
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


    <!-- TEMPLATE MODAL -->
<transition name="fade">
  <div
    v-if="showTemplateModal"
    class="modal-overlay"
  >

    <div class="delete-modal">

      <h3>Pilih Template</h3>

      <p class="delete-desc">
        Sila pilih template laporan.
      </p>

      <div
        style="
          display:flex;
          flex-direction:column;
          gap:12px;
          margin-top:20px;
        "
      >

        <button
          class="primary-btn"
          @click="downloadReport('Template A')"
        >
          Template A
        </button>

        <button
          class="primary-btn"
          @click="downloadReport('Template B')"
        >
          Template B
        </button>

        <button
          class="cancel-delete-btn"
          @click="showTemplateModal = false"
        >
          Batal
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
}

.toolbar,
.footer-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.footer-bar {
  margin-top: 24px;
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

.search-box input {
  border: none;
  outline: none;
  background: transparent;
  width: 100%;
  font-size: 14px;
  color: #111827;
}

.search-icon {
  color: #6b7280;
  font-size: 18px;
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
  margin-bottom: 12px;
}

.parent-desc {
  color: #6b7280;
  font-size: 14px;
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
  border-bottom: 1px solid #f1f5f9;
  color: #111827;
}

td:nth-child(3) {
  text-align: center;
}

th:nth-child(3),
th:nth-child(4),
th:nth-child(5) {
  text-align: left;
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
  box-shadow: 0 10px 24px rgba(2, 2, 101, 0.22);
}

.org-name {
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.org-desc {
  color: #6b7280;
  font-size: 14px;
  margin-top: 2px;
}

.primary-btn,
.secondary-btn,
.ghost-btn {
  border: none;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.2s ease;
}

.primary-btn {
  padding: 14px 22px;
  background: linear-gradient(135deg, #020265, #0b0b8f);
  color: white;
  box-shadow: 0 14px 28px rgba(2, 2, 101, 0.25);
}

.primary-btn:hover {
  transform: translateY(-1px);
}

.secondary-btn {
  padding: 14px 22px;
  background: white;
  border: 1px solid #dbe3ff;
  color: #111827;
}

.secondary-btn:hover {
  background: #f4f6ff;
  transform: translateY(-1px);
}

.ghost-btn {
  padding: 10px 14px;
  background: #eef1ff;
  color: #020265;
}

.ghost-btn:hover {
  background: #dde3ff;
}

.empty-cell {
  text-align: center;
  padding: 52px 20px;
  color: #6b7280;
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
  font-weight: 900;
}

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
  margin: 0;
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
  font-weight: 800;
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

.delete-trigger-btn {
  border: none;
  background: #fef2f2;
  color: #dc2626;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 800;
  cursor: pointer;
}

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
  font-weight: 800;
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
  .delete-actions,
  .footer-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .danger-btn,
  .cancel-delete-btn,
  .delete-trigger-btn,
  .primary-btn,
  .secondary-btn {
    width: 100%;
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