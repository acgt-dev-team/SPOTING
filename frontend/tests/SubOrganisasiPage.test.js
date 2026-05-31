import { mount } from "@vue/test-utils"
import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import SubOrganisasiPage
from "../src/features/configuration/SubOrganisasiPage.vue"

import api from "../src/services/api"

// =========================
// MOCK ROUTER
// =========================
const pushMock = vi.fn()

vi.mock("vue-router", () => ({
  useRoute: () => ({
    params: {
      organizationId: 1
    }
  }),

  useRouter: () => ({
    push: pushMock
  })
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

const AppPaginationStub = {
  template: `
    <div>
      Pagination
    </div>
  `
}

describe("SubOrganisasiPage.vue", () => {

  beforeEach(() => {

    vi.clearAllMocks()

    api.get.mockImplementation((url) => {

      // =========================
      // SUB ORGANISASI LIST
      // =========================
      if (
        url.includes(
          "/sub-organisasi/organisasi/"
        )
      ) {

        return Promise.resolve({
          data: [
            {
              id: 1,
              kod: "SUB001",
              nama: "Sub Organisasi Test",
              keterangan: "Keterangan sub",
              pegawai_tadbir: "Ali",
              jawatan: "Pengurus",
              tapak_count: 3
            }
          ]
        })

      }

      // =========================
      // ORGANISASI DETAIL
      // =========================
      if (url.includes("/organisasi/")) {

        return Promise.resolve({
          data: {
            id: 1,
            nama: "Organisasi Test",
            keterangan: "Keterangan organisasi"
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
  it("memaparkan halaman sub organisasi", async () => {

    const wrapper = mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    expect(wrapper.text())
      .toContain("Senarai Sub Organisasi")

  })

  // =========================
  // FETCH DATA
  // =========================
  it("mengambil data sub organisasi", async () => {

    mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
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

    const wrapper = mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    const input =
      wrapper.find('.search-box input')

    await input.setValue("sub")

    expect(input.element.value)
      .toBe("sub")

  })

  // =========================
  // OPEN ADD MODAL
  // =========================
  it("membuka modal tambah sub organisasi", async () => {

    const wrapper = mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    const button =
      wrapper.find(".primary-btn")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain("Tambah Sub Organisasi")

  })

  // =========================
  // OPEN EDIT MODAL
  // =========================
  it("membuka modal edit sub organisasi", async () => {

    const wrapper = mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
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
      .toContain("Edit Sub Organisasi")

  })

  // =========================
  // SAVE NEW SUB
  // =========================
  it("menyimpan sub organisasi baharu", async () => {

    api.post.mockResolvedValue({})

    const wrapper = mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    await wrapper.find(".primary-btn")
      .trigger("click")

    const inputs =
      wrapper.findAll("input")

    await inputs[1]
      .setValue("Sub Baru")

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
  it("membuka modal padam sub organisasi", async () => {

    const wrapper = mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
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

    const wrapper = mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
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
  it("navigasi ke tapak apabila row diklik", async () => {

    const wrapper = mount(SubOrganisasiPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
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
        "/admin/configuration/sub-organisasi/1/tapak/1"
      )

  })

})