import { mount } from "@vue/test-utils"

import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import DashboardContent
from "../src/features/configuration/DashboardContent.vue"

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
    get: vi.fn()
  }
}))

describe("DashboardContent.vue", () => {

  beforeEach(() => {

    vi.clearAllMocks()

    api.get.mockImplementation((url) => {

      if (url === "/dashboard/full") {

        return Promise.resolve({
          data: {
            stats: {
            organisasi: 5,
            sub_organisasi: 8,
            tapak: 12,
            profil: 20,
            tugasan: 50
            },
            organizations: [
              {
                bil: 1,
                nama: "Kementerian A",
                done: 90,
                total: 100
              },
              {
                bil: 2,
                nama: "Kementerian B",
                done: 50,
                total: 100
              },
              {
                bil: 3,
                nama: "Kementerian C",
                done: 75,
                total: 100
              }
            ],
            profile_health: {
              counts: {},
              profiles: [],
              failed_profiles: [],
              scheduled_profiles: [],
              recent_profiles: []
            }
          }
        })

      }

      return Promise.resolve({
        data: {}
      })

    })

  })

  // =========================
  // RENDER PAGE
  // =========================
  it("memaparkan halaman dashboard", async () => {

    const wrapper =
      mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()
    await wrapper.vm.$nextTick()

    expect(wrapper.text())
      .toContain("Ringkasan Prestasi")

  })

  // =========================
  // FETCH DASHBOARD STATS
  // =========================
  it("mengambil data dashboard", async () => {

    mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()

    expect(api.get)
      .toHaveBeenCalledWith(
        "/dashboard/full"
      )

  })

  // =========================
  // FETCH ORGANIZATIONS
  // =========================
  it("mengambil organisasi dashboard", async () => {

    mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()

    expect(api.get)
      .toHaveBeenCalledWith(
        "/dashboard/full"
      )

  })

  // =========================
  // DISPLAY STATS
  // =========================
  it("memaparkan statistik dashboard", async () => {

    const wrapper =
      mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()
    await wrapper.vm.$nextTick()

    expect(wrapper.text())
      .toContain("5")

    expect(wrapper.text())
      .toContain("8")

    expect(wrapper.text())
      .toContain("12")

    expect(wrapper.text())
      .toContain("20")

    expect(wrapper.text())
      .toContain("50")

  })

  // =========================
  // DISPLAY ORGANIZATIONS
  // =========================
  it("memaparkan organisasi", async () => {

    const wrapper =
      mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()
    await wrapper.vm.$nextTick()

    expect(wrapper.text())
      .toContain("Kementerian A")

    expect(wrapper.text())
      .toContain("Kementerian B")

    expect(wrapper.text())
      .toContain("Kementerian C")

  })

  // =========================
  // TOP ORGANIZATION
  // =========================
  it("mengira organisasi terbaik", async () => {

    const wrapper =
      mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()
    await wrapper.vm.$nextTick()

    expect(wrapper.text())
      .toContain("90%")

    expect(wrapper.text())
      .toContain("Kementerian A")

  })

  // =========================
  // ORGANIZATION PERFORMANCE PANEL
  // =========================
  it("memaparkan panel prestasi organisasi", async () => {

    const wrapper =
      mount(DashboardContent)

    expect(wrapper.text())
      .toContain("Prestasi Organisasi")

  })

  // =========================
  // QUICK ACTIONS
  // =========================
  it("memaparkan tindakan pantas dashboard", async () => {

    const wrapper =
      mount(DashboardContent)

    const buttons =
      wrapper.findAll(".quick-actions button")

    expect(
      buttons.map((button) => button.text())
    ).toEqual([
      "Buka Konfigurasi",
      "Tambah Organisasi",
      "Pengguna"
    ])

  })

  // =========================
  // NAVIGATE CONFIGURATION
  // =========================
  it("navigasi ke configuration", async () => {

    const wrapper =
      mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const buttons =
      wrapper.findAll("button")

    const configButton =
      buttons.find(btn =>
        btn.text().includes("Konfigurasi")
      )

    await configButton.trigger("click")

    expect(pushMock)
      .toHaveBeenCalledWith(
        "/admin/configuration"
      )

  })

  // =========================
  // NAVIGATE ACCOUNTS
  // =========================
  it("navigasi ke accounts", async () => {

    const wrapper =
      mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const buttons =
      wrapper.findAll("button")

    const accountButton =
      buttons.find(btn =>
        btn.text().includes("Pengguna")
      )

    await accountButton.trigger("click")

    expect(pushMock)
      .toHaveBeenCalledWith(
        "/admin/accounts"
      )

  })

  // =========================
  // EMPTY STATE
  // =========================
  it("memaparkan empty state jika tiada organisasi", async () => {

    api.get.mockImplementation((url) => {

      if (url === "/dashboard/full") {

        return Promise.resolve({
          data: {
            stats: {
              organisasi: 0,
              sub_organisasi: 0,
              tapak: 0,
              profil: 0,
              tugasan: 0
            },
            organizations: [],
            profile_health: {
              counts: {},
              profiles: [],
              failed_profiles: [],
              scheduled_profiles: [],
              recent_profiles: []
            }
          }
        })

      }

      return Promise.resolve({
        data: {}
      })

    })

    const wrapper =
      mount(DashboardContent)

    await Promise.resolve()
    await Promise.resolve()
    await wrapper.vm.$nextTick()

    expect(wrapper.text())
      .toContain(
        "Tiada data organisasi"
      )

  })

})
