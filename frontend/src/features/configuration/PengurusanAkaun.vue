<script setup>
import { ref, computed, onMounted, watch } from "vue"
import { KeyRound, LockKeyhole, Pencil, Plus } from "lucide-vue-next"
import api from "../../services/api"
import { t } from "../../i18n"
import { useToast } from "../../ui/AppToast.vue"
import { isValidUserId } from "../../utils/validation"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppSelect from "../../ui/AppSelect.vue"
import AppPagination from "../../ui/AppPagination.vue"
import ConfigTable from "../../ui/ConfigTable.vue"
import ConfirmActionModal from "../../ui/ConfirmActionModal.vue"
import FormModal from "../../ui/FormModal.vue"
import PageHeader from "../../ui/PageHeader.vue"
import PageToolbar from "../../ui/PageToolbar.vue"

const toast = useToast()

const search = ref("")
const roleFilter = ref("")
const accountStatusFilter = ref("")
const showModal = ref(false)
const showDeleteModal = ref(false)

const showPasswordModal = ref(false)
const generatedPassword = ref("")
const generatedUsername = ref("")
const passwordModalTitle = ref("")

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
const loading = ref(true)

const currentPage = ref(1)
const pageSize = 10

const tableColumns = [
  { key: "number", label: t("common.tableNumber"), width: "72px" },
  { key: "name", label: t("common.name") },
  { key: "username", label: t("auth.username"), width: "180px" },
  { key: "role", label: t("accounts.role"), width: "140px" },
  { key: "actions", label: t("common.actions"), width: "152px", align: "center" }
]

const accountRoleFilterOptions = computed(() => {
  const roles = currentRole === "super admin"
    ? ["admin", "user"]
    : ["user"]

  return [
    { label: t("filters.allRoles"), value: "" },
    ...roles.map((item) => ({
      label: item === "admin" ? t("accounts.roles.admin") : t("accounts.roles.user"),
      value: item
    }))
  ]
})

const accountStatusFilterOptions = [
  { label: t("filters.allStatuses"), value: "" },
  { label: t("status.active"), value: "active" },
  { label: t("status.notActive"), value: "inactive" }
]

const hasAccountFilters = computed(() =>
  Boolean(roleFilter.value || accountStatusFilter.value)
)

const hasAccountQuery = computed(() =>
  Boolean(search.value.trim() || hasAccountFilters.value)
)

const totalPages = computed(() => {
  return Math.ceil(filteredAccounts.value.length / pageSize)
})

const filteredAccounts = computed(() => {
  const query = search.value.trim().toLowerCase()

  return accounts.value
    .slice()
    .sort((a, b) => a.id - b.id)
    .filter((item) => {
      const activeStatus = item.aktif ? "active" : "inactive"
      const searchableValues = [item.nama, item.username, item.role]

      const matchesSearch = !query || searchableValues.some((value) =>
        String(value || "").toLowerCase().includes(query)
      )

      const matchesRole = !roleFilter.value || item.role === roleFilter.value
      const matchesStatus = !accountStatusFilter.value || activeStatus === accountStatusFilter.value

      return matchesSearch && matchesRole && matchesStatus
    })
})

watch([search, roleFilter, accountStatusFilter], () => {
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
  errors.value = {}
}

function openModal() {
  editingId.value = null
  resetForm()
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  errors.value = {}
}

function clearAccountFilters() {
  roleFilter.value = ""
  accountStatusFilter.value = ""
}

function validateForm() {
  const e = {}

  if (!nama.value.trim()) {
    e.nama = t("validation.nameRequired")
  }

  if (!username.value.trim()) {
    e.username = t("validation.usernameRequired")
  } else if (!isValidUserId(username.value)) {
    e.username = t("validation.usernameFormat")
  }

  errors.value = e

  return Object.keys(e).length === 0
}

function editAccount(item) {
  errors.value = {}
  editingId.value = item.id
  nama.value = item.nama
  username.value = item.username
  role.value = item.role
  aktif.value = item.aktif ?? true
  showModal.value = true
}

async function fetchAccounts() {
  loading.value = true

  try {

    const res = await api.get(
      `/auth/users?role=${currentRole}`
    )

    accounts.value = res.data

  } catch (err) {

    console.error(err)
    toast.error(t("common.loadFailed", { entity: t("accounts.countEntity") }))

  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAccounts()
})

async function saveAccount() {
  if (!validateForm()) {
    toast.warning(errors.value.username || t("validation.completeBeforeSave"))
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
      toast.success(t("accounts.passwordCreatedSuccess"))
    }

    await fetchAccounts()

    closeModal()
    toast.success(t("accounts.saveSuccess"))

  } catch (err) {
    console.error(err)
    toast.error(t("common.saveFailed", { entity: t("accounts.countEntity") }))
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
    toast.success(t("accounts.deleteSuccess"))

  } catch (err) {
    console.error(err)
    toast.error(t("common.deleteFailed", { entity: t("accounts.countEntity") }))
  }
}

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
    toast.success(t("accounts.toggleSuccess"))

  } catch (err) {

    console.error(err)
    toast.error(t("common.saveFailed", { entity: t("accounts.countEntity") }))

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
    toast.success(t("accounts.passwordResetSuccess"))

  } catch (err) {

    console.error(err)

    toast.error(t("accounts.passwordResetFailed"))

  }

}
</script>

