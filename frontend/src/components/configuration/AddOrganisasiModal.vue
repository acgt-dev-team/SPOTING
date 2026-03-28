<script setup>
import { ref, watch } from "vue"
import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"
import AppCard from "../ui/AppCard.vue"

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(["close", "save"])

const nama = ref("")
const keterangan = ref("")

watch(
  () => props.show,
  (value) => {
    if (value) {
      nama.value = ""
      keterangan.value = ""
    }
  }
)

function closeModal() {
  emit("close")
}

function saveOrganisasi() {
  if (!nama.value.trim()) return

  emit("save", {
    id: Date.now(),
    name: nama.value,
    description: keterangan.value,
    subCount: 0,
    siteCount: 0,
    taskCount: 0,
    totalTaskCount: 0
  })
}
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="modal-overlay" @click.self="closeModal">
      <AppCard class="modal-card">
        <div class="modal-header">
          <div>
            <p class="eyebrow">TAMBAH DATA</p>
            <h2>Tambah Organisasi</h2>
          </div>

          <button class="close-btn" @click="closeModal">✕</button>
        </div>

        <div class="form-area">
          <AppInput
            v-model="nama"
            label="Nama Organisasi"
            placeholder="Masukkan nama organisasi"
          />

          <div class="textarea-field">
            <label class="textarea-label">Keterangan</label>
            <textarea
              v-model="keterangan"
              rows="5"
              placeholder="Masukkan penerangan ringkas"
            />
          </div>
        </div>

        <div class="modal-actions">
          <AppButton text="Batal" variant="outline" @click="closeModal" />
          <AppButton text="Simpan" variant="primary" @click="saveOrganisasi" />
        </div>
      </AppCard>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.18s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 24px;
}

.modal-card {
  width: 100%;
  max-width: 720px;
  padding: 28px !important;
  animation: popIn 0.18s ease;
  box-sizing: border-box;
}

@keyframes popIn {
  from {
    transform: translateY(8px) scale(0.98);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
}

.eyebrow {
  font-size: 12px;
  font-weight: 800;
  color: #9333ea;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 10px;
}

.modal-header h2 {
  font-size: 26px;
  font-weight: 900;
  color: #111827;
  line-height: 1.15;
}

.close-btn {
  border: none;
  background: #f3f4f6;
  width: 44px;
  height: 44px;
  border-radius: 999px;
  cursor: pointer;
  font-size: 18px;
  color: #374151;
  flex-shrink: 0;
}

.form-area {
  width: 100%;
}

.textarea-field {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
  width: 100%;
}

.textarea-label {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
}

textarea {
  width: 100%;
  min-height: 130px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  border-radius: 18px;
  padding: 16px;
  font-size: 15px;
  outline: none;
  transition: 0.2s ease;
  color: #111827;
  resize: vertical;
  box-sizing: border-box;
  font-family: inherit;
}

textarea:focus {
  border-color: #9333ea;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(147, 51, 234, 0.08);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 14px;
  margin-top: 28px;
  flex-wrap: wrap;
}
</style>