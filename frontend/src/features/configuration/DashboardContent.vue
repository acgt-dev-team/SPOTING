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
    const statsRes = await api.get("/dashboard")
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
  <div class="dashboard">

    <!-- HEADER -->
    <div class="header">
      <div>
        <h1>Papan Pemuka</h1>
        <p>Ringkasan prestasi sistem pentadbiran</p>
      </div>

      <div class="filters">
        <button
          v-for="r in ranges"
          :key="r.value"
          :class="{ active: selectedRange === r.value }"
          @click="selectedRange = r.value"
        >
          {{ r.label }}
        </button>
      </div>
    </div>

    <!-- STATS -->
    <div class="stats">

      <div class="stat-card">
        <div class="number blue">
          {{ stats.organisasi }}
        </div>
        <div class="label">Organisasi</div>
      </div>

      <div class="stat-card">
        <div class="number blue">
          {{ stats.sub_organisasi }}
        </div>
        <div class="label">Sub Organisasi</div>
      </div>

      <div class="stat-card">
        <div class="number blue">
          {{ stats.tapak }}
        </div>
        <div class="label">Tapak</div>
      </div>

      <div class="stat-card">
        <div class="number blue">
          {{ stats.profil }}
        </div>
        <div class="label">Profil</div>
      </div>

      <div class="stat-card">
        <div class="number green">
          {{ stats.tugasan }}
        </div>
        <div class="label">Tugasan</div>
      </div>

    </div>

    <!-- GRID -->
    <div class="grid">

      <!-- TABLE -->
      <div class="panel">
        <div class="panel-header">
          <h2>Prestasi Organisasi</h2>
          <AppButton text="Lihat semua" variant="outline" @click="goConfig" />
        </div>

        <div v-if="organizations.length" class="table">
          <div class="row header">
            <div>Bil</div>
            <div>Nama</div>
            <div>Kemajuan</div>
          </div>

          <div
            v-for="(org, index) in paginatedOrganizations"
            :key="org.bil"
            class="row hover"
          >
            <div>{{ (currentPage - 1) * itemsPerPage + index + 1 }}</div>
            <div>{{ org.nama }}</div>

            <div>
              <div class="bar">
                <div
                  class="fill"
                  :style="{ width: getPercent(org.done, org.total) + '%' }"
                ></div>
              </div>
              <small>
                {{ org.done }} / {{ org.total }} ({{ getPercent(org.done, org.total) }}%)
              </small>
            </div>
          </div>
        </div>

        <div v-else class="empty">
          Tiada data organisasi
        </div>

      <!-- ✅ pagination inside the same panel -->
      <div class="pagination-wrapper" v-if="totalPages > 1">
        <AppPagination
          :currentPage="currentPage"
          :totalPages="totalPages"
          @update:currentPage="(page) => currentPage = page"
        />
      </div>

      </div>

      <!-- SIDE -->
      <div class="panel">
        <h2>Insight</h2>

        <div class="insight">
          <p>Organisasi terbaik:</p>

          <div class="insight-row">
            <strong>{{ topOrg?.nama || "-" }}</strong>
            <span class="percent">
              {{ topOrg ? getPercent(topOrg.done, topOrg.total) + "%" : "-" }}
            </span>
          </div>
        </div>

        <div class="actions">
          <AppButton text="Konfigurasi" @click="goConfig" />
          <AppButton text="Pengguna" variant="outline" @click="goAccounts" />
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* HEADER */
.header {
  display: flex;
  justify-content: space-between;
}

/* FILTER */
.filters button {
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  font-weight: 600;
  color: #6b7280;
  transition: 0.2s ease;
}

.filters button:hover {
  background: #f8fafc;
}

.filters .active {
  background: #eef2ff;
  color: #020265;
  border: 1px solid #c7d2fe;
}

/* STATS */
.stats {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.stat-card {
  background: #ffffff;
  padding: 22px;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
  transition: 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.number {
  font-size: 32px;
  font-weight: 800;
}

.blue {
  color: #2563eb;
}

.green {
  color: #16a34a;
}

.label {
  margin-top: 8px;
  font-size: 14px;
  color: #6b7280;
}

/* GRID */
.grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  align-items: start;
}

.panel {
  background: white;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* TABLE */
.row {
  display: grid;
  grid-template-columns: 60px 1fr 200px;
  padding: 16px 12px;
}

.hover:hover {
  background: #f8fafc;
}

/* BAR */
.bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 999px;
}

.fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #2563eb, #3b82f6);
}

/* INSIGHT */
.insight {
  margin: 12px 0;
}

.insight-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
}

.percent {
  color: #16a34a;
  font-weight: 700;
  font-size: 14px;
}

/* ACTIONS (buttons area) */
.actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

/* Removed heavy shadow from AppButton ONLY here */
.actions :deep(button) {
  box-shadow: none !important;
  transform: none !important;
}
</style>