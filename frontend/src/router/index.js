import { createRouter, createWebHistory } from "vue-router"

// Auth (single entry)
import Auth from "../views/auth/Auth.vue"

// Layout
import MainLayout from "../components/layout/MainLayout.vue"

// Pages
import Dashboard from "../views/dashboard/Dashboard.vue"
import Organisasi from "../views/organisasi/Organisasi.vue"
import Tapak from "../views/tapak/Tapak.vue"
import Profil from "../views/profil/Profil.vue"
import Tugasan from "../views/tugasan/Tugasan.vue"
import Tetapan from "../views/tetapan/Tetapan.vue"
import Pelanggan from "../views/pelanggan/Pelanggan.vue"

// Wizard
import Wizard from "../views/wizard/Wizard.vue"

const routes = [

  // Default → Wizard
  {
    path: "/",
    redirect: "/wizard"
  },

  // AUTH (single page controller)
  {
    path: "/login",
    component: Auth
  },

  // Wizard setup
  {
    path: "/wizard",
    component: Wizard
  },

  // MAIN SYSTEM (with sidebar)
  {
    path: "/app",   // ✅ IMPORTANT CHANGE (avoid path conflict)
    component: MainLayout,
    children: [
      {
        path: "dashboard",
        component: Dashboard
      },
      {
        path: "pelanggan",
        component: Pelanggan
      },
      {
        path: "organisasi",
        component: Organisasi
      },
      {
        path: "tapak",
        component: Tapak
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