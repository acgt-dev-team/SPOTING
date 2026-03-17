import { createRouter, createWebHistory } from "vue-router"

// Auth pages
import Login from "../views/auth/Login.vue"
import ForgotPassword from "../views/auth/ForgotPassword.vue"

// Layout
import MainLayout from "../components/layout/MainLayout.vue"

// Existing pages
import Dashboard from "../views/dashboard/Dashboard.vue"
import Organisasi from "../views/organisasi/Organisasi.vue"
import Tapak from "../views/tapak/Tapak.vue"
import Profil from "../views/profil/Profil.vue"
import Tugasan from "../views/tugasan/Tugasan.vue"
import Tetapan from "../views/tetapan/Tetapan.vue"
import Pelanggan from "../views/pelanggan/Pelanggan.vue"

// Wizard page
import Wizard from "../views/wizard/Wizard.vue"

const routes = [

  {
    path: "/",
    redirect: "/wizard"
  },

  // AUTH
  {
    path: "/login",
    component: Login
  },
  {
    path: "/forgot-password",
    component: ForgotPassword
  },

  // Wizard setup
  {
    path: "/wizard",
    component: Wizard
  },

  // MAIN SYSTEM (with sidebar layout)
  {
    path: "/",
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