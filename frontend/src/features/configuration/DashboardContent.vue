<script setup>
import { computed, onMounted, ref, watch } from "vue"
import { useRouter } from "vue-router"
import {
  Activity,
  AlertTriangle,
  Building2,
  CalendarClock,
  CheckCircle2,
  ClipboardList,
  Clock3,
  MapPin,
  Network,
  RefreshCcw,
  Settings,
  UserRound,
  Users
} from "lucide-vue-next"
import api from "../../services/api"
import { t } from "../../i18n"
import { useToast } from "../../ui/AppToast.vue"
import AppButton from "../../ui/AppButton.vue"
import AppPagination from "../../ui/AppPagination.vue"
import PageHeader from "../../ui/PageHeader.vue"

const router = useRouter()
const toast = useToast()

const loading = ref(false)
const loadError = ref("")
const updatedAt = ref(null)
const activeHealthFilter = ref("")

const stats = ref({
  organisasi: 0,
  sub_organisasi: 0,
  tapak: 0,
  profil: 0,
  tugasan: 0
})

const organizations = ref([])
const profileHealth = ref({
  counts: {},
  profiles: [],
  failed_profiles: [],
  scheduled_profiles: [],
  recent_profiles: []
})

const currentPage = ref(1)
const itemsPerPage = 8
const healthFilterPage = ref(1)
const healthFilterPerPage = 8

const healthCounts = computed(() => profileHealth.value.counts || {})

const healthCards = computed(() => [
  {
    key: "not_started",
    label: t("status.notStarted"),
    value: healthCounts.value.not_started || 0,
    icon: Clock3,
    tone: "idle"
  },
  {
    key: "in_process",
    label: t("status.inProcess"),
    value: healthCounts.value.in_process || 0,
    icon: Activity,
    tone: "warning"
  },
  {
    key: "scheduled",
    label: t("status.scheduled"),
    value: healthCounts.value.scheduled || 0,
    icon: CalendarClock,
    tone: "scheduled"
  },
  {
    key: "completed",
    label: t("status.completed"),
    value: healthCounts.value.completed || 0,
    icon: CheckCircle2,
    tone: "success"
  },
  {
    key: "failed",
    label: t("status.failed"),
    value: healthCounts.value.failed || 0,
    icon: AlertTriangle,
    tone: "danger"
  }
])

const statCards = computed(() => [
  {
    label: t("dashboard.statLabels.organization"),
    value: stats.value.organisasi,
    icon: Building2,
    tone: "primary"
  },
  {
    label: t("dashboard.statLabels.subOrganization"),
    value: stats.value.sub_organisasi,
    icon: Network,
    tone: "cyan"
  },
  {
    label: t("dashboard.statLabels.site"),
    value: stats.value.tapak,
    icon: MapPin,
    tone: "amber"
  },
  {
    label: t("dashboard.statLabels.profile"),
    value: stats.value.profil,
    icon: UserRound,
    tone: "violet"
  },
  {
    label: t("dashboard.statLabels.task"),
    value: stats.value.tugasan,
    icon: ClipboardList,
    tone: "success"
  }
])

const setupSteps = computed(() => [
  {
    label: t("dashboard.statLabels.organization"),
    done: stats.value.organisasi > 0
  },
  {
    label: t("dashboard.statLabels.subOrganization"),
    done: stats.value.sub_organisasi > 0
  },
  {
    label: t("dashboard.statLabels.site"),
    done: stats.value.tapak > 0
  },
  {
    label: t("dashboard.statLabels.profile"),
    done: stats.value.profil > 0
  },
  {
    label: t("dashboard.statLabels.task"),
    done: stats.value.tugasan > 0
  }
])

const showSetupChecklist = computed(() =>
  setupSteps.value.some((step) => !step.done)
)

const sortedOrganizations = computed(() => {
  return [...organizations.value].sort(
    (a, b) => getPercent(b.done, b.total) - getPercent(a.done, a.total)
  )
})

const totalPages = computed(() =>
  Math.ceil(sortedOrganizations.value.length / itemsPerPage)
)

const paginatedOrganizations = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedOrganizations.value.slice(start, start + itemsPerPage)
})

const totalTasks = computed(() =>
  organizations.value.reduce((sum, organization) => sum + organization.total, 0)
)

const completedTasks = computed(() =>
  organizations.value.reduce((sum, organization) => sum + organization.done, 0)
)

const completionRate = computed(() =>
  totalTasks.value ? Math.round((completedTasks.value / totalTasks.value) * 100) : 0
)

