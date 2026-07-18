import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import { setupGuards }
from "../src/router/guards"

// =========================
// MOCK ROUTER
// =========================
function createMockRouter() {

  return {
    beforeEach: vi.fn()
  }

}

describe("router guards", () => {

  let router
  let guard

  beforeEach(() => {

    sessionStorage.clear()

    router = createMockRouter()

    setupGuards(router)

    // capture registered guard
    guard =
      router.beforeEach.mock.calls[0][0]

  })

  // =========================
  // REDIRECT IF NO TOKEN
  // =========================
  it("redirect ke login jika tiada token", () => {

    const next = vi.fn()

    guard(
      {
        meta: {
          requiresAuth: true
        },
        path: "/admin/configuration"
      },
      {},
      next
    )

    expect(next)
      .toHaveBeenCalledWith("/login")

  })

  it("redirect change password ke login jika tiada token", () => {
    const next = vi.fn()

    guard(
      { path: "/change-password" },
      {},
      next
    )

    expect(next).toHaveBeenCalledWith("/login")
  })

  // =========================
  // FORCE PASSWORD CHANGE
  // =========================
  it("redirect ke tukar kata laluan jika dipaksa", () => {

    sessionStorage.setItem("token", "abc")
    sessionStorage.setItem(
      "forcePasswordChange",
      "true"
    )

    const next = vi.fn()

    guard(
      {
        path: "/admin/configuration",
        meta: {
          requiresAuth: true
        }
      },
      {},
      next
    )

    expect(next)
      .toHaveBeenCalledWith(
        "/change-password"
      )

  })

  // =========================
  // ADMIN BLOCK LOGIN PAGE
  // =========================
  it("admin tidak boleh kembali ke login", () => {

    sessionStorage.setItem("token", "abc")
    sessionStorage.setItem("role", "admin")

    const next = vi.fn()

    guard(
      {
        path: "/login"
      },
      {},
      next
    )

    expect(next)
      .toHaveBeenCalledWith(
        "/admin/configuration"
      )

  })

  // =========================
  // SUPER ADMIN BLOCK LOGIN
  // =========================
  it("super admin redirect ke configuration", () => {

    sessionStorage.setItem("token", "abc")
    sessionStorage.setItem(
      "role",
      "super admin"
    )

    const next = vi.fn()

    guard(
      {
        path: "/login"
      },
      {},
      next
    )

    expect(next)
      .toHaveBeenCalledWith(
        "/admin/configuration"
      )

  })

  // =========================
  // USER BLOCK LOGIN
  // =========================
  it("user redirect ke dashboard", () => {

    sessionStorage.setItem("token", "abc")
    sessionStorage.setItem("role", "user")

    const next = vi.fn()

    guard(
      {
        path: "/login"
      },
      {},
      next
    )

    expect(next)
      .toHaveBeenCalledWith(
        "/admin/dashboard/"
      )

  })

  // =========================
  // USER CANNOT ACCESS ACCOUNT PAGE
  // =========================
  it("user tidak boleh akses accounts", () => {

    sessionStorage.setItem("token", "abc")
    sessionStorage.setItem("role", "user")

    const next = vi.fn()

    guard(
      {
        path: "/admin/accounts"
      },
      {},
      next
    )

    expect(next)
      .toHaveBeenCalledWith(
        "/admin/dashboard/"
      )

  })

  // =========================
  // ALLOW NORMAL ROUTE
  // =========================
  it("membenarkan akses biasa", () => {

    sessionStorage.setItem("token", "abc")
    sessionStorage.setItem("role", "admin")

    const next = vi.fn()

    guard(
      {
        path: "/admin/configuration",
        meta: {
          requiresAuth: true
        }
      },
      {},
      next
    )

    expect(next)
      .toHaveBeenCalledWith()

  })

  // =========================
  // CHANGE PASSWORD PAGE ALLOWED
  // =========================
  it("membenarkan akses ke change password", () => {

    sessionStorage.setItem("token", "abc")
    sessionStorage.setItem(
      "forcePasswordChange",
      "true"
    )

    const next = vi.fn()

    guard(
      {
        path: "/change-password"
      },
      {},
      next
    )

    expect(next)
      .toHaveBeenCalledWith()

  })

})
