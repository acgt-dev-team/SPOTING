<script setup>
import { reactive, ref, onMounted, computed, watch } from "vue"
import { X } from "lucide-vue-next"
import api from "../../../services/api"
import { t } from "../../../i18n"
import { useToast } from "../../../ui/AppToast.vue"

import AppSelect from "../../../ui/AppSelect.vue"

const emit = defineEmits(["close", "saved"])
const toast = useToast()

const saving = ref(false)

const props = defineProps({
  task: {
    type: Object,
    default: null
  }
})

const jenisList = ref([])

const isEditMode = computed(() => !!props.task)

const protocols = [
  "TCP",
  "UDP",
  "HTTP",
  "HTTPS",
  "ICMP",
  "SSH",
  "FTP",
  "SMTP"
]

const form = reactive({
  nama: "",
  protocol: "",
  ip_start: "",
  ip_end: "",
  kod: "",
  keterangan: "",
  aktif: true,
  jenis_id: ""
})

function resetForm() {
  form.nama = ""
  form.protocol = ""
  form.ip_start = ""
  form.ip_end = ""
  form.kod = ""
  form.keterangan = ""
  form.aktif = true
  form.jenis_id = ""
}

function fillForm(task) {
  form.nama = task.nama || ""
  form.protocol = task.protocol || ""
  form.ip_start = task.ip_start || ""
  form.ip_end = task.ip_end || ""
  form.kod = task.kod || ""
  form.keterangan = task.keterangan || ""
  form.aktif = task.aktif ?? true
  form.jenis_id = task.jenis_id ? String(task.jenis_id) : ""
}

watch(
  () => props.task,
  (val) => {
    if (val) {
      fillForm(val)
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

async function fetchJenis() {
  try {
    const res = await api.get("/jenis_tugasan/")
    jenisList.value = res.data || []
  } catch (err) {
    console.error("Failed to fetch jenis:", err)
    toast.error(t("common.loadFailed", { entity: t("configuration.taskList.countEntity") }))
  }
}

async function handleSave() {
  if (saving.value) return

  if (!form.nama || !form.jenis_id) {
    toast.warning(t("validation.completeBeforeSave"))
    return
  }

  try {
    saving.value = true

    const payload = {
      nama: form.nama,
      kod: form.kod || "AUTO-" + Date.now(),
      keterangan: form.keterangan,
      jenis_id: Number(form.jenis_id),
      protocol: form.protocol,
      ip_start: form.ip_start,
      ip_end: form.ip_end,
      aktif: form.aktif
    }

    if (isEditMode.value) {
      await api.put(`/tugasan/${props.task.id}`, payload)
    } else {
      await api.post("/tugasan/", payload)
    }

    emit("saved")
    emit("close")

  } catch (err) {
    console.error("Failed to save tugasan:", err)
    toast.error(t("common.saveFailed", { entity: t("configuration.taskList.countEntity") }))
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchJenis()
})
</script>

<template>
  <div class="side-panel">

    <!-- HEADER -->
    <div class="panel-header">

      <div>
        <p class="eyebrow">
          {{ isEditMode ? t("configuration.shared.editData") : t("configuration.shared.addData") }}
        </p>

        <h2>
          {{ isEditMode ? t("tasks.add.editTitle") : t("tasks.add.addTitle") }}
        </h2>

        <p class="subtext">
          {{
            isEditMode
              ? t("tasks.add.editDescription")
              : t("tasks.add.newDescription")
          }}
        </p>
      </div>

      <button
        class="ui-icon-button"
        :title="t('common.close')"
        :aria-label="t('common.close')"
        @click="$emit('close')"
      >
        <X :size="18" aria-hidden="true" />
      </button>

    </div>

    <!-- BODY -->
    <div class="panel-body">

      <!-- MAKLUMAT -->
      <div class="section-card">

        <h3>{{ t("tasks.add.info") }}</h3>

        <div class="field">
          <label>{{ t("tasks.add.nameRequired") }}</label>

          <input
            v-model="form.nama"
            type="text"
            :placeholder="t('tasks.add.namePlaceholder')"
          />
        </div>

        <AppSelect
          v-model="form.jenis_id"
          :label="t('tasks.add.type')"
          :options="jenisList.map(j => ({
            label: j.nama,
            value: String(j.id)
          }))"
        />

        <div class="field">
          <label>{{ t("tasks.add.code") }}</label>

          <input
            v-model="form.kod"
            type="text"
            :placeholder="t('tasks.add.codePlaceholder')"
          />
        </div>

      </div>

      <!-- NETWORK -->
      <div class="section-card">

        <h3>{{ t("tasks.add.network") }}</h3>

        <AppSelect
          v-model="form.protocol"
          :label="t('tasks.protocol')"
          :options="protocols.map(p => ({
            label: p,
            value: p
          }))"
        />

        <div class="grid-2">

          <div class="field">
            <label>{{ t("tasks.ipStart") }}</label>

            <input
              v-model="form.ip_start"
              type="text"
              :placeholder="t('tasks.add.ipStartPlaceholder')"
            />
          </div>

          <div class="field">
            <label>{{ t("tasks.ipEnd") }}</label>

            <input
              v-model="form.ip_end"
              type="text"
              :placeholder="t('tasks.add.ipEndPlaceholder')"
            />
          </div>

        </div>

      </div>

      <!-- KETERANGAN -->
      <div class="section-card">

        <h3>{{ t("common.description") }}</h3>

        <div class="field">
          <label>{{ t("tasks.add.description") }}</label>

          <textarea
            v-model="form.keterangan"
            rows="5"
            :placeholder="t('tasks.add.descriptionPlaceholder')"
          ></textarea>
        </div>

      </div>

      <!-- STATUS -->
      <div class="section-card">

        <h3>{{ t("common.status") }}</h3>

        <div class="toggle-row">

          <div>
            <p class="toggle-title">{{ t("tasks.add.statusTitle") }}</p>

            <p class="toggle-desc">
              {{ t("tasks.add.statusDescription") }}
            </p>
          </div>

          <button
            type="button"
            class="toggle-btn active"
            disabled
          >
            <span></span>
          </button>

        </div>

        <div class="status-pill" :class="form.aktif ? 'on' : 'off'">
          {{ form.aktif ? t("status.active") : t("status.notActive") }}
        </div>

      </div>

    </div>

    <!-- FOOTER -->
    <div class="panel-footer">

      <button
        class="ui-button ui-button--outline"
        @click="$emit('close')"
      >
        {{ t("common.cancel") }}
      </button>

      <button
        class="ui-button ui-button--primary"
        :disabled="!form.nama || !form.jenis_id || saving"
        @click="handleSave"
      >
        {{
          saving
            ? t("common.saving")
            : isEditMode
              ? t("common.saveChanges")
              : t("tasks.add.save")
        }}
      </button>

    </div>

  </div>