const topOrg = computed(() => {
  if (!organizations.value.length) return null

  return sortedOrganizations.value[0]
})

const failedProfiles = computed(() =>
  profileHealth.value.failed_profiles || []
)

const dashboardProfiles = computed(() =>
  profileHealth.value.profiles || []
)

const scheduledProfiles = computed(() =>
  profileHealth.value.scheduled_profiles || []
)

const recentProfiles = computed(() =>
  profileHealth.value.recent_profiles || []
)

const activeHealthCard = computed(() =>
  healthCards.value.find((card) => card.key === activeHealthFilter.value) || null
)

const filteredHealthProfiles = computed(() => {
  if (!activeHealthFilter.value) return []

  return dashboardProfiles.value.filter(
    (profile) => profile.status_key === activeHealthFilter.value
  )
})

const healthFilterTotalPages = computed(() =>
  Math.ceil(filteredHealthProfiles.value.length / healthFilterPerPage)
)

const paginatedHealthProfiles = computed(() => {
  const start = (healthFilterPage.value - 1) * healthFilterPerPage
  return filteredHealthProfiles.value.slice(start, start + healthFilterPerPage)
})

const hasDashboardData = computed(() =>
  Boolean(updatedAt.value || organizations.value.length || dashboardProfiles.value.length)
)

const updatedAtLabel = computed(() => {
  if (!updatedAt.value) return ""
  return t("dashboard.dataUpdated", {
    time: updatedAt.value.toLocaleTimeString("ms-MY", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false
    })
  })
})

watch(organizations, () => {
  currentPage.value = 1
})

watch([activeHealthFilter, filteredHealthProfiles], () => {
  healthFilterPage.value = 1
})

watch(filteredHealthProfiles, () => {
  if (healthFilterPage.value > healthFilterTotalPages.value) {
    healthFilterPage.value = healthFilterTotalPages.value || 1
  }
})

onMounted(() => {
  loadDashboard()
})

async function loadDashboard() {
  loading.value = true

  try {
    loadError.value = ""
    const res = await api.get("/dashboard/full")
    const data = res.data || {}

    stats.value = data.stats || stats.value
    organizations.value = data.organizations || []
    profileHealth.value = data.profile_health || profileHealth.value
    updatedAt.value = new Date()
  } catch (err) {
    console.error("Dashboard API error:", err)
    loadError.value = t("dashboard.loadFailed")
    toast.error(t("common.loadFailed", { entity: t("layout.menu.dashboard") }))
  } finally {
    loading.value = false
  }
}

function formatNumber(num) {
  if (num >= 1000) return `${(num / 1000).toFixed(1)}k`
  return num
}

function getPercent(done, total) {
  return total ? Math.round((done / total) * 100) : 0
}

function formatDateTime(value) {
  if (!value) return t("common.emptyValue")

  return new Date(value).toLocaleString("ms-MY", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  })
}

function statusLabel(statusKey) {
  const labels = {
    not_started: t("status.notStarted"),
    in_process: t("status.inProcess"),
    scheduled: t("status.scheduled"),
    completed: t("status.completed"),
    failed: t("status.failed")
  }

  return labels[statusKey] || t("status.unknown")
}

function scheduleLabel(profile) {
  if (profile.cron_enabled) {
    return profile.frequency || profile.cron_expression || t("schedule.cronJob")
  }

  if (profile.scheduled_at) {
    return formatDateTime(profile.scheduled_at)
  }

  return t("schedule.scheduled")
}

function toggleHealthFilter(key) {
  activeHealthFilter.value = activeHealthFilter.value === key ? "" : key
}

function clearHealthFilter() {
  activeHealthFilter.value = ""
}

function goConfig() {
  router.push("/admin/configuration")
}

function goAccounts() {
  router.push("/admin/accounts")
}

function goProfileTasks(profile) {
  if (
    !profile.organisasi_id ||
    !profile.sub_organisasi_id ||
    !profile.tapak_id ||
    !profile.id
  ) {
    goConfig()
    return
  }

  router.push(
    `/admin/configuration/sub-organisasi/${profile.organisasi_id}/tapak/${profile.sub_organisasi_id}/profil/${profile.tapak_id}/tugasan/${profile.id}`
  )
}
</script>

