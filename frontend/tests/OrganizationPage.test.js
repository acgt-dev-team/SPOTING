import { mount } from "@vue/test-utils"
import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import OrganizationPage
from "../src/features/configuration/OrganizationPage.vue"

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
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}))

// =========================
// MOCK COMPONENTS
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
  props: ["currentPage", "totalPages"],

  template: `
    <div class="pagination-stub">
      Pagination
    </div>
  `
}

describe("OrganizationPage.vue", () => {

  beforeEach(() => {

    vi.clearAllMocks()

    api.get.mockResolvedValue({
      data: [
        {
          id: 1,
          kod: "ORG001",
          nama: "Organisasi Test",
          keterangan: "Keterangan Test",
          pegawai_tadbir: "Ali",
          jawatan: "Pengurus",
          sub_count: 2,
          tapak_count: 3,
          tugasan_count: 5
        }
      ]
    })

  })

  // =========================
  // RENDER PAGE
  // =========================
  it("memaparkan halaman organisasi", async () => {

    const wrapper = mount(OrganizationPage, {
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
      .toContain("Senarai Organisasi")

  })

  // =========================
  // FETCH ORGANIZATION
  // =========================
  it("mengambil data organisasi", async () => {

    mount(OrganizationPage, {
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
      .toHaveBeenCalledWith("/organisasi/pelanggan/1")

  })

  // =========================
  // SEARCH INPUT
  // =========================
  it("menerima input carian", async () => {

    const wrapper = mount(OrganizationPage, {
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

    await input.setValue("test")

    expect(input.element.value)
      .toBe("test")

  })

  // =========================
  // OPEN ADD MODAL
  // =========================
  it("membuka modal tambah organisasi", async () => {

    const wrapper = mount(OrganizationPage, {
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
      wrapper.find(".toolbar .ui-button--primary")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain("Tambah Organisasi")

  })

  // =========================
  // OPEN EDIT MODAL
  // =========================
  it("membuka modal edit organisasi", async () => {

    const wrapper = mount(OrganizationPage, {
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
      wrapper.findAll(".clickable-row .ui-icon-button")

    expect(editButtons.length)
      .toBeGreaterThan(0)

    await editButtons[0]
      .trigger("click")

    expect(wrapper.text())
      .toContain("Kemaskini Organisasi")

  })

  // =========================
  // SAVE ORGANIZATION
  // =========================
  
  it("menyimpan organisasi baharu", async () => {

    api.post.mockResolvedValue({})

    const wrapper = mount(OrganizationPage, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    await wrapper.find(".toolbar .ui-button--primary")
      .trigger("click")

    const inputs =
      wrapper.findAll("input")

    await inputs[1]
      .setValue("Organisasi Baru")

    await wrapper.vm.$nextTick()

    const modalButtons =
      wrapper.findAll(".modal-actions button")

    expect(modalButtons.length)
      .toBeGreaterThan(0)

    const saveButton =
      modalButtons[1]

    await saveButton.trigger("click")

    expect(api.post)
      .toHaveBeenCalled()

  })

  // =========================
  // DELETE MODAL
  // =========================
  it("membuka modal padam organisasi", async () => {

    const wrapper = mount(OrganizationPage, {
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
      wrapper.findAll(".clickable-row .ui-icon-button")

    await editButtons[0]
      .trigger("click")

    const deleteButton =
      wrapper.find(".modal-actions .ui-button--danger")

    await deleteButton.trigger("click")

    expect(wrapper.text())
      .toContain("Padam")

  })

  // =========================
  // DELETE VALIDATION
  // =========================
  it("button padam disabled jika pengesahan salah", async () => {

    const wrapper = mount(OrganizationPage, {
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
      wrapper.findAll(".clickable-row .ui-icon-button")

    await editButtons[0]
      .trigger("click")

    const deleteButton =
      wrapper.find(".modal-actions .ui-button--danger")

    await deleteButton.trigger("click")

    const confirmInput =
      wrapper.find(".delete-input")

    await confirmInput.setValue("salah")

    const dangerButton =
      wrapper.find(".delete-actions .ui-button--danger")

    expect(dangerButton.element.disabled)
      .toBe(true)

  })

  // =========================
  // NAVIGATION
  // =========================
  it("navigasi ke sub organisasi apabila row diklik", async () => {

    const wrapper = mount(OrganizationPage, {
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
        "/admin/configuration/sub-organisasi/1"
      )

  })

})
