import { createRouter, createWebHistory } from "vue-router"

// Auth pages
import Login from "../views/auth/Login.vue"
import Register from "../views/auth/Register.vue"

// Existing pages
import Dashboard from "../views/dashboard/Dashboard.vue"
import Organisasi from "../views/organisasi/Organisasi.vue"
import Tapak from "../views/tapak/Tapak.vue"
import Profil from "../views/profil/Profil.vue"
import Tugasan from "../views/tugasan/Tugasan.vue"
import Tetapan from "../views/tetapan/Tetapan.vue"
import Pengguna from "../views/pelanggan/Pelanggan.vue"

// Wizard page
import Wizard from "../views/wizard/Wizard.vue"

const routes = [

  // redirect root → login
  {
    path: "/",
    redirect: "/wizard"
  },

  // LOGIN PAGE
  {
    path: "/login",
    component: Login
  },

  // REGISTER PAGE
  {
    path: "/register",
    component: Register
  },

  // wizard setup page
  {
    path: "/wizard",
    component: Wizard
  },

  // existing pages
  {
    path: "/dashboard",
    component: Dashboard
  },
  {
    path: "/organisasi",
    component: Organisasi
  },
  {
    path: "/tapak",
    component: Tapak
  },
  {
    path: "/profil",
    component: Profil
  },
  {
    path: "/tugasan",
    component: Tugasan
  },
  {
    path: "/tetapan",
    component: Tetapan
  },
  {
    path: "/pengguna",
    component: Pengguna
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router