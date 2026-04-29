<script setup>
import { computed, ref } from "vue"
import { useRouter } from "vue-router"

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
// DATA
// =======================
const organizations = ref([
  { bil: 1, nama: "KDN", done: 1233, total: 9000 },
  { bil: 2, nama: "KKM", done: 850, total: 4200 },
  { bil: 3, nama: "KPM", done: 2145, total: 6400 }
])

// =======================
// COMPUTED
// =======================
const totalOrganizations = computed(() => organizations.value.length)

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
  Math.round((done / total) * 100)

const topOrg = computed(() => {
  return [...organizations.value].sort(
    (a, b) => getPercent(b.done, b.total) - getPercent(a.done, a.total)
  )[0]
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
          {{ totalOrganizations }}
        </div>
        <div class="label">Jumlah organisasi</div>
      </div>

      <div class="stat-card">
        <div class="number blue">
          {{ formatNumber(120) }}
        </div>
        <div class="label">Jumlah profil</div>
      </div>

      <div class="stat-card">
        <div class="number green">
          {{ formatNumber(completedTasks) }}
          <span>/ {{ formatNumber(totalTasks) }}</span>
        </div>
        <div class="label">Jumlah tugasan</div>
      </div>

      <div class="stat-card">
        <div class="number green">
          {{ formatNumber(completedTasks) }}
        </div>
        <div class="label">Jumlah peranti selesai</div>
      </div>

    </div>

    <!-- GRID -->
    <div class="grid">

      <!-- TABLE -->
      <div class="panel">
        <div class="panel-header">
          <h2>Prestasi Organisasi</h2>
          <button class="btn" @click="goConfig">Lihat semua</button>
        </div>

        <div v-if="organizations.length" class="table">
          <div class="row header">
            <div>Bil</div>
            <div>Nama</div>
            <div>Kemajuan</div>
          </div>

          <div
            v-for="org in organizations"
            :key="org.bil"
            class="row hover"
          >
            <div>{{ org.bil }}</div>
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
      </div>

      <!-- SIDE -->
      <div class="panel">
        <h2>Insight</h2>

        <div class="insight">
          <p>Organisasi terbaik:</p>

          <div class="insight-row">
            <strong>{{ topOrg?.nama }}</strong>
            <span class="percent">
              {{ getPercent(topOrg?.done, topOrg?.total) }}%
            </span>
          </div>
        </div>

        <div class="actions">
          <button class="btn primary" @click="goConfig">
            Konfigurasi
          </button>

          <button class="btn" @click="goAccounts">
            Pengguna
          </button>
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
  padding: 8px 12px;
  border-radius: 8px;
  border: none;
  background: #f1f5f9;
  cursor: pointer;
  font-weight: 600;
}

.filters .active {
  background: #020265;
  color: white;
}

/* STATS */
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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

/* NUMBER */
.number {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.number span {
  font-size: 14px;
  margin-left: 6px;
  color: #6b7280;
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
}

.panel {
  background: white;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
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
  margin: 16px 0;
}

.insight-row {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
}

.percent {
  color: #16a34a;
  font-weight: 700;
}

/* BUTTONS */
.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  background: white;
  font-weight: 600;
}

.btn:hover {
  background: #f8fafc;
}

.btn.primary {
  background: #020265;
  color: white;
  border: none;
}
</style>