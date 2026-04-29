export function setupGuards(router) {
  router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token")
    const role = localStorage.getItem("role")

    // Protected routes
    if (to.meta.requiresAuth && !token) {
      return next("/login")
    }

    // Prevent logged in users from going back to login
    if (to.path === "/login" && token) {
      if (
        role === "admin" ||
        role === "super admin"
      ) {
        return next("/admin/configuration")
      }

      if (role === "user") {
        return next("/admin/dashboard")
      }
    }

    // user cannot access account management
    if (
      role === "user" &&
      to.path.startsWith("/admin/accounts")
    ) {
      return next("/admin/dashboard")
    }

    next()
  })
}