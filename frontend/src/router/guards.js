export function setupGuards(router) {

  router.beforeEach((to, from, next) => {

    const token =
      localStorage.getItem("token")

    const role =
      localStorage.getItem("role")

    const forcePasswordChange =
      localStorage.getItem(
        "forcePasswordChange"
      )

    // =========================
    // PROTECTED ROUTES
    // =========================
    if (
      to.meta?.requiresAuth &&
      !token
    ) {
      return next("/login")
    }

    // =========================
    // FORCE CHANGE PASSWORD
    // =========================
    if (
      forcePasswordChange === "true" &&
      to.path !== "/change-password"
    ) {
      return next("/change-password")
    }

    // =========================
    // BLOCK LOGIN PAGE
    // =========================
    if (
      (
        to.path === "/login" ||
        to.path === "/change-password"
      ) &&
      token &&
      forcePasswordChange !== "true"
    ) {

      if (
        role === "admin" ||
        role === "super admin"
      ) {
        return next(
          "/admin/configuration"
        )
      }

      if (role === "user") {
        return next(
          "/admin/dashboard/"
        )
      }

    }

    // =========================
    // USER ACCESS RESTRICTION
    // =========================
    if (
      role === "user" &&
      to.path.startsWith(
        "/admin/accounts"
      )
    ) {
      return next(
        "/admin/dashboard/"
      )
    }

    // =========================
    // ALLOW ROUTE
    // =========================
    next()

  })

}