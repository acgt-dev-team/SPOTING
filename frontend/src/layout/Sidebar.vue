<script setup>
import { useRouter, useRoute } from "vue-router"
import logo from "../assets/images/spoting-logo.png"

import {
  LayoutDashboard,
  Users,
  ClipboardList,
  Settings
} from "lucide-vue-next"

const router = useRouter()
const route = useRoute()

// 🔐 Get role (for future use)
const role = localStorage.getItem("role")

function logout() {
  localStorage.removeItem("token")
  localStorage.removeItem("role")
  router.push("/login")
}
</script>

<template>

<div class="sidebar">

  <div class="logo">
    <img :src="logo" alt="Spoting Logo">
  </div>

  <nav class="nav">

    <div
      class="nav-item"
      :class="{ active: route.path === '/app/profil' }"
      @click="router.push('/app/profil')"
    >
      <LayoutDashboard size="18"/>
      <span>Profil</span>
    </div>

    <div
      class="nav-item"
      :class="{ active: route.path === '/app/pelanggan' }"
      @click="router.push('/app/pelanggan')"
    >
      <Users size="18"/>
      <span>Pelanggan</span>
    </div>

    <div
      class="nav-item"
      :class="{ active: route.path === '/app/tugasan' }"
      @click="router.push('/app/tugasan')"
    >
      <ClipboardList size="18"/>
      <span>Tugasan</span>
    </div>

    <div
      class="nav-item"
      :class="{ active: route.path === '/app/tetapan' }"
      @click="router.push('/app/tetapan')"
    >
      <Settings size="18"/>
      <span>Tetapan</span>
    </div>

  </nav>

  <div class="profile">

    <div class="avatar"></div>

    <div>
      <div class="username">Username</div>
      <div class="profile-link">Lihat profil</div>

      <div class="logout" @click="logout">
        Log keluar
      </div>
    </div>

  </div>

</div>

</template>

<style scoped>
.sidebar{
  width:240px;
  background:white;
  border-right:1px solid #e5e7eb;
  padding:20px 16px;
  display:flex;
  flex-direction:column;
  height:100vh;
  box-sizing:border-box;
}

.logo img{
  width:120px;
  margin-bottom:24px;
}

.nav{
  display:flex;
  flex-direction:column;
  gap:4px;
}

.nav-item{
  display:flex;
  align-items:center;
  gap:10px;
  padding:10px 12px;
  border-radius:8px;
  cursor:pointer;
  color:#374151;
  font-size:14px;
}

.nav-item:hover{
  background:#f3f4f6;
}

.nav-item.active{
  background:#f5f3ff;
  color:#7c3aed;
}

.profile{
  margin-top:auto;
  display:flex;
  align-items:center;
  gap:12px;
  padding-top:16px;
  border-top:1px solid #e5e7eb;
}

.avatar{
  width:36px;
  height:36px;
  border-radius:50%;
  background:#e5e7eb;
}

.username{
  font-size:14px;
  font-weight:600;
}

.profile-link{
  font-size:12px;
  color:#6b7280;
}

.logout{
  font-size:12px;
  color:#ef4444;
  cursor:pointer;
}
</style>