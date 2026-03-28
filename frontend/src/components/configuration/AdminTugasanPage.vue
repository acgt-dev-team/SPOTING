<script setup>
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import ConfigurationLayout from "./ConfigurationLayout.vue"

const route = useRoute()
const router = useRouter()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId
const siteId = route.params.siteId
const profileId = route.params.profileId

const search = ref("")

const profile = ref({
  id: profileId,
  name: "Profil Operasi",
  description: "Tetapan operasi tapak"
})

const tasks = ref([
  { id: 1, name: "Pengesahan akses", description: "Semakan akses pengguna", status: "Aktif" },
  { id: 2, name: "Audit tapak", description: "Pemeriksaan berkala", status: "Aktif" },
  { id: 3, name: "Semakan konfigurasi", description: "Validasi tetapan semasa", status: "Draf" }
])

const filteredTasks = computed(() => {
  return tasks.value.filter((item) =>
    item.name.toLowerCase().includes(search.value.toLowerCase())
  )
})

const breadcrumbs = [
  { label: "Organisasi", to: "/admin/configuration" },
  { label: "Sub Organisasi", to: `/admin/configuration/sub-organisasi/${organizationId}` },
  { label: "Tapak", to: `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}` },
  { label: "Profil", to: `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${siteId}` },
  { label: "Tugasan" }
]

function goBack() {
  router.push(`/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${siteId}`)
}
</script>

<template>
  <ConfigurationLayout :breadcrumbs="breadcrumbs">
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <p class="parent-label">Profil</p>
        <h2>{{ profile.name }}</h2>
        <p class="parent-desc">{{ profile.description }}</p>
      </div>

      <div class="hierarchy-right">
        <p class="child-label">Tugasan</p>
        <p class="child-subtext">Urus tugasan bagi profil yang dipilih.</p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian tugasan..." />
      </div>

      <button class="primary-btn">Tambah tugasan</button>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width: 80px">Bil</th>
              <th>Nama Tugasan</th>
              <th style="width: 180px">Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="filteredTasks.length === 0">
              <td colspan="3" class="empty-cell">Tiada tugasan dijumpai.</td>
            </tr>

            <tr v-for="(task, index) in filteredTasks" :key="task.id" class="clickable-row">
              <td>{{ index + 1 }}</td>

              <td>
                <div>
                  <p class="org-name">{{ task.name }}</p>
                  <p class="org-desc">{{ task.description }}</p>
                </div>
              </td>

              <td>
                <span class="status-pill" :class="{ draft: task.status === 'Draf' }">
                  {{ task.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="footer-bar">
      <button class="secondary-btn" @click="goBack">← Kembali</button>

      <div class="count-pill">
        Bilangan Tugasan:
        <strong>{{ filteredTasks.length.toString().padStart(2, "0") }}</strong>
      </div>
    </div>
  </ConfigurationLayout>
</template>

<style scoped>
.toolbar,
.footer-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.toolbar { margin-bottom: 24px; }
.footer-bar { margin-top: 24px; }

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
.search-box input {
  border: none;
  outline: none;
  background: transparent;
  width: 100%;
  font-size: 14px;
}
.search-icon { color: #6b7280; font-size: 18px; }

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
.parent-desc,
.child-subtext,
.org-desc { color: #6b7280; font-size: 14px; }
.child-label { font-size: 19px; font-weight: 800; color: #111827; margin-bottom: 6px; }

.table-card {
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid #e5e7eb;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.06);
}
.table-scroll { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
thead { background: #f8fafc; }
th {
  text-align: left;
  padding: 20px 24px;
  font-size: 13px;
  font-weight: 800;
  color: #374151;
  border-bottom: 1px solid #eef2f7;
  text-transform: uppercase;
}
td {
  padding: 18px 24px;
  font-size: 15px;
  border-bottom: 1px solid #f1f5f9;
}
.clickable-row:hover { background: #faf5ff; }
.org-name { font-weight: 800; color: #111827; }

.status-pill {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  background: #dcfce7;
  color: #166534;
  font-size: 13px;
  font-weight: 800;
}
.status-pill.draft {
  background: #ede9fe;
  color: #6d28d9;
}

.primary-btn,
.secondary-btn {
  border: none;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}
.primary-btn {
  padding: 14px 22px;
  background: linear-gradient(135deg, #7c3aed, #c026d3);
  color: white;
  box-shadow: 0 14px 28px rgba(147, 51, 234, 0.25);
}
.secondary-btn {
  padding: 14px 22px;
  background: white;
  border: 1px solid #e5e7eb;
  color: #111827;
}
.empty-cell {
  text-align: center;
  padding: 52px 20px;
  color: #6b7280;
}
.count-pill {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 16px 20px;
  color: #374151;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}
.count-pill strong { margin-left: 10px; color: #111827; }
</style>