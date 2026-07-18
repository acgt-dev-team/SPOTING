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
      .setValue("Abc123!x")

    expect(
      inputs[0].element.value
    ).toBe("Abc123!x")

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
      .setValue("Abc123!x")

    expect(
      inputs[1].element.value
    ).toBe("Abc123!x")

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
      .setValue("Abc123!x")

    await inputs[1]
      .setValue("Xyz123!x")

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
  it("memaparkan ralat untuk password lemah", async () => {
    const wrapper = mount(ChangePassword)
    const inputs = wrapper.findAll("input")

    await inputs[0].setValue("weakpass")
    await inputs[1].setValue("weakpass")
    await wrapper.find("button").trigger("click")

    expect(wrapper.text()).toContain("aksara khas")
    expect(api.post).not.toHaveBeenCalled()
  })

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
      .setValue("Abc123!x")

    await inputs[1]
      .setValue("Abc123!x")

    const button =
      wrapper.find("button")

    await button.trigger("click")

    expect(api.post)
      .toHaveBeenCalledWith(
        "/auth/change-password",
        {
          password: "Abc123!x"
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
      .setValue("Abc123!x")

    await inputs[1]
      .setValue("Abc123!x")

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
      .setValue("Abc123!x")

    await inputs[1]
      .setValue("Abc123!x")

    const button =
      wrapper.find("button")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain(
        "Gagal menukar kata laluan"
      )

  })

})
