<script setup>
import { computed, ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"
import AppButton from "../../ui/AppButton.vue"
import AppPagination from "../../ui/AppPagination.vue"

const router = useRouter()

// =======================
// FILTER
// =======================
const selectedRange = ref("minggu")

const ranges = [
  { label: "Hari ini", value: "hari" },
  { label: "Minggu", value: "minggu" },
  { label: "Bulan", value: "bulan" }
]

// =======================
// DASHBOARD STATS (API)
// =======================
const stats = ref({
  organisasi: 0,
  sub_organisasi: 0,
  tapak: 0,
  profil: 0,
  tugasan: 0
})

// ✅ REAL ORGANISASI DATA
const organizations = ref([])

onMounted(async () => {
  try {
    // ✅ stats (already working)
    const statsRes = await api.get("/dashboard/")
    stats.value = statsRes.data

    // ✅ ADD THIS (for table)
    const orgRes = await api.get("/dashboard/full")
    organizations.value = orgRes.data.organizations || []

  } catch (err) {
    console.error("Dashboard API error:", err)
  }
})

const currentPage = ref(1)
const itemsPerPage = 10

const totalPages = computed(() =>
  Math.ceil(sortedOrganizations.value.length / itemsPerPage)
)

const paginatedOrganizations = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedOrganizations.value.slice(start, start + itemsPerPage)
})

// =======================
// COMPUTED
// =======================
const totalTasks = computed(() =>
  organizations.value.reduce((sum, o) => sum + o.total, 0)
)

const completedTasks = computed(() =>
  organizations.value.reduce((sum, o) => sum + o.done, 0)
)

// =======================
// HELPERS
// =======================
const formatNumber = (num) => {
  if (num >= 1000) return (num / 1000).toFixed(1) + "k"
  return num
}

const getPercent = (done, total) =>
  total ? Math.round((done / total) * 100) : 0

const topOrg = computed(() => {
  if (!organizations.value.length) return null
  return [...organizations.value].sort(
    (a, b) => getPercent(b.done, b.total) - getPercent(a.done, a.total)
  )[0]
})

const sortedOrganizations = computed(() => {
  return [...organizations.value].sort(
    (a, b) => getPercent(b.done, b.total) - getPercent(a.done, a.total)
  )
})

watch(organizations, () => {
  currentPage.value = 1
})

// =======================
// NAV
// =======================
function goConfig() {
  router.push("/admin/configuration")
}

function goAccounts() {
  router.push("/admin/accounts")
}
</script>

