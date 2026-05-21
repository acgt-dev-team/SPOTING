import { mount } from "@vue/test-utils"
import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import ProfilListPage
from "../src/features/configuration/ProfilListPage.vue"

import api from "../src/services/api"

// =========================
// MOCK ROUTER
// =========================
const pushMock = vi.fn()

vi.mock("vue-router", () => ({
  useRoute: () => ({
    params: {
      organizationId: 1,
      subOrganizationId: 1,
      siteId: 1
    }
  }),

  useRouter: () => ({
    push: pushMock
  })
}))

// =========================
// MOCK FLATPICKR
// =========================
vi.mock("flatpickr", () => ({
  default: vi.fn()
}))

// =========================
// MOCK API
// =========================
vi.mock("../src/services/api", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}))

// =========================
// STUBS
// =========================
const AppInputStub = {
  props: ["modelValue"],

  template: `
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  `
}

const AppButtonStub = {
  props: ["text"],

  template: `
    <button @click="$emit('click')">
      {{ text }}
    </button>
  `
}

const AppCardStub = {
  template: `
    <div>
      <slot />
    </div>
  `
}

const AppSelectStub = {
  props: ["modelValue"],

  template: `
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option value="IMMEDIATE">
        Immediate
      </option>

      <option value="SCHEDULED">
        Scheduled
      </option>
    </select>
  `
}

const AppPaginationStub = {
  template: `
    <div>
      Pagination
    </div>
  `
}

const StatusPillStub = {
  template: `
    <div>Status</div>
  `
}

describe("ProfilListPage.vue", () => {

  beforeEach(() => {

    vi.clearAllMocks()

    api.get.mockImplementation((url) => {

      // =========================
      // PROFILE LIST
      // =========================
      if (
        url.includes("/profil/tapak/")
      ) {

        return Promise.resolve({
          data: [
            {
              id: 1,
              kod: "PRF001",
              nama: "Profil Test",
              keterangan: "Keterangan profil",
              tugasan_count: 5,
              execution_type: "IMMEDIATE",
              execution_status: "AKTIF",
              scheduled_at: null
            }
          ]
        })

      }

      // =========================
      // TAPAK DETAIL
      // =========================
      if (
        url.includes("/tapak/")
      ) {

        return Promise.resolve({
          data: {
            id: 1,
            nama: "Tapak Test",
            keterangan: "Keterangan tapak"
          }
        })

      }

      return Promise.resolve({
        data: []
      })

    })

  })

  // =========================
  // RENDER PAGE
  // =========================
  it("memaparkan halaman profil", async () => {

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    expect(wrapper.text())
      .toContain("Senarai Profil")

  })

  // =========================
  // FETCH PROFILE
  // =========================
  it("mengambil data profil", async () => {

    mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    await Promise.resolve()

    expect(api.get)
      .toHaveBeenCalled()

  })

  // =========================
  // SEARCH
  // =========================
  it("menerima input carian", async () => {

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    const input =
      wrapper.find('.search-box input')

    await input.setValue("profil")

    expect(input.element.value)
      .toBe("profil")

  })

  // =========================
  // OPEN ADD MODAL
  // =========================
  it("membuka modal tambah profil", async () => {

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    const button =
      wrapper.find(".primary-btn")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain("Tambah Profil")

  })

  // =========================
  // OPEN EDIT MODAL
  // =========================
  it("membuka modal edit profil", async () => {

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const editButtons =
      wrapper.findAll(".ghost-btn")

    expect(editButtons.length)
      .toBeGreaterThan(0)

    await editButtons[0]
      .trigger("click")

    expect(wrapper.text())
      .toContain("Edit Profil")

  })

  // =========================
  // SAVE PROFILE
  // =========================
  it("menyimpan profil baharu", async () => {

    api.post.mockResolvedValue({})

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    await wrapper.find(".primary-btn")
      .trigger("click")

    const inputs =
      wrapper.findAll("input")

    await inputs[1]
      .setValue("Profil Baru")

    await wrapper.vm.$nextTick()

    const modalButtons =
      wrapper.findAll(".modal-actions button")

    const saveButton =
      modalButtons[1]

    await saveButton.trigger("click")

    expect(api.post)
      .toHaveBeenCalled()

  })

  // =========================
  // DELETE MODAL
  // =========================
  it("membuka modal padam profil", async () => {

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const editButtons =
      wrapper.findAll(".ghost-btn")

    await editButtons[0]
      .trigger("click")

    const deleteButton =
      wrapper.find(".delete-trigger-btn")

    await deleteButton.trigger("click")

    expect(wrapper.text())
      .toContain("Padam")

  })

  // =========================
  // DELETE VALIDATION
  // =========================
  it("button padam disabled jika pengesahan salah", async () => {

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const editButtons =
      wrapper.findAll(".ghost-btn")

    await editButtons[0]
      .trigger("click")

    const deleteButton =
      wrapper.find(".delete-trigger-btn")

    await deleteButton.trigger("click")

    const confirmInput =
      wrapper.find(".delete-input")

    await confirmInput.setValue("salah")

    const dangerButton =
      wrapper.find(".danger-btn")

    expect(dangerButton.element.disabled)
      .toBe(true)

  })

  // =========================
  // ROUTER NAVIGATION
  // =========================
  it("navigasi ke tugasan apabila row diklik", async () => {

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const row =
      wrapper.find(".clickable-row")

    await row.trigger("click")

    expect(pushMock)
      .toHaveBeenCalledWith(
        "/admin/configuration/sub-organisasi/1/tapak/1/profil/1/tugasan/1"
      )

  })

  // =========================
  // TEMPLATE MODAL
  // =========================
  it("membuka modal template laporan", async () => {

    const wrapper = mount(ProfilListPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub,
          StatusPill: StatusPillStub
        }
      }
    })

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const buttons =
      wrapper.findAll(".ghost-btn")

    expect(buttons.length)
      .toBeGreaterThan(1)

    await buttons[1]
      .trigger("click")

    expect(wrapper.text())
      .toContain("Pilih Template")

  })

})