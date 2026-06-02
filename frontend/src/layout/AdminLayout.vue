<script setup>
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import logo from "../assets/images/spoting-logo.png"

import {
  LayoutDashboard,
  Settings,
  UserPlus,
  LogOut
} from "lucide-vue-next"

const route = useRoute()
const router = useRouter()

const currentRole = sessionStorage.getItem("role")

const user = ref({
  username: sessionStorage.getItem("username") || "User",
  role: sessionStorage.getItem("role") || "user"
})

const ministryName = computed(() => "Kementerian Dalam Negeri")

const menuItems = computed(() => {
  // user only sees configuration
  if (currentRole === "user") {
  return [
    {
      label: "Papan Pemuka",
      icon: LayoutDashboard,
      path: "/admin/dashboard",
      active: route.path.startsWith("/admin/dashboard")
    },
    {
      label: "Konfigurasi",
      icon: Settings,
      path: "/admin/configuration",
      active: route.path.startsWith("/admin/configuration")
    },
    {
      label: "Profil Saya",
      icon: UserPlus,
      path: "/admin/profile-user",
      active: route.path.startsWith("/admin/profile-user")
    }
  ]
}

  // admin + super admin
  return [
    {
      label: "Papan Pemuka",
      icon: LayoutDashboard,
      path: "/admin/dashboard",
      active: route.path.startsWith("/admin/dashboard")
    },
    {
      label: "Konfigurasi",
      icon: Settings,
      path: "/admin/configuration",
      active: route.path.startsWith("/admin/configuration")
    },
    {
      label: "Pengurusan Pengguna",
      icon: UserPlus,
      path: "/admin/accounts",
      active: route.path.startsWith("/admin/accounts")
    }
  ]
})

const breadcrumbs = computed(() => {
  const path = route.path
  const organizationId = route.params.organizationId
  const subOrganizationId = route.params.subOrganizationId
  const siteId = route.params.siteId

  const crumbs = [
    {
      label: ministryName.value,
      to: "/admin/configuration"
    }
  ]

  if (path.includes("/dashboard")) {
    crumbs.push({
      label: "Papan Pemuka",
      to: null
    })

  } else if (path.includes("/profile-user")) {
    crumbs.push({
      label: "Profil Saya",
      to: null
    })
  } else if (path.includes("/accounts")) {
    crumbs.push({
      label: "Pengurusan Pengguna",
      to: null
    })

  } else if (path.includes("/tugasan")) {
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

function goMenu(path) {
  router.push(path)
}

function goTo(crumb, index) {
  if (!crumb.to || index === breadcrumbs.value.length - 1) return
  router.push(crumb.to)
}

function logout() {

  sessionStorage.removeItem("token")
  sessionStorage.removeItem("role")
  sessionStorage.removeItem("username")
  sessionStorage.removeItem("forcePasswordChange")

  router.push("/login")

}

function goProfile() {
  router.push("/admin/profile-user")
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

        <div class="logo-divider"></div>

        <!-- MENU -->
        <div class="menu-list">
          <button
            v-for="item in menuItems"
            :key="item.path"
            class="menu-btn"
            :class="{ active: item.active }"
            @click="goMenu(item.path)"
          >
            <component :is="item.icon" size="18" />
            <span>{{ item.label }}</span>
          </button>
        </div>

      </div>

      <!-- PROFILE -->
      <div class="profile-card">

        <div
  class="profile-top clickable-profile"
  @click="goProfile"
>
          <div class="avatar">
            {{ user.username.charAt(0) }}
          </div>

          <div>
            <div class="username">{{ user.username }}</div>
            <div class="role">{{ user.role }}</div>
          </div>
        </div>

        <button class="logout-btn" @click="logout">
          <LogOut size="16" />
          <span>Log keluar</span>
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
              {{ ministryName }}
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
  min-height: 100vh;
  background: #f5f7fb;
}

/* SIDEBAR */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 240px; /* slightly reduced */
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-y: auto;
  z-index: 50;
}

.sidebar-top {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* BRAND */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 6px;
}

.logo-divider {
  width: 100%;
  height: 1px;
  background: #e5e7eb;
}

.logo {
  width: 110px;
}

.brand-text {
  font-weight: 700;
  color: #020265;
  font-size: 15px;
}

/* MENU */
.menu-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-btn {
  width: 100%;
  border: none;
  background: transparent;
  color: #374151;
  padding: 10px 12px;
  border-radius: 10px;
  text-align: left;
  font-weight: 600;
  cursor: pointer;
  transition: 0.15s ease;
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
}

/* Hover (light only) */
.menu-btn:hover {
  background: #f8fafc;
}

/* ACTIVE (clean style, no heavy block) */
.menu-btn.active {
  background: #eef2ff;
  color: #020265;
}

/* LEFT INDICATOR */
.menu-btn.active::before {
  content: "";
  position: absolute;
  left: 0;
  top: 6px;
  bottom: 6px;
  width: 3px;
  background: #020265;
  border-radius: 3px;
}

/* PROFILE (less "cardy") */
.profile-card {
  background: transparent;
  border: none;
  padding: 8px 4px;
}

.profile-top {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #1d4ed8;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.username {
  font-size: 13px;
  font-weight: 700;
}

.role {
  font-size: 11px;
  color: #6b7280;
}

/* LOGOUT */
.logout-btn {
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 8px;
  color: #dc2626;
  font-weight: 600;
  cursor: pointer;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: 0.15s ease;
}

.logout-btn:hover {
  background: #fef2f2;
}

/* MAIN */
.main-area {
  margin-left: 240px;
  width: calc(100% - 240px);
  min-height: 100vh;
}

.admin-container {
  padding: 24px;
}

/* HEADER */
.page-top-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

/* BREADCRUMBS */
.breadcrumbs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
}

.crumb {
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
}

.crumb.current {
  color: #020265;
  font-weight: 700;
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

/* Divider spacing fix */
.divider {
  color: #9ca3af;
  margin: 0 6px;
  vertical-align: middle;
  position: relative;
  top: -2px;
}

/* TITLE */
.customer-block {
  margin-left: auto;
}

.customer-name {
  font-size: 20px;
  font-weight: 500;
  color: #111827;
}

.clickable-profile {
  cursor: pointer;
  border-radius: 10px;
  padding: 6px;
  transition: 0.15s ease;
}

.clickable-profile:hover {
  background: #f3f4f6;
}
</style>