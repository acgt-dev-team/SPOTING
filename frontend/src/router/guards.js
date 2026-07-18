export function setupGuards(router) {

  router.beforeEach((to, from, next) => {

    const token =
      sessionStorage.getItem("token")

    const role =
      sessionStorage.getItem("role")

    const forcePasswordChange =
      sessionStorage.getItem(
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

    if (to.path === "/change-password" && !token) {
      return next("/login")
    }

    // =========================
    // FORCE CHANGE PASSWORD
    // =========================
    if (
      token &&
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
