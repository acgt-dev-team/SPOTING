<script setup>
import { computed, ref } from "vue"
import { useRouter } from "vue-router"
import AddOrganisasiModal from "./AddOrganisasiModal.vue"

const router = useRouter()

const search = ref("")
const showModal = ref(false)

const organizations = ref([
  {
    id: 1,
    name: "Jabatan Imigresen",
    description: "Pengurusan organisasi utama",
    subCount: 200,
    siteCount: 828,
    taskCount: 1233,
    totalTaskCount: 9000
  },
  {
    id: 2,
    name: "Jabatan Pendaftaran Negara",
    description: "Pengurusan data organisasi",
    subCount: 154,
    siteCount: 612,
    taskCount: 884,
    totalTaskCount: 6200
  }
])

const filteredOrganizations = computed(() => {
  return organizations.value.filter((org) =>
    org.name.toLowerCase().includes(search.value.toLowerCase())
  )
})

function openModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function addOrganization(newOrg) {
  organizations.value.unshift({
    ...newOrg,
    totalTaskCount: newOrg.totalTaskCount ?? 0
  })
  closeModal()
}

function goToSubOrganisasi(org) {
  router.push(`/admin/configuration/sub-organisasi/${org.id}`)
}
</script>

<template>
  <div>
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <p class="section-label">Konfigurasi</p>
        <h2>Senarai Organisasi</h2>
        <p class="section-desc">Urus organisasi utama dalam sistem Spoting.</p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian organisasi..." />
      </div>

      <button class="primary-btn" @click="openModal">
        Tambah organisasi
      </button>
    </div>

    <div class="page-heading-block">
      <h1 class="main-page-title">Senarai Organisasi</h1>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width: 80px">Bil</th>
              <th>Nama Organisasi</th>
              <th style="width: 180px">Sub Organisasi</th>
              <th style="width: 140px">Tapak</th>
              <th style="width: 180px">Tugasan</th>
              <th style="width: 140px"></th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="filteredOrganizations.length === 0">
              <td colspan="6" class="empty-cell">Tiada organisasi dijumpai.</td>
            </tr>

            <tr
              v-for="(org, index) in filteredOrganizations"
              :key="org.id"
              class="clickable-row"
              @click="goToSubOrganisasi(org)"
            >
              <td>{{ index + 1 }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar">
                    {{ org.name.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <p class="org-name">{{ org.name }}</p>
                    <p class="org-desc">{{ org.description }}</p>
                  </div>
                </div>
              </td>

              <td>{{ org.subCount }}</td>
              <td>{{ org.siteCount }}</td>

              <td>
                <span class="success">{{ org.taskCount.toLocaleString() }}</span>
                <span class="muted"> / {{ org.totalTaskCount.toLocaleString() }}</span>
              </td>

              <td>
                <button class="ghost-btn" @click.stop="goToSubOrganisasi(org)">
                  Buka →
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="footer-bar">
      <div class="count-pill">
        Bilangan Organisasi:
        <strong>{{ filteredOrganizations.length.toString().padStart(2, "0") }}</strong>
      </div>
    </div>

    <AddOrganisasiModal
      :show="showModal"
      @close="closeModal"
      @save="addOrganization"
    />
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

.section-label {
  font-size: 13px;
  font-weight: 700;
  color: #020265;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 6px;
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

.muted {
  color: #6b7280;
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
  white-space: nowrap;
}

.primary-btn:hover {
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .main-page-title {
    font-size: 25px;
  }

  .hierarchy-card {
    padding: 24px;
    border-radius: 24px;
  }

  .hierarchy-left h2 {
    font-size: 26px;
  }

  .toolbar {
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
  }
}
</style>