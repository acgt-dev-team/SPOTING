<script setup>
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import logo from "../assets/images/spoting-logo.png"

const route = useRoute()
const router = useRouter()

const user = ref({
  username: "Admin User",
  role: "Pentadbir"
})

const customerName = computed(() => "Kementerian Dalam Negeri")

const breadcrumbs = computed(() => {
  const path = route.path
  const organizationId = route.params.organizationId
  const subOrganizationId = route.params.subOrganizationId
  const siteId = route.params.siteId

  const crumbs = [
    {
      label: customerName.value,
      to: "/admin/configuration"
    }
  ]

  if (path.includes("/tugasan")) {
    crumbs.push(
      { label: "Senarai Organisasi", to: "/admin/configuration" },

      {
        label: "Senarai Sub Organisasi",
        to: organizationId
          ? `/admin/configuration/sub-organisasi/${organizationId}`
          : null
      },

      {
        label: "Senarai Tapak",
        to:
          organizationId && subOrganizationId
            ? `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}`
            : null
      },

      {
        label: "Senarai Profil",
        to:
          organizationId && subOrganizationId && siteId
            ? `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}/profil/${siteId}`
            : null
      },

      { label: "Senarai Tugasan", to: null }
    )

  } else if (path.includes("/profil")) {
    crumbs.push(
      { label: "Senarai Organisasi", to: "/admin/configuration" },

      {
        label: "Senarai Sub Organisasi",
        to: organizationId
          ? `/admin/configuration/sub-organisasi/${organizationId}`
          : null
      },

      {
        label: "Senarai Tapak",
        to:
          organizationId && subOrganizationId
            ? `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}`
            : null
      },

      { label: "Senarai Profil", to: null }
    )

  } else if (path.includes("/tapak")) {
    crumbs.push(
      { label: "Senarai Organisasi", to: "/admin/configuration" },

      {
        label: "Senarai Sub Organisasi",
        to: organizationId
          ? `/admin/configuration/sub-organisasi/${organizationId}`
          : null
      },

      { label: "Senarai Tapak", to: null }
    )

  } else if (path.includes("/sub-organisasi")) {
    crumbs.push(
      { label: "Senarai Organisasi", to: "/admin/configuration" },
      { label: "Senarai Sub Organisasi", to: null }
    )

  } else {
    crumbs.push({
      label: "Senarai Organisasi",
      to: null
    })
  }

  return crumbs
})

function goTo(crumb, index) {
  if (!crumb.to || index === breadcrumbs.value.length - 1) return
  router.push(crumb.to)
}

function logout() {
  localStorage.removeItem("token")
  localStorage.removeItem("role")
  router.push("/login")
}
</script>

<template>
  <div class="admin-layout">

    <!-- SIDEBAR -->
    <aside class="sidebar">

      <div class="sidebar-top">
        <div class="brand">
          <img :src="logo" class="logo" />
          <span class="brand-text">Paparan Pentadbir</span>
        </div>
      </div>

      <div></div>

      <div class="profile-card">
        <div class="profile-top">
          <div class="avatar">
            {{ user.username.charAt(0) }}
          </div>

          <div>
            <div class="username">{{ user.username }}</div>
            <div class="role">{{ user.role }}</div>
          </div>
        </div>

        <button class="logout-btn" @click="logout">
          Log keluar
        </button>
      </div>

    </aside>

    <!-- MAIN -->
    <div class="main-area">

      <div class="admin-container">

        <!-- HEADER -->
        <div class="page-top-header">

          <div class="breadcrumbs">
            <template
              v-for="(item, index) in breadcrumbs"
              :key="index"
            >
              <button
                v-if="item.to && index !== breadcrumbs.length - 1"
                class="crumb link"
                @click="goTo(item, index)"
              >
                {{ item.label }}
              </button>

              <span
                v-else
                class="crumb"
                :class="{ current: index === breadcrumbs.length - 1 }"
              >
                {{ item.label }}
              </span>

              <span
                v-if="index !== breadcrumbs.length - 1"
                class="divider"
              >
                ›
              </span>
            </template>
          </div>

          <div class="customer-block">
            <h2 class="customer-name">
              {{ customerName }}
            </h2>
          </div>

        </div>

        <router-view />

      </div>
    </div>

  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f7fb;
}

/* SIDEBAR */
.sidebar {
  width: 260px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 24px 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  width: 110px;
}

.brand-text {
  font-weight: 700;
  color: #020265;
  font-size: 16px;
}

/* USER */
.profile-card {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 16px;
}

.profile-top {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #1d4ed8;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.username {
  font-size: 14px;
  font-weight: 700;
}

.role {
  font-size: 12px;
  color: #6b7280;
}

.logout-btn {
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 10px;
  color: #dc2626;
  font-weight: 600;
  cursor: pointer;
}

.logout-btn:hover {
  background: #fef2f2;
}

/* MAIN */
.main-area {
  flex: 1;
}

.admin-container {
  padding: 24px 32px;
}

/* HEADER */
.page-top-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.crumb {
  font-size: 14px;
  font-weight: 700;
  color: #111827;
}

.crumb.current {
  color: #020265;
}

.link {
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
}

.link:hover {
  color: #020265;
}

.divider {
  color: #9ca3af;
}

/* RIGHT */
.customer-block {
  margin-left: auto;
}

.customer-name {
  font-size: 22px;
  font-weight: 500;
  color: #111827;
}
</style>