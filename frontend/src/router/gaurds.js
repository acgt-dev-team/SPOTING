export function setupGuards(router) {
  router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token")
    const role = localStorage.getItem("role")

    // 🔐 If route requires auth
    if (to.meta.requiresAuth) {
      if (!token) {
        return next("/login")
      }

      // 🚫 Role mismatch
      if (to.meta.role && to.meta.role !== role) {
        if (role === "admin") {
          return next("/admin/configuration")
        } else {
          return next("/app/profil")
        }
      }
    }

    // 🚫 Prevent logged-in user going back to login
    if (to.path === "/login" && token) {
      if (role === "admin") {
        return next("/admin/configuration")
      } else {
        return next("/app/profil")
      }
    }

    next()
  })
}