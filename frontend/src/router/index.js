import { createRouter, createWebHistory } from "vue-router"
import { setupGuards } from "../router/guards"

// =========================
// AUTH
// =========================
import Auth from "../features/auth/Auth.vue"

// =========================
// LAYOUTS
// =========================
import AdminLayout from "../layout/AdminLayout.vue"

// =========================
// ADMIN
// =========================
import OrganizationPage from "../features/configuration/OrganizationPage.vue"
import SubOrganisasi from "../features/configuration/SubOrganisasiPage.vue"
import Tapak from "../features/configuration/TapakPage.vue"
import ProfilList from "../features/configuration/ProfilListPage.vue"
import AdminTugasan from "../features/configuration/TugasanPage.vue"
import PengurusanAkaun from "../features/configuration/PengurusanAkaun.vue"
import DashboardContent from "../features/configuration/DashboardContent.vue"

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
    redirect: "/admin/dashboard", // ✅ default page
    children: [
      {
        path: "dashboard",
        component: DashboardContent // ✅ now using your new file
      },
      {
        path: "configuration",
        component: OrganizationPage
      },
      {
        path: "accounts",
        component: PengurusanAkaun
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