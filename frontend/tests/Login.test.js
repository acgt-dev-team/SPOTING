import { mount } from "@vue/test-utils"
import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import Auth from "../src/features/auth/Auth.vue"
import router from "../src/router"

import api from "../src/services/api"

// =========================
// MOCK API
// =========================
vi.mock("../src/services/api", () => ({
  default: {
    post: vi.fn()
  }
}))

// =========================
// HIDE CONSOLE ERROR
// =========================
vi.spyOn(console, "error")
  .mockImplementation(() => {})

describe("Auth.vue", () => {

  beforeEach(async () => {

    localStorage.clear()

    router.push("/login")

    await router.isReady()

  })

  // =========================
  // RENDER
  // =========================
  it("memaparkan halaman log masuk", () => {

    const wrapper = mount(Auth, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.text())
      .toContain("Log masuk")

  })

  // =========================
  // USERNAME INPUT
  // =========================
  it("menerima input nama pengguna", async () => {

    const wrapper = mount(Auth, {
      global: {
        plugins: [router]
      }
    })

    const input =
      wrapper.find('input[type="text"]')

    await input.setValue("admin")

    expect(input.element.value)
      .toBe("admin")

  })

  // =========================
  // PASSWORD INPUT
  // =========================
  it("menerima input kata laluan", async () => {

    const wrapper = mount(Auth, {
      global: {
        plugins: [router]
      }
    })

    const inputs = wrapper.findAll("input")

    await inputs[1]
      .setValue("password123")

    expect(inputs[1].element.value)
      .toBe("password123")

  })

  // =========================
  // EMPTY VALIDATION
  // =========================
  it("memaparkan ralat jika maklumat kosong", async () => {

    const wrapper = mount(Auth, {
      global: {
        plugins: [router]
      }
    })

    const button = wrapper.find("button")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain("Sila isi semua maklumat")

  })

  // =========================
  // FAILED LOGIN
  // =========================
  it("memaparkan ralat login apabila gagal", async () => {

    api.post.mockRejectedValue({
      response: {
        status: 401
      }
    })

    const wrapper = mount(Auth, {
      global: {
        plugins: [router]
      }
    })

    const inputs = wrapper.findAll("input")

    await inputs[0]
      .setValue("admin")

    await inputs[1]
      .setValue("wrongpassword")

    const button = wrapper.find("button")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain(
        "Nama pengguna atau kata laluan tidak sah"
      )

  })

  // =========================
  // SUCCESS LOGIN
  // =========================
  it("login berjaya dan redirect ke configuration", async () => {

    api.post.mockResolvedValue({
      data: {
        access_token: "fake-token",
        role: "admin",
        force_password_change: false
      }
    })

    const pushSpy =
      vi.spyOn(router, "push")

    const wrapper = mount(Auth, {
      global: {
        plugins: [router]
      }
    })

    const inputs = wrapper.findAll("input")

    await inputs[0]
      .setValue("admin")

    await inputs[1]
      .setValue("password123")

    const button = wrapper.find("button")

    await button.trigger("click")

    expect(
      localStorage.getItem("token")
    ).toBe("fake-token")

    expect(pushSpy)
      .toHaveBeenCalledWith(
        "/admin/configuration"
      )

  })

  // =========================
  // FORCE PASSWORD CHANGE
  // =========================
  it("redirect ke tukar kata laluan jika dipaksa", async () => {

    api.post.mockResolvedValue({
      data: {
        access_token: "fake-token",
        role: "admin",
        force_password_change: true
      }
    })

    const pushSpy =
      vi.spyOn(router, "push")

    const wrapper = mount(Auth, {
      global: {
        plugins: [router]
      }
    })

    const inputs = wrapper.findAll("input")

    await inputs[0]
      .setValue("admin")

    await inputs[1]
      .setValue("password123")

    const button = wrapper.find("button")

    await button.trigger("click")

    expect(pushSpy)
      .toHaveBeenCalledWith(
        "/change-password"
      )

  })

})