</template>

<style scoped>
.side-panel {
  width: 430px;
  max-width: 100%;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #E2E8F0;
  box-shadow: 0 1px 2px rgba(15,23,42,.04);
  display: flex;
  flex-direction: column;
  max-height: 760px;
  overflow: hidden;
}

.panel-header {
  padding: 28px;
  border-bottom: 1px solid #F1F5F9;
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.eyebrow {
  font-size: 12px;
  font-weight: 700;
  color: #4F46E5;
  letter-spacing: .12em;
  margin-bottom: 10px;
}

.panel-header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.15;
}

.subtext {
  margin-top: 8px;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
  max-width: 320px;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.section-card {
  background: #ffffff;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 20px;
}

.section-card h3 {
  margin: 0 0 18px;
  font-size: 15px;
  font-weight: 900;
  color: #111827;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.field:last-child {
  margin-bottom: 0;
}

.field label {
  font-size: 13px;
  font-weight: 700;
  color: #374151;
}

input,
textarea {
  width: 100%;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 14px 16px;
  font-size: 14px;
  color: #111827;
  background: #F8FAFC;
  box-sizing: border-box;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: var(--color-focus-border);
  background: white;
  box-shadow: var(--focus-ring);
}

textarea {
  resize: vertical;
  min-height: 130px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.toggle-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

.toggle-title {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: #111827;
}

.toggle-desc {
  margin-top: 4px;
  font-size: 13px;
  color: #6b7280;
}

.toggle-btn {
  width: 56px;
  height: 32px;
  border-radius: 999px;
  border: none;
  background: #d1d5db;
  position: relative;
  cursor: pointer;
  transition: 0.2s ease;
  flex-shrink: 0;
}

.toggle-btn span {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 999px;
  transition: 0.2s ease;
}

.toggle-btn.active {
  background: #4F46E5;
}

.toggle-btn.active span {
  transform: translateX(24px);
}

.status-pill {
  margin-top: 16px;
  display: inline-flex;
  padding: 10px 14px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 800;
}

.status-pill.on {
  background: #ecfdf5;
  color: #16a34a;
}

.status-pill.off {
  background: #fef2f2;
  color: #dc2626;
}

.panel-footer {
  padding: 22px 28px;
  border-top: 1px solid #F1F5F9;
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

@media (max-width: 1100px) {
  .side-panel {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }

  .panel-footer {
    flex-direction: column;
  }

  .panel-header {
    padding: 22px;
  }

  .panel-body {
    padding: 18px;
  }
}

.toggle-btn:disabled {
  cursor: not-allowed;
  opacity: 1;
}

.toggle-btn:disabled:hover {
  background: #dc2626;
}

.toggle-btn:disabled:hover span {
  background: white;
}
</style>