<template>
  <div class="dashboard-container">
    <PageHeader
      :title="t('dashboard.pageTitle')"
      :description="t('dashboard.pageDescription')"
    >
      <template #actions>
        <span v-if="updatedAtLabel" class="updated-pill">
          {{ updatedAtLabel }}
        </span>

        <button
          class="ui-button ui-button--outline"
          type="button"
          :disabled="loading"
          @click="loadDashboard"
        >
          <RefreshCcw :size="17" aria-hidden="true" />
          {{ t("dashboard.refresh") }}
        </button>
      </template>
    </PageHeader>

    <section v-if="loadError" class="retry-panel">
      <div class="retry-panel__icon">
        <AlertTriangle :size="22" aria-hidden="true" />
      </div>

      <div>
        <h2>{{ loadError }}</h2>
        <p>{{ t("dashboard.retryDescription") }}</p>
      </div>

      <button
        class="ui-button ui-button--primary"
        type="button"
        :disabled="loading"
        @click="loadDashboard"
      >
        <RefreshCcw :size="17" aria-hidden="true" />
        {{ t("dashboard.refresh") }}
      </button>
    </section>

    <template v-if="!loadError || hasDashboardData">
    <section class="stats-grid" aria-label="Dashboard summary">
      <article
        v-for="card in statCards"
        :key="card.label"
        class="stat-card"
        :class="`stat-card--${card.tone}`"
      >
        <div class="stat-card__icon">
          <component :is="card.icon" :size="24" aria-hidden="true" />
        </div>

        <div>
          <h3>{{ formatNumber(card.value) }}</h3>
          <span>{{ card.label }}</span>
        </div>
      </article>
    </section>

    <section class="health-section">
      <div class="section-heading">
        <h2>{{ t("dashboard.healthTitle") }}</h2>
        <span>{{ t("dashboard.completionRate") }}: {{ completionRate }}%</span>
      </div>

      <div class="health-grid">
        <button
          v-for="card in healthCards"
          :key="card.key"
          type="button"
          class="health-card"
          :class="[
            `health-card--${card.tone}`,
            { active: activeHealthFilter === card.key }
          ]"
          :aria-pressed="activeHealthFilter === card.key"
          @click="toggleHealthFilter(card.key)"
        >
          <component :is="card.icon" :size="20" aria-hidden="true" />
          <div>
            <strong>{{ card.value }}</strong>
            <span>{{ card.label }}</span>
          </div>
        </button>
      </div>
    </section>

    <section v-if="activeHealthFilter" class="panel filtered-panel">
      <div class="panel-header">
        <div>
          <h2>{{ t("dashboard.filteredProfiles") }}</h2>
          <p>
            {{ activeHealthCard?.label || t("common.status") }}
            -
            {{ filteredHealthProfiles.length }} {{ t("dashboard.statLabels.profile") }}
          </p>
        </div>

        <button
          class="link-btn"
          type="button"
          @click="clearHealthFilter"
        >
          {{ t("common.clear") }}
        </button>
      </div>

      <div v-if="filteredHealthProfiles.length">
        <div class="filtered-profile-grid">
          <button
            v-for="profile in paginatedHealthProfiles"
            :key="profile.id"
            class="profile-row"
            type="button"
            @click="goProfileTasks(profile)"
          >
            <div>
              <strong>{{ profile.nama }}</strong>
              <span>{{ profile.organisasi }} / {{ profile.tapak }}</span>
            </div>
            <span class="row-meta">{{ statusLabel(profile.status_key) }}</span>
          </button>
        </div>

        <div
          v-if="healthFilterTotalPages > 1"
          class="pagination-wrapper"
        >
          <AppPagination
            :currentPage="healthFilterPage"
            :totalPages="healthFilterTotalPages"
            @update:page="healthFilterPage = $event"
          />
        </div>
      </div>

      <div v-else class="empty-state">
        {{ t("dashboard.noFilteredProfiles") }}
      </div>
    </section>

    <section v-if="showSetupChecklist" class="setup-panel">
      <div>
        <h2>{{ t("dashboard.setupChecklist") }}</h2>
        <p>{{ t("dashboard.setupDescription") }}</p>
      </div>

      <div class="setup-steps">
        <div
          v-for="step in setupSteps"
          :key="step.label"
          class="setup-step"
          :class="{ complete: step.done }"
        >
          <CheckCircle2 :size="16" aria-hidden="true" />
          <span>{{ step.label }}</span>
        </div>
      </div>
    </section>

    <div class="dashboard-layout">
      <main class="dashboard-main">
        <section class="panel">
          <div class="panel-header">
            <div>
              <h2>{{ t("dashboard.organizationPerformance") }}</h2>
              <p>{{ completedTasks }} / {{ totalTasks }} {{ t("dashboard.taskComplete") }}</p>
            </div>

            <button
              class="link-btn"
              type="button"
              @click="goConfig"
            >
              {{ t("dashboard.actions.viewAll") }}
            </button>
          </div>

          <div v-if="organizations.length" class="table-wrap">
            <table class="performance-table">
              <thead>
                <tr>
                  <th>{{ t("configuration.organization.name") }}</th>
                  <th>{{ t("common.progress") }}</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="org in paginatedOrganizations"
                  :key="org.nama"
                >
                  <td>
                    <div class="org-name">{{ org.nama }}</div>
                  </td>

                  <td>
                    <div class="progress-header">
                      <span>{{ org.done }} / {{ org.total }}</span>
                      <strong>{{ getPercent(org.done, org.total) }}%</strong>
                    </div>

                    <div class="progress-bar">
                      <div
                        class="progress-fill"
                        :style="{ width: `${getPercent(org.done, org.total)}%` }"
                      />
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <div
              v-if="totalPages > 1"
              class="pagination-wrapper"
            >
              <AppPagination
                :currentPage="currentPage"
                :totalPages="totalPages"
                @update:page="currentPage = $event"
              />
            </div>
          </div>

          <div v-else class="empty-state">
            {{ t("dashboard.emptyOrganizations") }}
          </div>
        </section>

        <div class="operational-grid">
          <section class="panel panel--danger">
            <div class="panel-header">
              <div>
                <h2>{{ t("dashboard.failedProfiles") }}</h2>
                <p>{{ failedProfiles.length }} {{ t("status.failed") }}</p>
              </div>
              <AlertTriangle :size="22" aria-hidden="true" />
            </div>

            <div v-if="failedProfiles.length" class="list-stack">
              <button
                v-for="profile in failedProfiles"
                :key="profile.id"
                class="profile-row"
                type="button"
                @click="goProfileTasks(profile)"
              >
                <div>
                  <strong>{{ profile.nama }}</strong>
                  <span>{{ profile.organisasi }} / {{ profile.tapak }}</span>
                </div>
                <span class="row-meta">{{ profile.task_count }} {{ t("dashboard.statLabels.task") }}</span>
              </button>
            </div>

            <div v-else class="empty-state">
              {{ t("dashboard.noFailedProfiles") }}
            </div>
          </section>

          <section class="panel">
            <div class="panel-header">
              <div>
                <h2>{{ t("dashboard.scheduledRuns") }}</h2>
                <p>{{ scheduledProfiles.length }} {{ t("status.scheduled") }}</p>
              </div>
              <CalendarClock :size="22" aria-hidden="true" />
            </div>

            <div v-if="scheduledProfiles.length" class="list-stack">
              <button
                v-for="profile in scheduledProfiles"
                :key="profile.id"
                class="profile-row"
                type="button"
                @click="goProfileTasks(profile)"
              >
                <div>
                  <strong>{{ profile.nama }}</strong>
                  <span>{{ profile.tapak }}</span>
                </div>
                <span class="row-meta">{{ scheduleLabel(profile) }}</span>
              </button>
            </div>

            <div v-else class="empty-state">
              {{ t("dashboard.noScheduledProfiles") }}
            </div>
          </section>
        </div>
      </main>

      <aside class="dashboard-side">
        <section class="panel quick-panel">
          <div class="panel-header compact">
            <h2>{{ t("dashboard.quickActions") }}</h2>
          </div>

          <div class="quick-actions">
            <AppButton
              :text="t('dashboard.actions.openConfiguration')"
              @click="goConfig"
            >
              <template #icon>
                <Settings :size="17" aria-hidden="true" />
              </template>
            </AppButton>

            <button
              class="quick-action"
              type="button"
              @click="goConfig"
            >
              <Building2 :size="18" aria-hidden="true" />
              <span>{{ t("dashboard.actions.createOrganization") }}</span>
            </button>

            <button
              class="quick-action"
              type="button"
              @click="goAccounts"
            >
              <Users :size="18" aria-hidden="true" />
              <span>{{ t("dashboard.actions.accounts") }}</span>
            </button>
          </div>
        </section>

        <section class="panel insight-panel">
          <div class="panel-header compact">
            <h2>{{ t("dashboard.insightTitle") }}</h2>
          </div>

          <div class="top-org">
            <div class="avatar">
              {{ topOrg?.nama?.charAt(0) || t("dashboard.statLabels.organization").charAt(0) }}
            </div>

            <div>
              <strong>{{ topOrg?.nama || t("common.emptyValue") }}</strong>
              <span>{{ t("dashboard.completionRate") }}: {{ topOrg ? getPercent(topOrg.done, topOrg.total) : 0 }}%</span>
            </div>
          </div>

          <div class="metric">
            <div class="metric-header">
              <span>{{ t("dashboard.taskComplete") }}</span>
              <strong>{{ completionRate }}%</strong>
            </div>

            <div class="metric-bar">
              <div
                class="metric-fill"
                :style="{ width: `${completionRate}%` }"
              />
            </div>
          </div>
        </section>

        <section class="panel">
          <div class="panel-header compact">
            <h2>{{ t("dashboard.recentActivity") }}</h2>
          </div>

          <div v-if="recentProfiles.length" class="timeline">
            <button
              v-for="profile in recentProfiles"
              :key="profile.id"
              class="timeline-item"
              type="button"
              @click="goProfileTasks(profile)"
            >
              <span class="timeline-dot" :class="`timeline-dot--${profile.status_key}`" />
              <div>
                <strong>{{ profile.nama }}</strong>
                <span>{{ statusLabel(profile.status_key) }} - {{ formatDateTime(profile.updated_at) }}</span>
              </div>
            </button>
          </div>

          <div v-else class="empty-state">
            {{ t("dashboard.noRecentActivity") }}
          </div>
        </section>
      </aside>
    </div>
    </template>
  </div>
