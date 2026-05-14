<script setup>
import { ref, computed, onMounted, watch } from "vue"
import api from "../../services/api"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"
import AppSelect from "../../ui/AppSelect.vue"
import AppPagination from "../../ui/AppPagination.vue"

const search = ref("")
const showModal = ref(false)
const showDeleteModal = ref(false)

const showPasswordModal = ref(false)
const generatedPassword = ref("")
const generatedUsername = ref("")

// ✅ TOGGLE MODAL
const showToggleModal = ref(false)
const toggleConfirmText = ref("")
const toggleTarget = ref(null)

const editingId = ref(null)
const deleteId = ref(null)
const deleteConfirmText = ref("")

const nama = ref("")
const username = ref("")
const role = ref("user")
const aktif = ref(true)
const currentRole = localStorage.getItem("role")

const accounts = ref([])
const errors = ref({})

const currentPage = ref(1)
const pageSize = 10

const totalPages = computed(() => {
  return Math.ceil(filteredAccounts.value.length / pageSize)
})

const filteredAccounts = computed(() => {
  return accounts.value
  .slice()
  .sort((a, b) => a.id - b.id) // ascending (stable)
  .filter((item) =>
    item.nama.toLowerCase().includes(search.value.toLowerCase()) ||
    item.username.toLowerCase().includes(search.value.toLowerCase()) ||
    item.role.toLowerCase().includes(search.value.toLowerCase())
  )
})

watch(search, () => {
  currentPage.value = 1
})

const paginatedAccounts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredAccounts.value.slice(start, start + pageSize)
})

const selectedAccount = computed(() =>
  accounts.value.find((item) => item.id === deleteId.value)
)

const canDelete = computed(() =>
  deleteConfirmText.value.trim().toLowerCase() === "padam"
)

// ✅ Toggle keyword logic
const toggleKeyword = computed(() =>
  toggleTarget.value?.aktif ? "Nyahaktif" : "Aktifkan"
)

const toggleKeywordLower = computed(() =>
  toggleKeyword.value.toLowerCase()
)

const canToggle = computed(() =>
  toggleConfirmText.value.trim().toLowerCase() === toggleKeywordLower.value
)
function resetForm() {
  nama.value = ""
  username.value = ""
  role.value = "user"
  aktif.value = true
}

