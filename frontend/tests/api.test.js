import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import api from "../src/services/api"

// =========================
// MOCK WINDOW LOCATION
// =========================
delete window.location

window.location = {
  href: "",
  hash: ""
}

describe("api interceptor", () => {

  beforeEach(() => {

    sessionStorage.clear()

    vi.clearAllMocks()

    window.location.href = ""
    window.location.hash = ""

  })

  // =========================
  // REQUEST TOKEN INJECTION
  // =========================
  it("menambah bearer token pada request", async () => {

    sessionStorage.setItem(
      "token",
      "abc123"
    )

    const interceptor =
      api.interceptors.request.handlers[0]
        .fulfilled

    const config = {
      headers: {}
    }

    const result =
      await interceptor(config)

    expect(
      result.headers.Authorization
    ).toBe("Bearer abc123")

  })

  // =========================
  // REQUEST WITHOUT TOKEN
  // =========================
  it("tidak menambah authorization jika tiada token", async () => {

    const interceptor =
      api.interceptors.request.handlers[0]
        .fulfilled

    const config = {
      headers: {}
    }

    const result =
      await interceptor(config)

    expect(
      result.headers.Authorization
    ).toBeUndefined()

  })

  // =========================
  // RESPONSE SUCCESS
  // =========================
  it("memulangkan response berjaya", async () => {

    const interceptor =
      api.interceptors.response.handlers[0]
        .fulfilled

    const response = {
      data: {
        success: true
      }
    }

    const result =
      interceptor(response)

    expect(result)
      .toEqual(response)

  })

  // =========================
  // AUTO LOGOUT 401
  // =========================
  it("logout automatik apabila 401", async () => {

    sessionStorage.setItem(
      "token",
      "abc"
    )

    sessionStorage.setItem(
      "role",
      "admin"
    )
    sessionStorage.setItem("username", "admin.user1")
    sessionStorage.setItem("forcePasswordChange", "false")
    localStorage.setItem("token", "legacy-token")

    const warnSpy =
      vi.spyOn(console, "warn")
        .mockImplementation(() => {})

    const interceptor =
      api.interceptors.response.handlers[0]
        .rejected

    const error = {
      response: {
        status: 401
      }
    }

    await expect(
      interceptor(error)
    ).rejects.toEqual(error)

    expect(warnSpy)
      .toHaveBeenCalled()

    expect(
      sessionStorage.getItem("token")
    ).toBeNull()

    expect(
      sessionStorage.getItem("role")
    ).toBeNull()

    expect(sessionStorage.getItem("username")).toBeNull()
    expect(sessionStorage.getItem("forcePasswordChange")).toBeNull()
    expect(localStorage.getItem("token")).toBeNull()

    expect(window.location.hash)
      .toBe("#/login")

  })

  // =========================
  // NON 401 SHOULD NOT LOGOUT
  // =========================
  it("redirect ke tukar kata laluan apabila backend memulangkan 428", async () => {
    sessionStorage.setItem("token", "abc")

    const interceptor = api.interceptors.response.handlers[0].rejected
    const error = { response: { status: 428 } }

    await expect(interceptor(error)).rejects.toEqual(error)
    expect(sessionStorage.getItem("forcePasswordChange")).toBe("true")
    expect(window.location.hash).toBe("#/change-password")
  })

  it("tidak logout untuk error selain 401", async () => {

    sessionStorage.setItem(
      "token",
      "abc"
    )

    sessionStorage.setItem(
      "role",
      "admin"
    )

    const interceptor =
      api.interceptors.response.handlers[0]
        .rejected

    const error = {
      response: {
        status: 500
      }
    }

    await expect(
      interceptor(error)
    ).rejects.toEqual(error)

    expect(
      sessionStorage.getItem("token")
    ).toBe("abc")

    expect(
      sessionStorage.getItem("role")
    ).toBe("admin")

    expect(window.location.href)
      .toBe("")

  })

})
