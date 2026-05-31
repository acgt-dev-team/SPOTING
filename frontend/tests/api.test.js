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
  href: ""
}

describe("api interceptor", () => {

  beforeEach(() => {

    localStorage.clear()

    vi.clearAllMocks()

    window.location.href = ""

  })

  // =========================
  // REQUEST TOKEN INJECTION
  // =========================
  it("menambah bearer token pada request", async () => {

    localStorage.setItem(
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

    localStorage.setItem(
      "token",
      "abc"
    )

    localStorage.setItem(
      "role",
      "admin"
    )

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
      localStorage.getItem("token")
    ).toBeNull()

    expect(
      localStorage.getItem("role")
    ).toBeNull()

    expect(window.location.href)
      .toBe("/login")

  })

  // =========================
  // NON 401 SHOULD NOT LOGOUT
  // =========================
  it("tidak logout untuk error selain 401", async () => {

    localStorage.setItem(
      "token",
      "abc"
    )

    localStorage.setItem(
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
      localStorage.getItem("token")
    ).toBe("abc")

    expect(
      localStorage.getItem("role")
    ).toBe("admin")

    expect(window.location.href)
      .toBe("")

  })

})