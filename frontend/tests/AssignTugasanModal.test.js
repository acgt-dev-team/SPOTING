import { mount } from "@vue/test-utils"
import {
  describe,
  it,
  expect,
  beforeEach,
  vi
} from "vitest"

import AssignTugasanModal
from "../src/features/configuration/components/AssignTugasanModal.vue"

import api from "../src/services/api"

// =========================
// MOCK ROUTER
// =========================
vi.mock("vue-router", () => ({
  useRoute: () => ({
    params: {
      profileId: 1
    }
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
// STUB CHILD MODAL
// =========================
const AddTugasanModalStub = {
  template: `
    <div>
      Add Tugasan Modal
    </div>
  `
}

describe("AssignTugasanModal.vue", () => {

  beforeEach(() => {

    vi.clearAllMocks()

    api.get.mockImplementation((url) => {

      // =========================
      // ALL TASKS
      // =========================
      if (url === "/tugasan/") {

        return Promise.resolve({
          data: [
            {
              id: 1,
              nama: "Ping Test",
              kod: "TGS001",
              protocol: "ICMP",
              aktif: true,
              ip_start: "192.168.0.1",
              ip_end: "192.168.0.10"
            },
            {
              id: 2,
              nama: "HTTP Check",
              kod: "TGS002",
              protocol: "HTTP",
              aktif: true,
              ip_start: "10.0.0.1",
              ip_end: "10.0.0.10"
            }
          ]
        })

      }

      // =========================
      // ASSIGNED TASKS
      // =========================
      if (
        url.includes("/tugasan/profil/")
      ) {

        return Promise.resolve({
          data: [
            {
              id: 1
            }
          ]
        })

      }

      return Promise.resolve({
        data: []
      })

    })

  })

  // =========================
  // RENDER MODAL
  // =========================
  it("memaparkan modal tugasan", async () => {

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    expect(wrapper.text())
      .toContain("Tetapkan Tugasan")

  })

  // =========================
  // FETCH TASKS
  // =========================
  it("mengambil senarai tugasan", async () => {

    mount(AssignTugasanModal, {
      global: {
        stubs: {
          AddTugasanModal:
            AddTugasanModalStub
        }
      }
    })

    await Promise.resolve()

    expect(api.get)
      .toHaveBeenCalledWith("/tugasan/")

  })

  // =========================
  // FETCH ASSIGNED
  // =========================
  it("mengambil tugasan yang telah ditetapkan", async () => {

    mount(AssignTugasanModal, {
      global: {
        stubs: {
          AddTugasanModal:
            AddTugasanModalStub
        }
      }
    })

    await Promise.resolve()

    expect(api.get)
      .toHaveBeenCalledWith(
        "/tugasan/profil/1"
      )

  })

  // =========================
  // SEARCH
  // =========================
  it("menerima input carian", async () => {

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    const input =
      wrapper.find(".search-box input")

    await input.setValue("Ping")

    expect(input.element.value)
      .toBe("Ping")

  })

  // =========================
  // SELECT CHECKBOX
  // =========================
  it("membolehkan pemilihan tugasan", async () => {

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const checkboxes =
      wrapper.findAll(
        '.row-item input[type="checkbox"]'
      )

    expect(checkboxes.length)
      .toBeGreaterThan(0)

    await checkboxes[1]
      .setValue(true)

    expect(wrapper.text())
      .toContain("2 dipilih")

  })

  // =========================
  // TOGGLE ALL
  // =========================
  it("memilih semua tugasan", async () => {

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const selectAll =
      wrapper.find(
        '.table-head input[type="checkbox"]'
      )

    await selectAll.setValue(true)

    expect(wrapper.text())
      .toContain("2 dipilih")

  })

  // =========================
  // CLEAR SELECTION
  // =========================
  it("mengosongkan pilihan tugasan", async () => {

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const selectAll =
      wrapper.find(
        '.table-head input[type="checkbox"]'
      )

    await selectAll.setValue(true)

    const clearButton =
      wrapper.find(".clear-btn")

    await clearButton.trigger("click")

    expect(wrapper.text())
      .toContain("0 dipilih")

  })

  // =========================
  // OPEN ADD MODAL
  // =========================
  it("membuka modal tambah tugasan", async () => {

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    const button =
      wrapper.find(".primary-btn")

    await button.trigger("click")

    expect(wrapper.text())
      .toContain("Add Tugasan Modal")

  })

  // =========================
  // OPEN EDIT MODAL
  // =========================
  it("membuka modal edit tugasan", async () => {

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    const editButtons =
      wrapper.findAll(".edit-btn")

    expect(editButtons.length)
      .toBeGreaterThan(0)

    await editButtons[0]
      .trigger("click")

    expect(wrapper.text())
      .toContain("Add Tugasan Modal")

  })

  // =========================
  // SUBMIT ASSIGNMENT
  // =========================
  it("menyimpan tetapan tugasan", async () => {

    api.post.mockResolvedValue({})
    api.delete.mockResolvedValue({})

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    // assign task 2
    const checkboxes =
      wrapper.findAll(
        '.row-item input[type="checkbox"]'
      )

    await checkboxes[1]
      .setValue(true)

    const saveButton =
      wrapper.find(".save-btn")

    await saveButton.trigger("click")

    expect(api.post)
      .toHaveBeenCalled()

    expect(wrapper.emitted("assigned"))
      .toBeTruthy()

    expect(wrapper.emitted("close"))
      .toBeTruthy()

  })

  // =========================
  // REMOVE ASSIGNMENT
  // =========================
  it("membuang tugasan yang dinyahpilih", async () => {

    api.post.mockResolvedValue({})
    api.delete.mockResolvedValue({})

    const wrapper = mount(
      AssignTugasanModal,
      {
        global: {
          stubs: {
            AddTugasanModal:
              AddTugasanModalStub
          }
        }
      }
    )

    await Promise.resolve()
    await wrapper.vm.$nextTick()

    // original task id=1 already selected
    const checkboxes =
      wrapper.findAll(
        '.row-item input[type="checkbox"]'
      )

    await checkboxes[0]
      .setValue(false)

    const saveButton =
      wrapper.find(".save-btn")

    await saveButton.trigger("click")

    expect(api.delete)
      .toHaveBeenCalled()

  })

})