<template>
  <div class="dashboard-container">

    <!-- PAGE TITLE -->
    <div class="page-title">
      <h1>Ringkasan Prestasi</h1>
      <p>Prestasi semasa sistem pentadbiran agensi.</p>
    </div>

    <!-- KPI -->
    <div class="stats-grid">

      <!-- ORGANISASI -->
      <div class="stat-card">

        <div class="card-icon">

          <svg viewBox="0 0 24 24" fill="none">

            <path
              d="M4 21H20M7 21V4H17V21"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
            />

            <path d="M10 8H10.01" stroke="currentColor" stroke-width="2"/>
            <path d="M14 8H14.01" stroke="currentColor" stroke-width="2"/>

            <path d="M10 12H10.01" stroke="currentColor" stroke-width="2"/>
            <path d="M14 12H14.01" stroke="currentColor" stroke-width="2"/>

          </svg>

        </div>

        <h3>{{ stats.organisasi }}</h3>

        <span>Organisasi</span>

      </div>

      <!-- SUB ORGANISASI -->
      <div class="stat-card">

        <div class="card-icon">

          <svg viewBox="0 0 24 24" fill="none">

            <circle cx="12" cy="7" r="2" stroke="currentColor" stroke-width="1.8"/>

            <circle cx="6.5" cy="10" r="2" stroke="currentColor" stroke-width="1.8"/>

            <circle cx="17.5" cy="10" r="2" stroke="currentColor" stroke-width="1.8"/>

            <path
              d="M8 18C8 15.5 10 14 12 14C14 14 16 15.5 16 18"
              stroke="currentColor"
              stroke-width="1.8"
            />

            <path
              d="M3 18C3 16.5 4.5 15.5 6.5 15.5"
              stroke="currentColor"
              stroke-width="1.8"
            />

            <path
              d="M17.5 15.5C19.5 15.5 21 16.5 21 18"
              stroke="currentColor"
              stroke-width="1.8"
            />

          </svg>

        </div>

        <h3>{{ stats.sub_organisasi }}</h3>

        <span>Sub Organisasi</span>

      </div>

      <!-- TAPAK -->
      <div class="stat-card">

        <div class="card-icon">

          <svg viewBox="0 0 24 24" fill="none">

            <path
              d="M12 21C16 16 18 13 18 9A6 6 0 006 9C6 13 8 16 12 21Z"
              stroke="currentColor"
              stroke-width="1.8"
            />

            <circle
              cx="12"
              cy="9"
              r="2.5"
              stroke="currentColor"
              stroke-width="1.8"
            />

          </svg>

        </div>

        <h3>{{ stats.tapak }}</h3>

        <span>Tapak</span>

      </div>

      <!-- PROFIL -->
      <div class="stat-card">

        <div class="card-icon">

          <svg viewBox="0 0 24 24" fill="none">

            <circle
              cx="12"
              cy="8"
              r="3"
              stroke="currentColor"
              stroke-width="1.8"
            />

            <path
              d="M6 20C6 16.5 8.5 15 12 15C15.5 15 18 16.5 18 20"
              stroke="currentColor"
              stroke-width="1.8"
            />

          </svg>

        </div>

        <h3>{{ stats.profil }}</h3>

        <span>Profil</span>

      </div>

      <!-- TUGASAN -->
      <div class="stat-card">

        <div class="card-icon success">

          <svg viewBox="0 0 24 24" fill="none">

            <!-- body -->
            <rect
              x="6"
              y="3"
              width="12"
              height="18"
              rx="2"
              stroke="currentColor"
              stroke-width="1.8"
            />

            <!-- top clip -->
            <path
              d="M10 3H14"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
            />

            <!-- row 1 -->
            <rect
              x="8.2"
              y="8"
              width="1.2"
              height="1.2"
              rx=".3"
              fill="currentColor"
            />

            <path
              d="M11 8.6H15"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
            />

            <!-- row 2 -->
            <rect
              x="8.2"
              y="11.8"
              width="1.2"
              height="1.2"
              rx=".3"
              fill="currentColor"
            />

            <path
              d="M11 12.4H15"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
            />

            <!-- row 3 -->
            <rect
              x="8.2"
              y="15.6"
              width="1.2"
              height="1.2"
              rx=".3"
              fill="currentColor"
            />

            <path
              d="M11 16.2H15"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
            />

          </svg>

        </div>

        <h3>{{ stats.tugasan }}</h3>

        <span>Tugasan</span>

      </div>

    </div>

    <!-- CONTENT GRID -->
    <div class="content-grid">

      <div class="panel">

        <div class="panel-header">

          <h2>Prestasi Organisasi</h2>

          <button
            class="link-btn"
            @click="goConfig"
          >
            Lihat semua
          </button>

        </div>

        <div v-if="organizations.length">

          <table class="performance-table">

            <thead>
              <tr>
                <th>Nama Organisasi</th>
                <th>Kemajuan</th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="org in paginatedOrganizations"
                :key="org.nama"
              >

                <td>

                  <div class="org-name">
                    {{ org.nama }}
                  </div>

                </td>

                <td>

                  <div class="progress-header">

                    <span>
                      {{ org.done }} / {{ org.total }}
                    </span>

                    <span class="progress-percent">
                      {{ getPercent(org.done, org.total) }}%
                    </span>

                  </div>

                  <div class="progress-bar">

                    <div
                      class="progress-fill"
                      :style="{
                        width:
                        getPercent(
                          org.done,
                          org.total
                        ) + '%'
                      }"
                    />

                  </div>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

        <div
          v-else
          class="empty"
        >
          Tiada data organisasi
        </div>

        <div
          v-if="totalPages > 1"
          class="pagination-wrapper"
        >

          <AppPagination
            :currentPage="currentPage"
            :totalPages="totalPages"
            @update:currentPage="
            (page)=>
            currentPage=page
            "
          />

        </div>

      </div>

      <div class="insight-card">

        <h2>
          Insight Minggu Ini
        </h2>

        <div class="top-org">

          <div class="avatar">

            {{
              topOrg?.nama?.charAt(0)
              || "O"
            }}

          </div>

          <div>

            <strong>
              {{ topOrg?.nama || "-" }}
            </strong>

          </div>

        </div>

        <div class="metric">

          <div class="metric-header">

            <span>
              Tugas Selesai
            </span>

            <strong>

              {{
                totalTasks
                ? Math.round(
                  (
                    completedTasks
                    /
                    totalTasks
                  )
                  *
                  100
                )
                : 0
              }}%

            </strong>

          </div>

          <div class="metric-bar">

            <div
              class="metric-fill success-fill"
              :style="{
                width:
                totalTasks
                ? Math.round(
                  (
                    completedTasks
                    /
                    totalTasks
                  )
                  *
                  100
                ) + '%'
                : '0%'
              }"
            />

          </div>

        </div>

        <div class="actions">

          <AppButton
            text="Konfigurasi"
            @click="goConfig"
          />

          <AppButton
            text="Pengguna"
            variant="outline"
            @click="goAccounts"
          />

        </div>

      </div>

    </div>

  </div>
