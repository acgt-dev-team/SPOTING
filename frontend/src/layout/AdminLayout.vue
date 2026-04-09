<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from "vue"
import { useRoute, useRouter } from "vue-router"
import logo from "../assets/images/spoting-logo.png"

const route = useRoute()
const router = useRouter()

const showDropdown = ref(false)
const dropdownRef = ref(null)

const customerName = computed(() => "Kementerian Dalam Negeri")

const breadcrumbs = computed(() => {
  const path = route.path
  const organizationId = route.params.organizationId
  const subOrganizationId = route.params.subOrganizationId

  const crumbs = [
    {
      label: customerName.value,
      to: "/admin/configuration"
    }
  ]

  if (path.includes("/profil")) {
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
  } else if (path.includes("/tugasan")) {
    crumbs.push(
      { label: "Senarai Organisasi", to: "/admin/configuration" },
      { label: "Tugasan", to: null }
    )
  } else {
    crumbs.push({ label: "Senarai Organisasi", to: null })
  }

  return crumbs
})

function goTo(crumb, index) {
  if (!crumb.to || index === breadcrumbs.value.length - 1) return
  router.push(crumb.to)
}

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

function logout() {
  localStorage.removeItem("token")
  localStorage.removeItem("role")
  router.push("/login")
}

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside)
})
</script>

<template>
  <div class="admin-shell">
    <!-- 🔹 NAVBAR -->
    <header class="admin-navbar">
      <div class="brand-wrap">
        <img :src="logo" alt="Spoting" class="brand-logo" />
        <p class="brand-sub">ADMIN PANEL</p>
      </div>

      <!-- 🔥 PROFILE + DROPDOWN -->
      <div class="profile-wrapper" ref="dropdownRef">
        <button class="profile-btn" @click="toggleDropdown">
          👤
        </button>

        <div v-if="showDropdown" class="dropdown-menu">
          <button class="dropdown-item" @click="logout">
            🚪 Logout
          </button>
        </div>
      </div>
    </header>

    <!-- 🔹 CONTENT -->
    <div class="admin-container">
      <div class="page-top-header">
        <div class="breadcrumbs">
          <template v-for="(item, index) in breadcrumbs" :key="index">
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

            <span v-if="index !== breadcrumbs.length - 1">›</span>
          </template>
        </div>

        <div class="customer-block">
          <p class="customer-caption">Pelanggan</p>
          <h2 class="customer-name">{{ customerName }}</h2>
        </div>
      </div>

      <slot />
    </div>
  </div>
</template>

<style scoped>
.admin-shell {
  min-height: 100vh;
  background: #f5f7fb;
}

.admin-navbar {
  height: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 32px;
  background: white;
  border-bottom: 1px solid #eee;
}

.brand-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  height: 40px;
}

.brand-sub {
  font-weight: bold;
  color: #020265;
}

.profile-wrapper {
  position: relative;
}

.profile-btn {
  width: 45px;
  height: 45px;
  border-radius: 12px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 55px;
  background: white;
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 8px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.08);
}

.dropdown-item {
  background: none;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.admin-container {
  padding: 24px 32px;
}

.breadcrumbs {
  display: flex;
  gap: 8px;
}

.crumb {
  font-weight: 600;
}

.link {
  cursor: pointer;
  background: none;
  border: none;
}

.customer-block {
  margin-left: auto;
  text-align: right;
}
</style>