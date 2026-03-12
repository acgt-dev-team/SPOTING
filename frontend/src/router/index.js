import { createRouter, createWebHistory } from "vue-router"

import MainLayout from "@/components/layout/MainLayout.vue"

import Dashboard from "@/views/dashboard/Dashboard.vue"

const routes = [

{
  path: "/",
  component: MainLayout,

  children: [
    {
      path: "",
      component: Dashboard
    }
  ]

}

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router