</template>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-title h1 {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
}

.page-title p {
  margin-top: 4px;
  color: #64748b;
}

.filter-group {
  display: flex;
  gap: 8px;
}

.filter-group button {
  border: none;
  background: #f1f5f9;
  color: #64748b;
  padding: 8px 14px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.filter-group button.active {
  background: white;
  color: #4f46e5;
  border: 1px solid #c7d2fe;
}

/* =====================
   KPI
===================== */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
}

.card-icon {
  width: 26px;
  height: 26px;

  margin-bottom: 16px;

  display: flex;
  align-items: center;
  justify-content: flex-start;

  color: #6366f1;
}

.card-icon.success {
  color: #10b981;
}

.card-icon svg {
  width: 26px;
  height: 26px;

  fill: none;

  overflow: visible;

  stroke-linecap: round;
  stroke-linejoin: round;
}

/* END NEW */

.stat-card h3 {
  font-size: 34px;
  font-weight: 700;
  color: #334155;
}

.stat-card span {
  display: block;
  margin-top: 8px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: #94a3b8;
}

.success {
  color: #16a34a !important;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.panel,
.insight-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
}

.panel {
  overflow: hidden;
}

.panel-header {
  padding: 24px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h2,
.insight-card h2 {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.link-btn {
  background: none;
  border: none;
  color: #4f46e5;
  font-weight: 600;
  cursor: pointer;
}

.performance-table {
  width: 100%;
  border-collapse: collapse;
}

.performance-table th {
  text-align: left;
  background: #f8fafc;
  color: #64748b;
  padding: 16px 24px;
}

.performance-table td {
  padding: 20px 24px;
  border-top: 1px solid #f1f5f9;
}

.performance-table tr:hover {
  background: #fafafa;
}

.org-name {
  font-weight: 600;
  color: #334155;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.progress-percent {
  color: #4f46e5;
  font-weight: 700;
}

.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 999px;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  background: #4f46e5;
}

.insight-card {
  padding: 24px;
}

.top-org {
  display: flex;
  gap: 12px;
  margin: 24px 0;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  background: #e0e7ff;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.metric {
  margin-bottom: 20px;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.metric-bar {
  height: 6px;
  background: #e2e8f0;
  border-radius: 999px;
}

.metric-fill {
  height: 100%;
  border-radius: 999px;
}

.success-fill {
  background: #16a34a;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.actions :deep(button) {
  box-shadow: none !important;
}

.pagination-wrapper {
  padding: 16px;
}

.empty {
  padding: 40px;
  text-align: center;
  color: #94a3b8;
}

</style>