<template>
  <div>

    <PageHeader
      :title="t('accounts.title')"
      :description="t('accounts.description')"
    />

    <PageToolbar
      v-model="search"
      :placeholder="t('configuration.shared.search', { entity: t('accounts.searchEntity') })"
      :action-text="t('accounts.add')"
      @action="openModal"
    >
      <template #filters>
        <AppSelect
          v-model="roleFilter"
          :label="t('accounts.role')"
          :options="accountRoleFilterOptions"
        />

        <AppSelect
          v-model="accountStatusFilter"
          :label="t('accounts.status')"
          :options="accountStatusFilterOptions"
        />

        <button
          v-if="hasAccountFilters"
          class="ui-button ui-button--outline"
          type="button"
          @click="clearAccountFilters"
        >
          {{ t("filters.clear") }}
        </button>
      </template>

      <template #action-icon>
        <Plus :size="18" aria-hidden="true" />
      </template>
    </PageToolbar>

    <div class="page-heading-block">
      <h1 class="main-page-title">{{ t("accounts.listTitle") }}</h1>
    </div>

    <ConfigTable
      :columns="tableColumns"
      :loading="loading"
      :empty="filteredAccounts.length === 0"
      :empty-message="t('accounts.empty')"
      :empty-action-text="hasAccountQuery ? '' : t('accounts.add')"
      min-width="760px"
      @empty-action="openModal"
    >

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

              <td class="table-cell--center">
                <div class="config-row-actions">

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

    </ConfigTable>

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

    <FormModal
      :show="showModal"
      :eyebrow="t('accounts.eyebrow')"
      :title="editingId ? t('accounts.edit') : t('accounts.add')"
      @close="closeModal"
    >

          <div class="form-area">

            <AppInput
              v-model="nama"
              :label="t('common.name')"
              :placeholder="t('profileUser.namePlaceholder')"
              :error="errors.nama || ''"
            />

            <AppInput
              v-model="username"
              :label="t('auth.username')"
              :placeholder="t('accounts.usernamePlaceholder')"
              :error="errors.username || ''"
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

          <template #actions>

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

          </template>

    </FormModal>

    <ConfirmActionModal
      v-model="deleteConfirmText"
      :show="showDeleteModal"
      :title="t('common.deleteTitle', { name: selectedAccount?.nama || t('common.emptyValue') })"
      :keyword="t('common.deleteKeyword')"
      :disabled="!canDelete"
      @close="closeDeleteModal"
      @confirm="confirmDelete"
    />

    <ConfirmActionModal
      v-model="toggleConfirmText"
      :show="showToggleModal"
      :title="toggleTarget?.aktif ? t('accounts.deactivateQuestion') : t('accounts.activeQuestion')"
      :description="t('accounts.typeToggleToConfirm', { keyword: toggleKeyword })"
      :keyword="toggleKeyword"
      :placeholder="toggleKeyword"
      :confirm-text="t('common.confirm')"
      confirm-variant="primary"
      :disabled="!canToggle"
      icon="warning"
      @close="closeToggleModal"
      @confirm="confirmToggle"
    />

  </div>

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

.delete-actions{
  display:flex;
  justify-content:flex-end;
  gap:12px;
  margin-top:24px;
}

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

.clickable-row{
  transition:.15s;
}

.clickable-row:hover{
  background:#F8FAFC;
}

@media(max-width:768px){

  .form-area{
    grid-template-columns:1fr;
  }

  .delete-actions{
    flex-direction:column;
    align-items:stretch;
  }

}

</style>

