<script setup>
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import logo from "../../assets/images/spoting-logo.png"

const route = useRoute()
const router = useRouter()

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

  if (path.includes("/profil")) {
    crumbs.push({
      label: "Senarai Organisasi",
      to: "/admin/configuration"
    })

    crumbs.push({
      label: "Senarai Sub Organisasi",
      to: organizationId
        ? `/admin/configuration/sub-organisasi/${organizationId}`
        : null
    })

    crumbs.push({
      label: "Senarai Tapak",
      to:
        organizationId && subOrganizationId
          ? `/admin/configuration/sub-organisasi/${organizationId}/tapak/${subOrganizationId}`
          : null
    })

    crumbs.push({
      label: "Senarai Profil",
      to: null
    })
  } else if (path.includes("/tapak")) {
    crumbs.push({
      label: "Senarai Organisasi",
      to: "/admin/configuration"
    })

    crumbs.push({
      label: "Senarai Sub Organisasi",
      to: organizationId
        ? `/admin/configuration/sub-organisasi/${organizationId}`
        : null
    })

    crumbs.push({
      label: "Senarai Tapak",
      to: null
    })
  } else if (path.includes("/sub-organisasi")) {
    crumbs.push({
      label: "Senarai Organisasi",
      to: "/admin/configuration"
    })

    crumbs.push({
      label: "Senarai Sub Organisasi",
      to: null
    })
  } else if (path.includes("/tugasan")) {
    crumbs.push({
      label: "Senarai Organisasi",
      to: "/admin/configuration"
    })

    crumbs.push({
      label: "Tugasan",
      to: null
    })
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
</script>

<template>
  <div class="config-shell">
    <header class="admin-navbar">
      <div class="brand-wrap">
        <img :src="logo" alt="Spoting" class="brand-logo" />
        <div class="brand-meta">
          <p class="brand-sub">ADMIN PANEL</p>
        </div>
      </div>

      <button class="profile-btn" type="button" title="Profil Admin">
        <span class="profile-icon">👤</span>
      </button>
    </header>

    <div class="config-container">
      <div class="page-top-header">
        <div class="page-top-left">
          <div class="breadcrumbs">
            <template v-for="(item, index) in breadcrumbs" :key="index">
              <button
                v-if="item.to && index !== breadcrumbs.length - 1"
                type="button"
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

              <span v-if="index !== breadcrumbs.length - 1" class="divider">›</span>
            </template>
          </div>
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
.config-shell {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(2, 2, 101, 0.08), transparent 22%),
    radial-gradient(circle at top right, rgba(11, 11, 143, 0.05), transparent 20%),
    #f5f7fb;
}

.admin-navbar {
  height: 84px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid #eceff5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 36px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.05);
  position: sticky;
  top: 0;
  z-index: 50;
}

.brand-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-logo {
  height: 46px;
  width: auto;
  object-fit: contain;
  display: block;
}

.brand-meta {
  display: flex;
  align-items: center;
}

.brand-sub {
  font-size: 12px;
  font-weight: 800;
  color: #020265;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  line-height: 1;
  margin: 0;
}

.profile-btn {
  width: 52px;
  height: 52px;
  border-radius: 18px;
  border: 1px solid #dbe3ff;
  background: linear-gradient(180deg, #ffffff, #f4f6ff);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
  transition: 0.18s ease;
}

.profile-btn:hover {
  transform: translateY(-1px);
  border-color: #c7d2fe;
  background: #eef1ff;
}

.profile-icon {
  font-size: 22px;
}

.config-container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 28px 36px 40px;
}

.page-top-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.page-top-left {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  flex-wrap: wrap;
  min-width: 0;
}

.crumb {
  color: #6b7280;
  font-weight: 700;
  white-space: nowrap;
}

.crumb.current {
  color: #111827;
  font-weight: 800;
}

.link {
  text-decoration: none;
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: 0.18s ease;
}

.link:hover {
  color: #020265;
}

.divider {
  color: #9ca3af;
  font-weight: 700;
}

.customer-block {
  margin-left: auto;
  text-align: right;
}

.customer-caption {
  font-size: 12px;
  font-weight: 800;
  color: #020265;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 6px;
}

.customer-name {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.1;
  color: #111827;
  white-space: nowrap;
  margin: 0;
}

@media (max-width: 768px) {
  .admin-navbar {
    padding: 0 20px;
    height: 76px;
  }

  .brand-wrap {
    gap: 10px;
  }

  .brand-logo {
    height: 38px;
  }

  .brand-sub {
    font-size: 11px;
  }

  .profile-btn {
    width: 46px;
    height: 46px;
    border-radius: 16px;
  }

  .config-container {
    padding: 22px 20px 32px;
  }

  .page-top-header {
    flex-direction: column;
  }

  .customer-block {
    margin-left: 0;
    text-align: left;
  }

  .customer-name {
    font-size: 22px;
    white-space: normal;
  }

  .breadcrumbs {
    font-size: 14px;
  }
}
</style>