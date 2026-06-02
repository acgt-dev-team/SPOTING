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

      <div>

        <!-- LOGO -->
        <div class="logo-section">
          <img :src="logo" class="logo" />
        </div>

        <!-- MENU -->
        <nav class="menu-list">

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

        </nav>

      </div>

      <!-- PROFILE -->
      <div class="profile-section">

        <div class="profile-card">

        <div
  class="profile-top clickable-profile"
  @click="goProfile"
>
          <div class="avatar">
            {{ user.username.charAt(0).toUpperCase() }}
          </div>

          <div class="profile-info">
            <div class="username">
              {{ user.username }}
            </div>

            <div class="role">
              {{ user.role }}
            </div>
          </div>

        </div>

        <button
          class="logout-btn"
          @click="logout"
        >
          <LogOut size="14" />
          <span>Log keluar</span>
        </button>

        </div>

      </div>

    </aside>

    <!-- MAIN -->
    <main class="main-content">

      <!-- HEADER -->
      <header class="top-header">

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

        <div class="header-right">
          {{ ministryName }}
        </div>

      </header>

      <!-- PAGE CONTENT -->
      <div class="content-wrapper">
        <router-view />
      </div>

    </main>

  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
  font-family: "Plus Jakarta Sans", sans-serif;
}

/* =========================
   SIDEBAR
========================= */

.sidebar {
  width: 256px;
  background: white;
  border-right: 1px solid #e2e8f0;

  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;

  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* LOGO SECTION */

.logo-section {
  height: 64px;
  padding: 0 24px;

  display: flex;
  align-items: center;

  border-bottom: 1px solid #e2e8f0;

  box-sizing: border-box;
}

.logo {
  width: 170px;
  display: block;
}

/* MENU */

.menu-list {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-btn {
  width: 100%;

  border: none;
  background: transparent;

  padding: 12px 16px;
  border-radius: 12px;

  display: flex;
  align-items: center;
  gap: 12px;

  color: #64748b;
  font-size: 14px;
  font-weight: 600;

  cursor: pointer;
  transition: all 0.15s ease;
}

.menu-btn:hover {
  background: #f8fafc;
  color: #0f172a;
}

.menu-btn.active {
  background: #eef2ff;
  color: #4f46e5;
}

/* PROFILE */

.profile-section {
  padding: 16px;
  border-top: 1px solid #f1f5f9;
}

.profile-top{
  width:100%;
  display:flex;
  align-items:center;
  gap:12px;
}

.profile-card{
  display:flex;
  flex-direction:column;
  gap:12px;
}

.avatar{
  width:44px;
  height:44px;
  border-radius:12px;

  background:#EEF2FF;
  color:#4F46E5;

  display:flex;
  align-items:center;
  justify-content:center;

  font-weight:700;
  font-size:14px;

  flex-shrink:0;
}

.profile-info {
  flex: 1;
}

.username {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.role {
  font-size: 12px;
  color: #94a3b8;
}

.logout-btn {
  width: 100%;
  min-height:42px;

  border: none;
  border-radius: 10px;

  background: #fef2f2;
  color: #dc2626;

  padding: 10px;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  font-size: 13px;
  font-weight: 600;

  cursor: pointer;

  transition: all 0.15s ease;
}

.logout-btn:hover {
  background: #fee2e2;
}

/* =========================
   MAIN
========================= */

.main-content {
  flex: 1;
  margin-left: 256px;

  min-height: 100vh;

  display: flex;
  flex-direction: column;
}

/* HEADER */

.top-header {
  height: 64px;

  background: white;

  border-bottom: 1px solid #e2e8f0;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 0 32px;

  box-sizing: border-box;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.crumb {
  font-size: 13px;
  color: #94a3b8;
}

.crumb.current {
  color: #0f172a;
  font-weight: 700;
}

.link {
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
}

.link:hover {
  color: #4f46e5;
}

.divider {
  margin: 0 8px;
  color: #cbd5e1;
}

.header-right {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

/* CONTENT */

.content-wrapper {
  padding: 32px;
  flex: 1;
}

/* RESPONSIVE */

@media (max-width: 1024px) {
  .sidebar {
    width: 220px;
  }

  .main-content {
    margin-left: 220px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .main-content {
    margin-left: 0;
  }

  .top-header {
    padding: 0 16px;
  }

  .content-wrapper {
    padding: 16px;
  }
}

.clickable-profile{
  cursor:pointer;
  border-radius:14px;
  padding:10px;
  transition:.15s ease;
}

.clickable-profile:hover{
  background:#F8FAFC;
}
</style>