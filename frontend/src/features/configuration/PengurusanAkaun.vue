<script setup>
import { ref, computed, onMounted, watch } from "vue"
import { KeyRound, LockKeyhole, Pencil, Plus, Search, Trash2, TriangleAlert, X } from "lucide-vue-next"
import api from "../../services/api"
import { t } from "../../i18n"

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
const passwordModalTitle = ref("")

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
const currentRole = sessionStorage.getItem("role")

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
  deleteConfirmText.value.trim().toLowerCase() === t("common.deleteKeyword").toLowerCase()
)

// ✅ Toggle keyword logic
const toggleKeyword = computed(() =>
  toggleTarget.value?.aktif ? t("accounts.deactivate") : t("accounts.activate")
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
    e.nama = t("validation.nameRequired")
  }

  if (!username.value.trim()) {
    e.username = t("validation.usernameRequired")
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

    const res = await api.get(
      `/auth/users?role=${currentRole}`
    )

    accounts.value = res.data

  } catch (err) {

    console.error(err)

  }
}

onMounted(() => {
  fetchAccounts()
})

async function saveAccount() {

  // ✅ REQUIRED FIELD VALIDATION
  if (
    !nama.value.trim() ||
    !username.value.trim()
  ) {
    alert(t("validation.completeBeforeSave"))
    return
  }

  // ✅ USERNAME VALIDATION
  const usernameRegex = /^[a-z0-9.]{12,24}$/

  if (!usernameRegex.test(username.value)) {
    alert(t("validation.usernameFormat"))
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

      passwordModalTitle.value = t("accounts.createdTitle")

generatedPassword.value =
  res.data.generated_password

generatedUsername.value =
  username.value

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
async function handleToggle(event, isEdit = false) {
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

async function confirmToggle() {

  try {

    if (toggleTarget.value.aktif) {

      await api.put(
        `/auth/users/${toggleTarget.value.id}/deactivate`
      )

      aktif.value = false

    } else {

      await api.put(
        `/auth/users/${toggleTarget.value.id}/activate`
      )

      aktif.value = true

    }

    await fetchAccounts()

    showToggleModal.value = false

  } catch (err) {

    console.error(err)

  }
}

async function resetPassword(item) {

  try {

    const res = await api.put(
      `/auth/users/${item.id}/reset-password`
    )

    passwordModalTitle.value = t("accounts.passwordResetTitle")

    generatedUsername.value =
      item.username

    generatedPassword.value =
      res.data.temporary_password

    showPasswordModal.value = true

  } catch (err) {

    console.error(err)

    alert(t("accounts.passwordResetFailed"))

  }

}
</script>

<template>
  <div>

    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>{{ t("accounts.title") }}</h2>
        <p class="section-desc">
          {{ t("accounts.description") }}
        </p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <Search class="search-icon" :size="18" aria-hidden="true" />
        <input
          v-model="search"
          type="text"
          :placeholder="t('configuration.shared.search', { entity: t('accounts.searchEntity') })"
        />
      </div>

      <button
        class="ui-button ui-button--primary"
        @click="openModal"
      >
        <Plus :size="18" aria-hidden="true" />
        {{ t("accounts.add") }}
      </button>
    </div>

    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("accounts.listTitle") }}</h1>
    </div>

    <div class="table-card">
      <div class="table-scroll">

        <table>
          <thead>
            <tr>
              <th style="width:80px">{{ t("common.tableNumber") }}</th>
              <th style="width:220px">{{ t("common.name") }}</th>
              <th style="width:160px">{{ t("auth.username") }}</th>
              <th style="width:120px">{{ t("accounts.role") }}</th>
              <th
                style="
                  width:160px;
                  text-align:center;
                "
              >
                {{ t("common.actions") }}
              </th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="filteredAccounts.length === 0">
              <td colspan="7" class="empty-cell">
                {{ t("accounts.empty") }}
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
                      {{ item.aktif ? t("status.active") : t("status.notActive") }}
                    </p>
                  </div>
                </div>
              </td>

              <td>{{ item.username }}</td>
              <td>
  {{
    item.role === "super admin"
      ? t("accounts.roles.superAdmin")
      : item.role === "admin"
      ? t("accounts.roles.admin")
      : t("accounts.roles.user")
  }}
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
                :title="t('accounts.edit')"
                :aria-label="t('accounts.edit')"
                @click="editAccount(item)"
              >
                <Pencil :size="17" aria-hidden="true" />
              </button>

              <button
                class="ui-icon-button"
                :title="t('accounts.resetPassword')"
                :aria-label="t('accounts.resetPassword')"
                @click="resetPassword(item)"
              >
                <KeyRound :size="17" aria-hidden="true" />
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
      <div class="count-pill">
        {{ t("configuration.shared.count", { entity: t("accounts.countEntity") }) }}
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
      >

        <AppCard class="modal-card">

          <div class="modal-header">
            <div>
              <p class="eyebrow">{{ t("accounts.eyebrow") }}</p>
              <h2>
                {{ editingId
                  ? t("accounts.edit")
                  : t("accounts.add")
                }}
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
              :label="t('common.name')"
              :placeholder="t('profileUser.namePlaceholder')"
            />

            <AppInput
              v-model="username"
              :label="t('auth.username')"
              :placeholder="t('accounts.usernamePlaceholder')"
            />

            <AppSelect
              v-model="role"
              :label="t('accounts.role')"
              :options="
  currentRole === 'super admin'
    ? [
        { label: t('accounts.roles.admin'), value: 'admin' },
        { label: t('accounts.roles.user'), value: 'user' }
      ]
    : [
        { label: t('accounts.roles.user'), value: 'user' }
      ]
"
            />

            <!-- ✅ TOGGLE (UPDATED) -->
            <div class="field">
              <label>{{ t("accounts.status") }}</label>

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
                  {{ aktif ? t("status.active") : t("status.notActive") }}
                </span>
              </div>
            </div>

          </div>

          <div class="modal-actions">

            <button
              v-if="editingId"
              class="ui-button ui-button--outline ui-button--danger"
              @click="askDelete({ id: editingId })"
            >
              {{ t("common.delete") }}
            </button>

            <AppButton
              :text="t('common.cancel')"
              variant="outline"
              @click="closeModal"
            />

            <AppButton
              :text="editingId ? t('common.update') : t('common.save')"
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

          <div class="delete-icon">
            <Trash2 :size="28" aria-hidden="true" />
          </div>

          <h3>
            {{ t("common.deleteTitle", { name: selectedAccount?.nama }) }}
          </h3>

          <p class="delete-desc">
            {{ t("common.deleteWarning") }}
          </p>

          <div class="confirm-box">

            <label>
              {{ t("common.typeToConfirm", { keyword: t("common.deleteKeyword") }) }}
            </label>

            <div class="org-delete-name">
              <span class="danger-word">{{ t("common.deleteKeyword") }}</span>
            </div>

            <input
              v-model="deleteConfirmText"
              class="delete-input"
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

    <!-- ✅ TOGGLE CONFIRM MODAL -->
    <transition name="fade">
      <div
        v-if="showToggleModal"
        class="modal-overlay"
      >

        <div class="delete-modal">

          <div class="delete-icon">
            <TriangleAlert :size="28" aria-hidden="true" />
          </div>

          <h3>
            {{ toggleTarget?.aktif
              ? t("accounts.deactivateQuestion")
              : t("accounts.activeQuestion")
            }}
          </h3>

          <p class="delete-desc">
            {{ t("accounts.typeToggleToConfirm", { keyword: toggleKeyword }) }}
          </p>

          <div class="confirm-box">

            <label>
              {{ t("accounts.toggleConfirm") }}
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
              class="ui-button ui-button--outline"
              @click="closeToggleModal"
            >
              {{ t("common.cancel") }}
            </button>

            <button
              class="ui-button ui-button--danger"
              :disabled="!canToggle"
              @click="confirmToggle"
            >
              {{ t("common.confirm") }}
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

      <div class="delete-icon">
        <LockKeyhole :size="28" aria-hidden="true" />
      </div>

      <h3>{{ passwordModalTitle }}</h3>

      <p class="delete-desc">
        {{ t("accounts.temporaryPasswordNotice") }}
</p>

      <div class="confirm-box">

        <label>{{ t("auth.username") }}</label>

        <div class="org-delete-name">
          {{ generatedUsername }}
        </div>

        <label style="margin-top:12px">
          {{ t("accounts.temporaryPassword") }}
        </label>

        <div class="org-delete-name">
          <strong>{{ generatedPassword }}</strong>
        </div>

      </div>

      <div class="delete-actions">

        <button
          class="ui-button ui-button--outline"
          @click="showPasswordModal = false"
        >
          {{ t("common.close") }}
        </button>

      </div>

    </div>
  </div>
</transition>
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

.hierarchy-card{
  background:white;
  border:1px solid var(--border);
  border-radius:20px;
  padding:32px;
  margin-bottom:32px;
  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.hierarchy-left{
  flex:1;
  min-width:280px;
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
  font-size:15px;
}

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
  font-size:14px;
  color:#334155;
  border-bottom:1px solid #F1F5F9;
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
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight:800;
  flex-shrink:0;
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

.success{
  color:#16A34A;
  font-weight:700;
}

.danger{
  color:#DC2626;
  font-weight:700;
}

.empty-cell{
  text-align:center;
  color:#94A3B8;
  padding:50px;
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

.btn-plus{
  font-size:18px;
  line-height:1;
}

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
}

.modal-card{
  width:100%;
  max-width:760px;
  background:white;
  border-radius:20px;
  padding:30px !important;
  box-sizing:border-box;
  border:1px solid var(--border);
  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.modal-header{
  display:flex;
  justify-content:space-between;
  gap:16px;
  margin-bottom:28px;
}

.eyebrow{
  font-size:12px;
  font-weight:700;
  color:var(--primary);
  letter-spacing:.12em;
  text-transform:uppercase;
  margin-bottom:10px;
}

.modal-header h2{
  font-size:28px;
  font-weight:800;
  color:var(--text);
  margin:0;
}

.form-area{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:18px;
}

.field{
  display:flex;
  flex-direction:column;
  gap:8px;
}

.field label{
  font-size:14px;
  font-weight:600;
  color:#334155;
}

.modal-actions{
  display:flex;
  justify-content:flex-end;
  gap:12px;
  margin-top:32px;
  padding-top:20px;
  border-top:1px solid #F1F5F9;
  flex-wrap:wrap;
}

/* DELETE MODAL */

.delete-modal{
  width:100%;
  max-width:480px;
  background:white;
  border-radius:20px;
  border:1px solid var(--border);
  padding:28px;
  box-shadow:0 12px 28px rgba(15,23,42,.08);
}

.delete-icon{
  width:64px;
  height:64px;
  margin:0 auto 18px;
  border-radius:999px;
  background:#FEF2F2;
  color:#DC2626;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:32px;
}

.delete-modal h3{
  text-align:center;
  font-size:24px;
  font-weight:800;
  color:#111827;
  margin-bottom:8px;
}

.delete-desc{
  text-align:center;
  color:#64748B;
  margin-bottom:24px;
}

.confirm-box label{
  display:block;
  font-size:14px;
  font-weight:600;
  color:#334155;
  margin-bottom:10px;
}

.org-delete-name{
  background:#F8FAFC;
  border:1px solid var(--border);
  padding:14px;
  border-radius:12px;
  font-weight:700;
  margin-bottom:12px;
  text-align:center;
}

.danger-word{
  color:#DC2626;
  font-size:20px;
  font-weight:800;
  letter-spacing:.04em;
}

.delete-input{
  width:100%;
  border:1px solid var(--border);
  border-radius:12px;
  padding:14px;
  font-size:14px;
  box-sizing:border-box;
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

/* TOGGLE SWITCH */

.switch-wrapper{
  display:flex;
  align-items:center;
  gap:12px;
}

.switch{
  position:relative;
  width:44px;
  height:24px;
}

.switch input{
  display:none;
}

.slider{
  position:absolute;
  inset:0;
  background:#D1D5DB;
  border-radius:999px;
  cursor:pointer;
  transition:.25s;
}

.slider::before{
  content:"";
  position:absolute;
  width:18px;
  height:18px;
  left:3px;
  top:3px;
  background:white;
  border-radius:50%;
  transition:.25s;
  box-shadow:0 2px 6px rgba(0,0,0,.15);
}

.switch input:checked + .slider{
  background:#22C55E;
}

.switch input:checked + .slider::before{
  transform:translateX(20px);
}

.status-text{
  font-size:14px;
  font-weight:600;
  color:#475569;
}

/* TABLE ROWS */

.clickable-row{
  transition:.15s;
}

.clickable-row:hover{
  background:#F8FAFC;
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

  .form-area{
    grid-template-columns:1fr;
  }

  .modal-actions,
  .delete-actions{
    flex-direction:column;
    align-items:stretch;
  }

}

</style>