</template>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.updated-pill {
  height: 40px;
  padding: 0 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  background: var(--color-surface-muted);
  color: var(--color-text-muted);
  display: inline-flex;
  align-items: center;
  font-size: 13px;
  font-weight: 700;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
}

.stat-card,
.panel,
.health-section,
.setup-panel,
.retry-panel {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
}

.retry-panel {
  padding: 18px 20px;
  border-color: rgba(220, 38, 38, 0.22);
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 14px;
}

.retry-panel__icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-lg);
  background: var(--color-danger-soft);
  color: var(--color-danger);
  display: flex;
  align-items: center;
  justify-content: center;
}

.retry-panel h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 16px;
  font-weight: 800;
}

.retry-panel p {
  margin: 4px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.stat-card {
  min-height: 132px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 14px;
}

.stat-card__icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-lg);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.stat-card--cyan .stat-card__icon {
  background: #ecfeff;
  color: #0891b2;
}

.stat-card--amber .stat-card__icon {
  background: #fffbeb;
  color: #d97706;
}

.stat-card--violet .stat-card__icon {
  background: #f5f3ff;
  color: #7c3aed;
}

.stat-card--success .stat-card__icon {
  background: var(--color-success-soft);
  color: var(--color-success);
}

.stat-card h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 32px;
  line-height: 1;
}

