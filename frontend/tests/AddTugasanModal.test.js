import { mount } from "@vue/test-utils"
import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import AddTugasanModal
from "../src/features/configuration/components/AddTugasanModal.vue"

import api from "../src/services/api"

// =========================
// MOCK API
// =========================
vi.mock("../src/services/api", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn()
  }
}))

// =========================
// MOCK APPSELECT
// =========================
const AppSelectStub = {
  props: ["modelValue", "options", "label"],

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

describe("AddTugasanModal.vue", () => {

  beforeEach(() => {

    vi.clearAllMocks()

    api.get.mockResolvedValue({
      data: [
        {
          id: 1,
          nama: "Jenis A"
        }
      ]
    })

  })

  // =========================
  // RENDER
  // =========================
  it("memaparkan modal tambah tugasan", () => {

    const wrapper = mount(AddTugasanModal, {
      global: {
        stubs: {
          AppSelect: AppSelectStub
        }
      }
    })

    expect(wrapper.text())
      .toContain("Tambah Tugasan")

  })

  // =========================
  // FETCH JENIS
  // =========================
  it("mengambil data jenis tugasan", () => {

    mount(AddTugasanModal, {
      global: {
        stubs: {
          AppSelect: AppSelectStub
        }
      }
    })

    expect(api.get)
      .toHaveBeenCalledWith("/jenis_tugasan/")

  })

  // =========================
  // INPUT NAMA
  // =========================
  it("menerima input nama tugasan", async () => {

    const wrapper = mount(AddTugasanModal, {
      global: {
        stubs: {
          AppSelect: AppSelectStub
        }
      }
    })

    const input =
      wrapper.find('input[type="text"]')

    await input.setValue("Tugasan Test")

    expect(input.element.value)
      .toBe("Tugasan Test")

  })

  // =========================
  // BUTTON DISABLED
  // =========================
  it("butang simpan disabled jika maklumat tidak lengkap", () => {

    const wrapper = mount(AddTugasanModal, {
      global: {
        stubs: {
          AppSelect: AppSelectStub
        }
      }
    })

    const saveButton =
      wrapper.find(".panel-footer .ui-button--primary")

    expect(saveButton.element.disabled)
      .toBe(true)

  })

  // =========================
  // STATUS TOGGLE DISABLED
  // =========================
  it("toggle status sentiasa disabled", () => {

    const wrapper = mount(AddTugasanModal, {
      global: {
        stubs: {
          AppSelect: AppSelectStub
        }
      }
    })

    const toggle =
      wrapper.find(".toggle-btn")

    expect(toggle.attributes("disabled"))
      .toBeDefined()

  })

  // =========================
  // SAVE TUGASAN
  // =========================
  it("menyimpan tugasan baharu", async () => {

    api.post.mockResolvedValue({})

    const wrapper = mount(AddTugasanModal, {
      global: {
        stubs: {
          AppSelect: AppSelectStub
        }
      }
    })

    const inputs =
      wrapper.findAll("input")

    await inputs[0]
      .setValue("Tugasan Baru")

    const selects =
      wrapper.findAll("select")

    await selects[0]
      .setValue("1")

    await wrapper.vm.$nextTick()

    const saveButton =
      wrapper.find(".panel-footer .ui-button--primary")

    await saveButton.trigger("click")

    expect(api.post)
      .toHaveBeenCalled()

    expect(wrapper.emitted("saved"))
      .toBeTruthy()

    expect(wrapper.emitted("close"))
      .toBeTruthy()

  })

  // =========================
  // EDIT MODE
  // =========================
  it("mengemaskini tugasan sedia ada", async () => {

    api.put.mockResolvedValue({})

    const wrapper = mount(AddTugasanModal, {
      props: {
        task: {
          id: 99,
          nama: "Task Lama",
          jenis_id: 1,
          aktif: true
        }
      },

      global: {
        stubs: {
          AppSelect: AppSelectStub
        }
      }
    })

    await wrapper.vm.$nextTick()

    const saveButton =
      wrapper.find(".panel-footer .ui-button--primary")

    await saveButton.trigger("click")

    expect(api.put)
      .toHaveBeenCalled()

  })

})
