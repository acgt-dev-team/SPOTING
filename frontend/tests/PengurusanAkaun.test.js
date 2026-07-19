import { mount } from "@vue/test-utils"
import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import PengurusanAkaun
from "../src/features/configuration/PengurusanAkaun.vue"

import api from "../src/services/api"

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
  props: ["text", "variant", "disabled"],

  template: `
    <button
      :class="['ui-button', 'ui-button--' + (variant || 'primary')]"
      :disabled="disabled"
      @click="$emit('click')"
    >
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
  props: ["modelValue", "options"],

  template: `
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  `
}

const AppPaginationStub = {
  template: `<div></div>`
}

describe("PengurusanAkaun.vue", () => {

  beforeEach(() => {

    vi.clearAllMocks()

    sessionStorage.setItem(
      "role",
      "super admin"
    )

    api.get.mockResolvedValue({
      data: [
        {
          id: 1,
          nama: "Admin Test",
          username: "admin",
          role: "admin",
          aktif: true
        }
      ]
    })

  })

  // =========================
  // RENDER PAGE
  // =========================
  it("memaparkan halaman pengurusan pengguna", () => {

    const wrapper = mount(PengurusanAkaun, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    expect(wrapper.text())
      .toContain("Pengurusan Pengguna")

  })

  // =========================
  // FETCH USERS
  // =========================
  it("mengambil senarai pengguna", () => {

    mount(PengurusanAkaun, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    expect(api.get)
      .toHaveBeenCalledWith("/auth/users?role=super admin")

  })

  // =========================
  // OPEN MODAL
  // =========================
  it("membuka modal tambah akaun", async () => {

    const wrapper = mount(PengurusanAkaun, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    const button =
      wrapper.find(".toolbar .ui-button--primary")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain("Tambah Akaun")

  })

  // =========================
  // SEARCH INPUT
  // =========================
  it("menerima input carian", async () => {

    const wrapper = mount(PengurusanAkaun, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    const input =
      wrapper.find(".search-box input")

    await input.setValue("admin")

    expect(input.element.value)
      .toBe("admin")

  })

  // =========================
  // EDIT ACCOUNT
  // =========================
  it("membuka modal edit akaun", async () => {

    const wrapper = mount(PengurusanAkaun, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
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
      .toContain("Kemaskini Akaun")

  })

  // =========================
  // SAVE NEW ACCOUNT
  // =========================
  it("menyimpan akaun baharu", async () => {

    api.post.mockResolvedValue({
      data: {
        generated_password: "abc123"
      }
    })

    window.alert = vi.fn()

    const wrapper = mount(PengurusanAkaun, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
          AppPagination: AppPaginationStub
        }
      }
    })

    await wrapper.find(".toolbar .ui-button--primary")
      .trigger("click")

    const inputs =
      wrapper.findAll("input")

    await inputs[1]
      .setValue("Ali")

    await inputs[2]
      .setValue("ali.akaun123")

    const saveButtons =
      wrapper.findAll(".form-modal__actions button")

    await saveButtons[1]
      .trigger("click")

    expect(api.post)
      .toHaveBeenCalled()

  })

  // =========================
  // DELETE MODAL
  // =========================
  it("membuka modal padam", async () => {

    const wrapper = mount(PengurusanAkaun, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
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

    const deleteButton =
      wrapper.find(".form-modal__actions .ui-button--danger")

    await deleteButton.trigger("click")

    expect(wrapper.text())
      .toContain("Padam")

  })

  // =========================
  // TOGGLE MODAL
  // =========================
  it("membuka modal toggle status", async () => {

    const wrapper = mount(PengurusanAkaun, {
      global: {
        stubs: {
          AppInput: AppInputStub,
          AppButton: AppButtonStub,
          AppCard: AppCardStub,
          AppSelect: AppSelectStub,
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

    const toggle =
      wrapper.find('input[type="checkbox"]')

    await toggle.trigger("click")

    expect(wrapper.text())
      .toContain("Nyahaktif")

  })

})
