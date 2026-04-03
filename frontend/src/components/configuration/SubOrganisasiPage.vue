<script setup>
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import AddSubOrganisasiModal from "./AddSubOrganisasiModal.vue"
import ConfigurationLayout from "./ConfigurationLayout.vue"

const route = useRoute()
const router = useRouter()

const organizationId = route.params.organizationId
const search = ref("")
const showModal = ref(false)
const selectedSubOrganisasi = ref(null)

const organization = ref({
  id: organizationId,
  name: "Jabatan Imigresen",
  description: "Pengurusan organisasi utama"
})

const subOrganizations = ref([
  {
    id: 1,
    name: "Sub Organisasi A",
    description: "Bahagian operasi utama",
    siteCount: 320,
    taskCount: 412
  },
  {
    id: 2,
    name: "Sub Organisasi B",
    description: "Bahagian pentadbiran",
    siteCount: 180,
    taskCount: 255
  }
])

const filteredSubOrganizations = computed(() => {
  return subOrganizations.value.filter((item) =>
    item.name.toLowerCase().includes(search.value.toLowerCase())
  )
})

const breadcrumbs = [
  { label: "Organisasi", to: "/admin/configuration" },
  { label: "Sub Organisasi" }
]

function goBack() {
  router.push("/admin/configuration")
}

function goToTapak(item) {
  router.push(`/admin/configuration/sub-organisasi/${organizationId}/tapak/${item.id}`)
}

function openAddModal() {
  selectedSubOrganisasi.value = null
  showModal.value = true
}

function openEditModal(item) {
  selectedSubOrganisasi.value = { ...item }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedSubOrganisasi.value = null
}

function saveSubOrganisasi(payload) {
  const existingIndex = subOrganizations.value.findIndex((item) => item.id === payload.id)

  if (existingIndex !== -1) {
    subOrganizations.value[existingIndex] = {
      ...subOrganizations.value[existingIndex],
      ...payload
    }
  } else {
    subOrganizations.value.unshift(payload)
  }

  closeModal()
}
</script>

<template>
  <ConfigurationLayout :breadcrumbs="breadcrumbs">
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <p class="parent-label">Organisasi Induk</p>
        <h2>{{ organization.name }}</h2>
        <p class="parent-desc">{{ organization.description }}</p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian sub organisasi..." />
      </div>

      <button class="primary-btn" @click="openAddModal">
        Tambah sub organisasi
      </button>
    </div>

    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Sub Organisasi</h1>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width: 80px">Bil</th>
              <th>Nama Sub Organisasi</th>
              <th style="width: 180px">Tapak</th>
              <th style="width: 180px">Tugasan</th>
              <th style="width: 120px">Tindakan</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="filteredSubOrganizations.length === 0">
              <td colspan="5" class="empty-cell">
                Tiada sub organisasi dijumpai.
              </td>
            </tr>

            <tr
              v-for="(item, index) in filteredSubOrganizations"
              :key="item.id"
              class="clickable-row"
              @click="goToTapak(item)"
            >
              <td>{{ index + 1 }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar small">
                    {{ item.name.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <p class="org-name">{{ item.name }}</p>
                    <p class="org-desc">{{ item.description }}</p>
                  </div>
                </div>
              </td>

              <td>{{ item.siteCount }}</td>
              <td>{{ item.taskCount }}</td>

              <td>
                <button class="icon-btn" @click.stop="openEditModal(item)" title="Edit">
                  ✎
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="footer-bar">
      <button class="secondary-btn" @click="goBack">← Kembali</button>

      <div class="count-pill">
        Bilangan Sub Organisasi:
        <strong>{{ filteredSubOrganizations.length.toString().padStart(2, "0") }}</strong>
      </div>
    </div>

    <AddSubOrganisasiModal
      :show="showModal"
      :editData="selectedSubOrganisasi"
      @close="closeModal"
      @save="saveSubOrganisasi"
    />
  </ConfigurationLayout>
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
  font-family: "Trebuchet MS", "Segoe UI", "Inter", sans-serif;
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
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid #dbe3ff;
  border-radius: 30px;
  padding: 30px;
  margin-bottom: 28px;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.06);
}

.parent-label {
  font-size: 13px;
  font-weight: 800;
  color: #020265;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}

.hierarchy-left h2 {
  font-size: 32px;
  font-weight: 900;
  color: #111827;
  margin-bottom: 8px;
}

.parent-desc {
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

.org-avatar.small {
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
}

.org-desc {
  font-size: 13px;
  color: #6b7280;
  margin-top: 2px;
}

.icon-btn {
  border: none;
  background: #eef1ff;
  color: #020265;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  font-size: 16px;
  cursor: pointer;
  transition: 0.18s ease;
}

.icon-btn:hover {
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
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
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

.secondary-btn,
.primary-btn {
  border: none;
  padding: 14px 22px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.2s ease;
}

.secondary-btn {
  background: white;
  border: 1px solid #dbe3ff;
  color: #111827;
}

.secondary-btn:hover {
  background: #f4f6ff;
  transform: translateY(-1px);
}

.primary-btn {
  background: linear-gradient(135deg, #020265, #0b0b8f);
  color: white;
  box-shadow: 0 14px 28px rgba(2, 2, 101, 0.25);
}

.primary-btn:hover {
  transform: translateY(-1px);
}
</style>