function openModal() {
  editingId.value = null
  resetForm()
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function validateForm() {
  const e = {}

  if (!nama.value.trim()) {
    e.nama = "Nama diperlukan"
  }

  if (!username.value.trim()) {
    e.username = "Nama pengguna diperlukan"
  }

  errors.value = e

  return Object.keys(e).length === 0
}

function editAccount(item) {
  editingId.value = item.id
  nama.value = item.nama
  username.value = item.username
  role.value = item.role
  aktif.value = item.aktif ?? true
  showModal.value = true
}

async function fetchAccounts() {
  try {
    const res = await api.get("/auth/users")
    accounts.value = res.data
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  fetchAccounts()
})

async function saveAccount() {

  // ✅ VALIDATION
  if (
    !nama.value.trim() ||
    !username.value.trim()
  ) {
    alert("Sila lengkapkan semua maklumat sebelum simpan.")
    return
  }

  try {

    if (editingId.value) {

      await api.put(
        `/auth/users/${editingId.value}`,
        {
          nama: nama.value,
          username: username.value,
          role: role.value,
          aktif: aktif.value
        }
      )

    } else {

      const res = await api.post("/auth/users", {
        nama: nama.value,
        username: username.value,
        role: role.value,
        aktif: aktif.value
      })

      generatedPassword.value = res.data.generated_password
      generatedUsername.value = username.value
      showPasswordModal.value = true
    }

    await fetchAccounts()

    closeModal()

  } catch (err) {
    console.error(err)
  }
}

async function askDelete(item) {
  deleteId.value = item.id
  deleteConfirmText.value = ""
  showDeleteModal.value = true
}

async function closeDeleteModal() {
  showDeleteModal.value = false
}

async function confirmDelete() {
  try {
    await api.delete(
      `/auth/users/${deleteId.value}`
    )

    await fetchAccounts()

    showDeleteModal.value = false
    showModal.value = false

  } catch (err) {
    console.error(err)
  }
}

// ✅ HANDLE TOGGLE (core logic you wanted)
function handleToggle(event, isEdit = false) {
  if (!editingId.value) {
    aktif.value = !aktif.value
    return
  }

  // ❗ stop checkbox from changing ONLY in edit mode
  if (isEdit && event) {
    event.preventDefault()
  }

  toggleTarget.value = {
    id: editingId.value,
    aktif: aktif.value
  }

  toggleConfirmText.value = ""
  showToggleModal.value = true
}

function closeToggleModal() {
  showToggleModal.value = false
}

function confirmToggle() {
  aktif.value = !toggleTarget.value.aktif
  showToggleModal.value = false
}
</script>

<template>
  <div>

    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>Pengurusan Pengguna</h2>
        <p class="section-desc">
          Sistem memaparkan senarai akaun yang telah didaftarkan bagi
          membolehkan pentadbir membuat semakan dan pengurusan akaun.
        </p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input
          v-model="search"
          type="text"
          placeholder="Carian akaun..."
        />
      </div>

      <button class="primary-btn" @click="openModal">
        Tambah Akaun
      </button>
    </div>

    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Akaun</h1>
    </div>

    <div class="table-card">
      <div class="table-scroll">

        <table>
          <thead>
            <tr>
              <th style="width:80px">BIL</th>
              <th style="width:220px">NAMA</th>
              <th style="width:160px">NAMA PENGGUNA</th>
              <th style="width:120px">PERANAN</th>
              <th style="width:120px">TINDAKAN</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="filteredAccounts.length === 0">
              <td colspan="7" class="empty-cell">
                Tiada akaun dijumpai.
              </td>
            </tr>

            <tr
              v-for="(item,index) in paginatedAccounts"
              :key="item.id"
              class="clickable-row"
            >
              <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar">
                    {{ item.nama.charAt(0).toUpperCase() }}
                  </div>

                  <div>
                    <p class="org-name">{{ item.nama }}</p>
                    <p class="org-desc">
                      {{ item.aktif ? "Aktif" : "Tidak Aktif" }}
                    </p>
                  </div>
                </div>
              </td>

              <td>{{ item.username }}</td>
              <td>
  {{
    item.role === "super admin"
      ? "Super Admin"
      : item.role === "admin"
      ? "Pentadbir"
      : "Pengguna"
  }}
</td>

              <td>
                <button
                  class="ghost-btn"
                  @click="editAccount(item)"
                >
                  ✏️
                </button>
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
      <div class="count-pill">
        Bilangan Akaun:
        <strong>
          {{ filteredAccounts.length.toString().padStart(2,"0") }}
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
              <p class="eyebrow">AKAUN SISTEM</p>
              <h2>
                {{ editingId
                  ? "Kemaskini Akaun"
                  : "Tambah Akaun"
                }}
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
              label="Nama"
              placeholder="Masukkan nama"
            />

            <AppInput
              v-model="username"
              label="Nama Pengguna"
              placeholder="Masukkan username"
            />

            <AppSelect
              v-model="role"
              label="Peranan"
              :options="
  currentRole === 'super admin'
    ? [
        { label: 'Pentadbir', value: 'admin' },
        { label: 'Pengguna', value: 'user' }
      ]
    : [
        { label: 'Pengguna', value: 'user' }
      ]
"
            />

            <!-- ✅ TOGGLE (UPDATED) -->
            <div class="field">
              <label>Status Akaun</label>

              <div class="switch-wrapper">
                <label class="switch">
                  <input
                    type="checkbox"
                    :checked="aktif"
                    @click="editingId ? handleToggle($event, true) : handleToggle()"
                  />
                  <span class="slider"></span>
                </label>

                <span class="status-text">
                  {{ aktif ? "Aktif" : "Tidak Aktif" }}
                </span>
              </div>
            </div>

          </div>

          <div class="modal-actions">

            <button
              v-if="editingId"
              class="delete-trigger-btn"
              @click="askDelete({ id: editingId })"
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
              @click="saveAccount"
            />

          </div>

        </AppCard>

      </div>
    </transition>

    <!-- DELETE MODAL -->
    <transition name="fade">
      <div
        v-if="showDeleteModal"
        class="modal-overlay"
      >

        <div class="delete-modal">

          <div class="delete-icon">🗑️</div>

          <h3>
            Padam {{ selectedAccount?.nama }}?
          </h3>

          <p class="delete-desc">
            Tindakan ini tidak boleh dibatalkan.
          </p>

          <div class="confirm-box">

            <label>
              Taip <strong>Padam</strong> untuk sahkan:
            </label>

            <div class="org-delete-name">
              <span class="danger-word">Padam</span>
            </div>

            <input
              v-model="deleteConfirmText"
              class="delete-input"
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

    <!-- ✅ TOGGLE CONFIRM MODAL -->
    <transition name="fade">
      <div
        v-if="showToggleModal"
        class="modal-overlay"
      >

        <div class="delete-modal">

          <div class="delete-icon">⚠️</div>

          <h3>
            {{ toggleTarget?.aktif
              ? "Nyahaktif akaun ini?"
              : "Aktifkan akaun ini?"
            }}
          </h3>

          <p class="delete-desc">
            Taip <strong>{{ toggleKeyword }}</strong> untuk sahkan.
          </p>

          <div class="confirm-box">

            <label>
              Sahkan tindakan:
            </label>

            <div class="org-delete-name">
              <span class="danger-word">
                {{ toggleKeyword }}
              </span>
            </div>

            <input
              v-model="toggleConfirmText"
              class="delete-input"
              :placeholder="toggleKeyword"
            />

          </div>

          <div class="delete-actions">

            <button
              class="cancel-delete-btn"
              @click="closeToggleModal"
            >
              Batal
            </button>

            <button
              class="danger-btn"
              :disabled="!canToggle"
              @click="confirmToggle"
            >
              Sahkan
            </button>

          </div>

        </div>

      </div>
    </transition>

  </div>

  <!-- PASSWORD SUCCESS MODAL -->
<transition name="fade">
  <div
    v-if="showPasswordModal"
    class="modal-overlay"
  >
    <div class="delete-modal">

      <div class="delete-icon">🔐</div>

      <h3>Akaun Berjaya Dicipta</h3>

      <p class="delete-desc">
        Kata laluan sementara hanya dipaparkan sekali.
        Sila simpan dan kongsi kepada pengguna.
      </p>

      <div class="confirm-box">

        <label>Nama Pengguna</label>

        <div class="org-delete-name">
          {{ generatedUsername }}
        </div>

        <label style="margin-top:12px">
          Kata Laluan Sementara
        </label>

        <div class="org-delete-name">
          <strong>{{ generatedPassword }}</strong>
        </div>

      </div>

      <div class="delete-actions">

        <button
          class="cancel-delete-btn"
          @click="showPasswordModal = false"
        >
          Tutup
        </button>

      </div>

    </div>
  </div>
</transition>
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
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 24px;
}

.modal-card {
  width: 100%;
  max-width: 760px;
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field label {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
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

/* DELETE MODAL */

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
  text-align: center;
}

.danger-word {
  color: #dc2626;
  font-size: 20px;
  font-weight: 900;
  letter-spacing: 0.04em;
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

/* ✅ ADDED TOGGLE SWITCH */

.switch-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.switch {
  position: relative;
  width: 44px;
  height: 24px;
}

.switch input {
  display: none;
}

.slider {
  position: absolute;
  inset: 0;
  background: #d1d5db;
  border-radius: 999px;
  cursor: pointer;
  transition: 0.25s;
}

.slider::before {
  content: "";
  position: absolute;
  width: 18px;
  height: 18px;
  left: 3px;
  top: 3px;
  background: white;
  border-radius: 50%;
  transition: 0.25s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.switch input:checked + .slider {
  background: #22c55e;
}

.switch input:checked + .slider::before {
  transform: translateX(20px);
}

.status-text {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
}

.clickable-row {
  transition: 0.18s ease;
}

.clickable-row:hover {
  background: #f4f6ff;
}

</style>