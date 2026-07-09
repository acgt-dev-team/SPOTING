import { mount } from "@vue/test-utils"

import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import ChangePassword
from "../src/features/auth/ChangePassword.vue"

import api from "../src/services/api"

// =========================
// MOCK ROUTER
// =========================
const pushMock = vi.fn()

vi.mock("vue-router", () => ({
  useRouter: () => ({
    push: pushMock
  })
}))

// =========================
// MOCK API
// =========================
vi.mock("../src/services/api", () => ({
  default: {
    post: vi.fn()
  }
}))

describe("ChangePassword.vue", () => {

  beforeEach(() => {

    vi.clearAllMocks()

    sessionStorage.clear()

    sessionStorage.setItem(
      "username",
      "admin"
    )

  })

  // =========================
  // RENDER PAGE
  // =========================
  it("memaparkan halaman tukar password", () => {

    const wrapper =
      mount(ChangePassword)

    expect(wrapper.text())
      .toContain(
        "Tukar Kata Laluan"
      )

  })

  // =========================
  // INPUT PASSWORD
  // =========================
  it("menerima input password", async () => {

    const wrapper =
      mount(ChangePassword)

    const inputs =
      wrapper.findAll("input")

    await inputs[0]
      .setValue("abc123")

    expect(
      inputs[0].element.value
    ).toBe("abc123")

  })

  // =========================
  // INPUT CONFIRM PASSWORD
  // =========================
  it("menerima input sahkan password", async () => {

    const wrapper =
      mount(ChangePassword)

    const inputs =
      wrapper.findAll("input")

    await inputs[1]
      .setValue("abc123")

    expect(
      inputs[1].element.value
    ).toBe("abc123")

  })

  // =========================
  // EMPTY VALIDATION
  // =========================
  it("memaparkan ralat jika kosong", async () => {

    const wrapper =
      mount(ChangePassword)

    const button =
      wrapper.find("button")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain(
        "Sila isi semua maklumat"
      )

  })

  // =========================
  // PASSWORD MISMATCH
  // =========================
  it("memaparkan ralat jika password tidak sama", async () => {

    const wrapper =
      mount(ChangePassword)

    const inputs =
      wrapper.findAll("input")

    await inputs[0]
      .setValue("abc123")

    await inputs[1]
      .setValue("xyz123")

    const button =
      wrapper.find("button")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain(
        "Kata laluan tidak sama"
      )

  })

  // =========================
  // SUCCESS ADMIN
  // =========================
  it("redirect admin selepas berjaya", async () => {

    api.post.mockResolvedValue({})

    sessionStorage.setItem(
      "role",
      "admin"
    )

    sessionStorage.setItem(
      "forcePasswordChange",
      "true"
    )

    const wrapper =
      mount(ChangePassword)

    const inputs =
      wrapper.findAll("input")

    await inputs[0]
      .setValue("abc123")

    await inputs[1]
      .setValue("abc123")

    const button =
      wrapper.find("button")

    await button.trigger("click")

    expect(api.post)
      .toHaveBeenCalledWith(
        "/auth/change-password",
        {
          username: "admin",
          password: "abc123"
        }
      )

    expect(
      sessionStorage.getItem(
        "forcePasswordChange"
      )
    ).toBeNull()

    expect(pushMock)
      .toHaveBeenCalledWith(
        "/admin/configuration"
      )

  })

  // =========================
  // SUCCESS USER
  // =========================
  it("redirect user ke dashboard", async () => {

    api.post.mockResolvedValue({})

    sessionStorage.setItem(
      "role",
      "user"
    )

    const wrapper =
      mount(ChangePassword)

    const inputs =
      wrapper.findAll("input")

    await inputs[0]
      .setValue("abc123")

    await inputs[1]
      .setValue("abc123")

    const button =
      wrapper.find("button")

    await button.trigger("click")

    expect(pushMock)
      .toHaveBeenCalledWith(
        "/admin/dashboard"
      )

  })

  // =========================
  // API FAILURE
  // =========================
  it("memaparkan ralat jika gagal tukar password", async () => {

    // suppress expected console error
    vi.spyOn(console, "error")
      .mockImplementation(() => {})

    api.post.mockRejectedValue(
      new Error("API Error")
    )

    const wrapper =
      mount(ChangePassword)

    const inputs =
      wrapper.findAll("input")

    await inputs[0]
      .setValue("abc123")

    await inputs[1]
      .setValue("abc123")

    const button =
      wrapper.find("button")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain(
        "Gagal menukar kata laluan"
      )

  })

})
