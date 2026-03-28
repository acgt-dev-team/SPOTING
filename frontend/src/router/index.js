import { createRouter, createWebHistory } from "vue-router"

// Auth
import Auth from "../views/auth/Auth.vue"

// User Layout (USER SIDE ONLY)
import MainLayout from "../components/layout/MainLayout.vue"

// Admin Configuration Views
import Configuration from "../views/configuration/Configuration.vue"
import SubOrganisasi from "../views/configuration/SubOrganisasi.vue"
import Tapak from "../views/configuration/Tapak.vue"
import ProfilList from "../views/configuration/ProfilList.vue"
import AdminTugasan from "../views/configuration/AdminTugasan.vue"

// User Pages
import Profil from "../views/profil/Profil.vue"
import Tugasan from "../views/tugasan/Tugasan.vue"
import Tetapan from "../views/tetapan/Tetapan.vue"
import Pelanggan from "../views/pelanggan/Pelanggan.vue"

const routes = [
  {
    path: "/",
    redirect: "/admin/configuration"
  },

  {
    path: "/login",
    component: Auth
  },

  // =========================
  // ADMIN CONFIGURATION FLOW
  // =========================
  {
    path: "/admin/configuration",
    component: Configuration
  },
  {
    path: "/admin/configuration/sub-organisasi/:organizationId",
    component: SubOrganisasi
  },
  {
    path: "/admin/configuration/sub-organisasi/:organizationId/tapak/:subOrganizationId",
    component: Tapak
  },
  {
    path: "/admin/configuration/sub-organisasi/:organizationId/tapak/:subOrganizationId/profil/:siteId",
    component: ProfilList
  },
  {
    path: "/admin/configuration/sub-organisasi/:organizationId/tapak/:subOrganizationId/profil/:siteId/tugasan/:profileId",
    component: AdminTugasan
  },

  // =========================
  // USER SIDE ONLY
  // =========================
  {
    path: "/app",
    component: MainLayout,
    children: [
      {
        path: "",
        redirect: "/app/profil"
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

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router