.stat-card span {
  display: block;
  margin-top: 8px;
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.health-section {
  padding: 20px;
}

.section-heading,
.panel-header,
.setup-panel {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.section-heading {
  margin-bottom: 16px;
  align-items: center;
}

.section-heading h2,
.panel-header h2,
.setup-panel h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 18px;
  font-weight: 800;
}

.section-heading span,
.panel-header p,
.setup-panel p {
  margin: 6px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.health-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
}

.health-card {
  min-height: 82px;
  padding: 14px;
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  background: var(--color-surface-muted);
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  font: inherit;
  text-align: left;
  transition: border-color var(--transition-base), box-shadow var(--transition-base), transform var(--transition-base);
}

.health-card:hover,
.health-card.active {
  border-color: var(--color-focus-border);
  box-shadow: var(--focus-ring);
}

.health-card:active {
  transform: translateY(1px);
}

.health-card strong {
  display: block;
  color: var(--color-text);
  font-size: 22px;
  line-height: 1;
}

.health-card span {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  font-weight: 700;
}

.health-card--warning {
  background: var(--color-warning-soft);
  color: var(--color-warning);
}

.health-card--scheduled {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.health-card--success {
  background: var(--color-success-soft);
  color: var(--color-success);
}

.health-card--danger {
  background: var(--color-danger-soft);
  color: var(--color-danger);
}

.filtered-panel {
  overflow: hidden;
}

.filtered-profile-grid {
  padding: 16px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.setup-panel {
  padding: 20px;
}

.setup-steps {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  flex-wrap: wrap;
}

.setup-step {
  min-height: 36px;
  padding: 0 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  color: var(--color-text-muted);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
}

.setup-step.complete {
  border-color: transparent;
  background: var(--color-success-soft);
  color: var(--color-success);
}

.dashboard-layout {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(320px, 0.85fr);
  gap: 24px;
  align-items: start;
}

.dashboard-main,
.dashboard-side {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.operational-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.panel {
  overflow: hidden;
}

.panel--danger {
  border-color: rgba(220, 38, 38, 0.22);
}

.panel-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
  align-items: center;
}

.panel-header.compact {
  padding-bottom: 14px;
}

.link-btn {
  border: 0;
  background: transparent;
  color: var(--color-primary);
  cursor: pointer;
  font: inherit;
  font-weight: 800;
}

.link-btn:hover {
  color: var(--color-primary-hover);
}

.table-wrap {
  overflow-x: auto;
}

.performance-table {
  width: 100%;
  min-width: 620px;
  border-collapse: collapse;
}

.performance-table th {
  padding: 14px 24px;
  background: var(--color-surface-muted);
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 800;
  text-align: left;
  text-transform: uppercase;
}

.performance-table td {
  padding: 18px 24px;
  border-top: 1px solid var(--color-border);
}

.performance-table tr:hover {
  background: var(--color-surface-hover);
}

.org-name {
  color: var(--color-text);
  font-weight: 800;
}

.progress-header,
.metric-header {
  margin-bottom: 8px;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 13px;
}

.progress-header strong {
  color: var(--color-primary);
}

.progress-bar,
.metric-bar {
  height: 8px;
  overflow: hidden;
  border-radius: var(--radius-pill);
  background: var(--color-surface-hover);
}

.progress-fill,
.metric-fill {
  height: 100%;
  border-radius: var(--radius-pill);
  background: var(--color-primary);
}

.pagination-wrapper {
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
}

.list-stack,
.quick-actions,
.timeline {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.profile-row,
.quick-action,
.timeline-item {
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  color: var(--color-text);
  cursor: pointer;
  font: inherit;
  text-align: left;
  transition: border-color var(--transition-base), background var(--transition-base);
}

.profile-row {
  min-height: 72px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.profile-row:hover,
.quick-action:hover,
.timeline-item:hover {
  border-color: var(--color-focus-border);
  background: var(--color-primary-soft);
}

.profile-row strong,
.timeline-item strong {
  display: block;
  color: var(--color-text);
  font-weight: 800;
}

.profile-row span,
.timeline-item span {
  display: block;
  margin-top: 4px;
  color: var(--color-text-muted);
  font-size: 12px;
}

.row-meta {
  max-width: 160px;
  margin-top: 0 !important;
  text-align: right;
  font-weight: 800;
}

.quick-actions :deep(.ui-button) {
  width: 100%;
  justify-content: center;
}

.quick-action {
  min-height: 46px;
  padding: 0 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
}

.insight-panel {
  padding-bottom: 18px;
}

.top-org {
  padding: 0 24px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.top-org strong,
.top-org span {
  display: block;
}

.top-org span {
  margin-top: 4px;
  color: var(--color-text-muted);
  font-size: 13px;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-pill);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
}

.metric {
  padding: 0 24px;
}

.metric-fill {
  background: var(--color-success);
}

.timeline-item {
  min-height: 58px;
  padding: 10px 12px;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 10px;
}

.timeline-dot {
  width: 10px;
  height: 10px;
  margin-top: 6px;
  border-radius: 50%;
  background: var(--color-text-muted);
}

.timeline-dot--not_started {
  background: var(--color-text-muted);
}

.timeline-dot--in_process,
.timeline-dot--scheduled {
  background: var(--color-warning);
}

.timeline-dot--completed {
  background: var(--color-success);
}

.timeline-dot--failed {
  background: var(--color-danger);
}

.empty-state {
  padding: 32px 24px;
  color: var(--color-text-muted);
  text-align: center;
}

@media (max-width: 1180px) {
  .stats-grid,
  .health-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .dashboard-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 780px) {
  .stats-grid,
  .health-grid,
  .filtered-profile-grid,
  .operational-grid {
    grid-template-columns: 1fr;
  }

  .retry-panel {
    grid-template-columns: 1fr;
  }

  .setup-panel,
  .section-heading,
  .panel-header {
    flex-direction: column;
    align-items: stretch;
  }

  .setup-steps {
    justify-content: flex-start;
  }

  .profile-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .row-meta {
    max-width: none;
    text-align: left;
  }
}
</style>
