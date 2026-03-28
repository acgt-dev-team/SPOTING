<script setup>
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import ConfigurationLayout from "./ConfigurationLayout.vue"

const route = useRoute()
const router = useRouter()

const organizationId = route.params.organizationId
const subOrganizationId = route.params.subOrganizationId
const siteId = route.params.siteId

const search = ref("")

const site = ref({
  id: siteId,
  name: "Tapak Putrajaya",
  description: "Zon pentadbiran utama"
})

const profiles = ref([
  { id: 1, name: "Profil Operasi", description: "Tetapan operasi tapak", taskCount: 34 },
  { id: 2, name: "Profil Pentadbiran", description: "Konfigurasi pentadbiran", taskCount: 21 },
  { id: 3, name: "Profil Keselamatan", description: "Polisi keselamatan", taskCount: 18 }
])

const filteredProfiles = computed(() => {
  return profiles.value.filter((item) =>
    item.name.toLowerCase().includes(search.value.toLowerCase())
  )
})

const breadcrumbs = [
  { label: "Organisasi", to: "/admin/configuration" },
  { label: "Sub Organisasi", to: `/admin/configuration/sub-organisasi/${organizationId}` },
  { label: "Tapak", to: `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}` },
  { label: "Profil" }
]

function goBack() {
  router.push(`/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}`)
}

function goToTugasan(profile) {
  router.push(
    `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${siteId}/tugasan/${profile.id}`
  )
}
</script>

<template>
  <ConfigurationLayout :breadcrumbs="breadcrumbs">
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <p class="parent-label">Tapak</p>
        <h2>{{ site.name }}</h2>
        <p class="parent-desc">{{ site.description }}</p>
      </div>

      <div class="hierarchy-right">
        <p class="child-label">Senarai Profil</p>
        <p class="child-subtext">Pilih profil untuk melihat tugasan berkaitan.</p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">⌕</span>
        <input v-model="search" type="text" placeholder="Carian profil..." />
      </div>

      <button class="primary-btn">Tambah profil</button>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width: 80px">Bil</th>
              <th>Nama Profil</th>
              <th style="width: 180px">Jumlah Tugasan</th>
              <th style="width: 140px"></th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="filteredProfiles.length === 0">
              <td colspan="4" class="empty-cell">Tiada profil dijumpai.</td>
            </tr>

            <tr
              v-for="(profile, index) in filteredProfiles"
              :key="profile.id"
              class="clickable-row"
              @click="goToTugasan(profile)"
            >
              <td>{{ index + 1 }}</td>

              <td>
                <div class="org-cell">
                  <div class="org-avatar">{{ profile.name.charAt(0).toUpperCase() }}</div>
                  <div>
                    <p class="org-name">{{ profile.name }}</p>
                    <p class="org-desc">{{ profile.description }}</p>
                  </div>
                </div>
              </td>

              <td>{{ profile.taskCount }}</td>

              <td>
                <button class="ghost-btn" @click.stop="goToTugasan(profile)">
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
        Bilangan Profil:
        <strong>{{ filteredProfiles.length.toString().padStart(2, "0") }}</strong>
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
.clickable-row { cursor: pointer; transition: 0.18s ease; }
.clickable-row:hover { background: #faf5ff; }

.org-cell { display: flex; align-items: center; gap: 14px; }
.org-avatar {
  width: 44px;
  height: 44px;
  border-radius: 15px;
  background: linear-gradient(135deg, #7c3aed, #c026d3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  box-shadow: 0 10px 24px rgba(147, 51, 234, 0.22);
}
.org-name { font-weight: 800; color: #111827; }

.primary-btn,
.secondary-btn,
.ghost-btn {
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
.ghost-btn {
  padding: 10px 14px;
  background: #f3f4f6;
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