import { createRouter, createWebHistory } from "vue-router"
import { setupGuards } from "../router/guards"

// =========================
// AUTH
// =========================
import Auth from "../features/auth/Auth.vue"

// =========================
// LAYOUTS
// =========================
import MainLayout from "../layout/MainLayout.vue"
import AdminLayout from "../layout/AdminLayout.vue"

// =========================
// ADMIN
// =========================
import OrganizationPage from "../features/configuration/OrganizationPage.vue"
import SubOrganisasi from "../features/configuration/SubOrganisasiPage.vue"
import Tapak from "../features/configuration/TapakPage.vue"
import ProfilList from "../features/configuration/ProfilListPage.vue"
import AdminTugasan from "../features/configuration/TugasanPage.vue"

// =========================
// USER
// =========================
import Profil from "../features/profil/Profil.vue"
import Tugasan from "../features/tugasan/Tugasan.vue"
import Tetapan from "../features/tetapan/Tetapan.vue"
import Pelanggan from "../features/pelanggan/Pelanggan.vue"

// =========================
// DASHBOARD
// =========================
import Dashboard from "../features/dashboard/Dashboard.vue"

// =========================
// ROUTES
// =========================
const routes = [
  {
    path: "/",
    redirect: "/login"
  },

  {
    path: "/login",
    component: Auth
  },

  // =========================
  // ADMIN (WITH LAYOUT)
  // =========================
  {
    path: "/admin",
    component: AdminLayout,
    meta: { requiresAuth: true, role: "admin" },
    children: [
      {
        path: "configuration",
        component: OrganizationPage
      },
      {
        path: "configuration/sub-organisasi/:organizationId",
        component: SubOrganisasi
      },
      {
        path: "configuration/sub-organisasi/:organizationId/tapak/:subOrganizationId",
        component: Tapak
      },
      {
        path: "configuration/sub-organisasi/:organizationId/tapak/:subOrganizationId/profil/:siteId",
        component: ProfilList
      },
      {
        path: "configuration/sub-organisasi/:organizationId/tapak/:subOrganizationId/profil/:siteId/tugasan/:profileId",
        component: AdminTugasan
      }
    ]
  },

  // =========================
  // USER APP
  // =========================
  {
    path: "/app",
    component: MainLayout,
    meta: { requiresAuth: true, role: "user" },
    children: [
      {
        path: "",
        redirect: "profil"
      },
      {
        path: "dashboard",
        component: Dashboard
      },
      {
        path: "pelanggan",
        component: Pelanggan
      },
      {
        path: "profil",
        component: Profil
      },
      {
        path: "tugasan",
        component: Tugasan
      },
      {
        path: "tetapan",
        component: Tetapan
      }
    ]
  }
]

// =========================
// ROUTER INIT
// =========================
const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ Apply guards
setupGuards(router)

export default router