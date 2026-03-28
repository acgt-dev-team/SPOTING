<script setup>
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import ConfigurationLayout from "./ConfigurationLayout.vue"

const route = useRoute()
const router = useRouter()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId

const search = ref("")

const organization = ref({
  id: organizationId,
  name: "Jabatan Imigresen"
})

const subOrganization = ref({
  id: subOrganizationId,
  name: "Sub Organisasi A",
  description: "Bahagian operasi utama"
})

const sites = ref([
  {
    id: 1,
    name: "Tapak Putrajaya",
    description: "Zon pentadbiran utama",
    taskCount: 84
  },
  {
    id: 2,
    name: "Tapak KLIA",
    description: "Lokasi operasi lapangan",
    taskCount: 112
  },
  {
    id: 3,
    name: "Tapak Johor Bahru",
    description: "Cawangan selatan",
    taskCount: 67
  }
])

const filteredSites = computed(() => {
  return sites.value.filter((item) =>
    item.name.toLowerCase().includes(search.value.toLowerCase())
  )
})

const breadcrumbs = [
  { label: "Organisasi", to: "/admin/configuration" },
  { label: "Sub Organisasi", to: `/admin/configuration/sub-organisasi/${organizationId}` },
  { label: "Tapak" }
]

function goBack() {
  router.push(`/admin/configuration/sub-organisasi/${organizationId}`)
}

function goToProfil(site) {
  router.push(
    `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${site.id}`
  )
}
</script>

<template>
  <ConfigurationLayout :breadcrumbs="breadcrumbs">
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <p class="parent-label">Sub Organisasi</p>
        <h2>{{ subOrganization.name }}</h2>
        <p class="parent-desc">
          {{ organization.name }} · {{ subOrganization.description }}
        </p>
      </div>

      <div class="hierarchy-right">
        <p class="child-label">Senarai Tapak</p>
        <p class="child-subtext">Pilih tapak untuk melihat senarai profil berkaitan.</p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian tapak..." />
      </div>

      <button class="primary-btn">Tambah tapak</button>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width: 80px">Bil</th>
              <th>Nama Tapak</th>
              <th style="width: 180px">Jumlah Tugasan</th>
              <th style="width: 140px"></th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="filteredSites.length === 0">
              <td colspan="4" class="empty-cell">
                Tiada tapak dijumpai.
              </td>
            </tr>

            <tr
              v-for="(site, index) in filteredSites"
              :key="site.id"
              class="clickable-row"
              @click="goToProfil(site)"
            >
              <td>{{ index + 1 }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar small">
                    {{ site.name.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <p class="org-name">{{ site.name }}</p>
                    <p class="org-desc">{{ site.description }}</p>
                  </div>
                </div>
              </td>

              <td>{{ site.taskCount }}</td>

              <td>
                <button class="ghost-btn" @click.stop="goToProfil(site)">
                  Buka →
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
        Bilangan Tapak:
        <strong>{{ filteredSites.length.toString().padStart(2, "0") }}</strong>
      </div>
    </div>
  </ConfigurationLayout>
</template>

<style scoped>
.toolbar {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.search-box {
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 0 16px;
  height: 54px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
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
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid #e5e7eb;
  border-radius: 30px;
  padding: 30px;
  margin-bottom: 24px;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.06);
  flex-wrap: wrap;
}

.hierarchy-left {
  flex: 1;
  min-width: 280px;
}

.hierarchy-right {
  min-width: 260px;
  padding-top: 54px;
  text-align: left;
}

.parent-label {
  font-size: 13px;
  font-weight: 800;
  color: #9333ea;
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

.child-label {
  font-size: 19px;
  font-weight: 800;
  color: #111827;
  margin-bottom: 6px;
}

.child-subtext {
  color: #6b7280;
  font-size: 14px;
}

.table-card {
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid #e5e7eb;
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
  background: #f8fafc;
}

th {
  text-align: left;
  padding: 20px 24px;
  font-size: 13px;
  font-weight: 800;
  color: #374151;
  border-bottom: 1px solid #eef2f7;
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
  background: #faf5ff;
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
  background: linear-gradient(135deg, #7c3aed, #c026d3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  flex-shrink: 0;
  box-shadow: 0 10px 24px rgba(147, 51, 234, 0.22);
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

.ghost-btn {
  border: none;
  background: #f3f4f6;
  color: #111827;
  padding: 10px 14px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
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
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 16px 20px;
  color: #374151;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

.count-pill strong {
  margin-left: 10px;
  color: #111827;
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
  border: 1px solid #e5e7eb;
  color: #111827;
}

.primary-btn {
  background: linear-gradient(135deg, #7c3aed, #c026d3);
  color: white;
  box-shadow: 0 14px 28px rgba(147, 51, 234, 0.25);
}

.primary-btn:hover,
.secondary-btn:hover {
  transform: translateY(-1px);
}
</style>