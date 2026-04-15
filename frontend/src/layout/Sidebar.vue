<script setup>
import { useRouter, useRoute } from "vue-router"
import logo from "../assets/images/spoting-logo.png"

import {
  LayoutDashboard,
  Users,
  ClipboardList,
  Settings,
  UserCircle2,
  LogOut
} from "lucide-vue-next"

const router = useRouter()
const route = useRoute()

function logout() {
  localStorage.removeItem("token")
  localStorage.removeItem("role")
  router.push("/login")
}

const menus = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/app/dashboard"
  },
  {
    label: "Pelanggan",
    icon: Users,
    path: "/app/pelanggan"
  },
  {
    label: "Profil",
    icon: UserCircle2,
    path: "/app/profil"
  },
  {
    label: "Tugasan",
    icon: ClipboardList,
    path: "/app/tugasan"
  },
  {
    label: "Tetapan",
    icon: Settings,
    path: "/app/tetapan"
  }
]
</script>

<template>
  <aside class="sidebar">
    <div>
      <div class="logo-wrap">
        <img :src="logo" alt="Spoting Logo" class="logo" />
      </div>

      <div class="section-label">MENU UTAMA</div>

      <nav class="nav">
        <div
          v-for="item in menus"
          :key="item.path"
          class="nav-item"
          :class="{ active: route.path === item.path }"
          @click="router.push(item.path)"
        >
          <component :is="item.icon" size="18" />
          <span>{{ item.label }}</span>
        </div>
      </nav>
    </div>

    <div class="profile-card">
      <div class="profile-top">
        <div class="avatar">T</div>
        <div>
          <div class="username">Test User</div>
          <div class="role">Pengguna Sistem</div>
        </div>
      </div>

      <button class="logout-btn" @click="logout">
        <LogOut size="16" />
        <span>Log keluar</span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  min-height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 24px 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}

.logo-wrap {
  margin-bottom: 28px;
}

.logo {
  width: 128px;
}

.section-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #9ca3af;
  margin-bottom: 12px;
  padding: 0 10px;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  cursor: pointer;
  color: #374151;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: #f3f4f6;
}

.nav-item.active {
  background: #eef4ff;
  color: #1d4ed8;
}

.profile-card {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 16px;
}

.profile-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
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
  color: #111827;
}

.role {
  font-size: 12px;
  color: #6b7280;
}

.logout-btn {
  width: 100%;
  border: none;
  background: white;
  border: 1px solid #e5e7eb;
  color: #dc2626;
  border-radius: 12px;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s ease;
}

.logout-btn:hover {
  background: #fef2f2;
}
</style>