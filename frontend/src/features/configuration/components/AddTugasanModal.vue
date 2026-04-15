<script setup>
import { reactive, ref } from 'vue';
import { Icon } from '@iconify/vue';
import api from '../../../services/api'

const emit = defineEmits(['close', 'saved']);

const form = reactive({
  nama: '',
  protocol: '',
  ip_start: '',
  ip_end: '',
  kod: '',
  keterangan: '',
  aktif: true,
  jenis_id: '',
});

const saving = ref(false);

const protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'ICMP', 'SSH', 'FTP', 'SMTP'];

async function handleSave() {
  if (!form.nama || !form.jenis_id) return;

  saving.value = true;

  try {
    const res = await api.post('/tugasan', {
      nama: form.nama,
      kod: form.kod || "AUTO-" + Date.now(),
      keterangan: form.keterangan,
      jenis_id: Number(form.jenis_id),
      protocol: form.protocol,
      ip_start: form.ip_start,
      ip_end: form.ip_end,
      aktif: form.aktif
    })

    emit('saved', res.data)

  } catch (err) {
    console.error('Failed to create tugasan:', err)
  } finally {
    saving.value = false
  }
}

function handleCancel() {
  emit('close');
}
</script>

<template>
  <div class="add-modal">
    <div class="add-modal__header">
      <div class="add-modal__title-row">
        <Icon icon="mdi:plus-circle-outline" class="add-modal__icon" />
        <h3 class="add-modal__title">Tambah Tugasan Baru</h3>
      </div>
      <button class="add-modal__close" @click="handleCancel" aria-label="Tutup">
        <Icon icon="mdi:close" />
      </button>
    </div>

    <div class="add-modal__body">
      <div class="field">
        <label class="field__label">Nama Tugasan <span class="field__req">*</span></label>
        <input
          v-model="form.nama"
          type="text"
          class="field__input"
          placeholder="Masukkan nama tugasan"
        />
      </div>

      <div class="field">
        <label class="field__label">Jenis ID <span class="field__req">*</span></label>
        <input
          v-model="form.jenis_id"
          type="number"
          class="field__input"
          placeholder="ID jenis tugasan"
          min="1"
        />
      </div>

      <div class="field">
        <label class="field__label">Protokol</label>
        <select v-model="form.protocol" class="field__input field__select">
          <option value="">-- Pilih Protokol --</option>
          <option v-for="p in protocols" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>

      <div class="field-row">
        <div class="field">
          <label class="field__label">IP Mula</label>
          <input
            v-model="form.ip_start"
            type="text"
            class="field__input"
            placeholder="192.168.0.1"
          />
        </div>
        <div class="field">
          <label class="field__label">IP Akhir</label>
          <input
            v-model="form.ip_end"
            type="text"
            class="field__input"
            placeholder="192.168.0.254"
          />
        </div>
      </div>

      <div class="field">
        <label class="field__label">Kod</label>
        <input
          v-model="form.kod"
          type="text"
          class="field__input"
          placeholder="Kod unik tugasan"
        />
      </div>

      <div class="field">
        <label class="field__label">Keterangan</label>
        <textarea
          v-model="form.keterangan"
          class="field__input field__textarea"
          placeholder="Huraian tugasan..."
          rows="3"
        ></textarea>
      </div>

      <div class="field field--toggle">
        <label class="field__label">Status Aktif</label>
        <button
          type="button"
          class="toggle"
          :class="{ 'toggle--on': form.aktif }"
          @click="form.aktif = !form.aktif"
          :aria-pressed="form.aktif"
        >
          <span class="toggle__thumb"></span>
        </button>
        <span class="toggle__label">{{ form.aktif ? 'Aktif' : 'Tidak Aktif' }}</span>
      </div>
    </div>

    <div class="add-modal__footer">
      <button class="btn btn--ghost" @click="handleCancel">
        Batal
      </button>
      <button
        class="btn btn--primary"
        :disabled="!form.nama || !form.jenis_id || saving"
        @click="handleSave"
      >
      Simpan
      </button>
    </div>
  </div>
</template>

<style scoped>
.add-modal {
  width: 380px;
  min-height: 100%;
  background: var(--bg-elevated);
  border-left: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  animation: slideIn 0.22s ease;
}

@keyframes slideIn {
  from { transform: translateX(24px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}

.add-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 20px 16px;
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.add-modal__title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.add-modal__icon {
  font-size: 18px;
  color: var(--accent);
}

.add-modal__title {
  margin: 0;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
}

.add-modal__close {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  display: flex;
  border-radius: 6px;
  font-size: 16px;
  transition: color 0.15s, background 0.15s;
}

.add-modal__close:hover {
  color: var(--text-primary);
  background: #ffffff;
}

.add-modal__body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field--toggle {
  flex-direction: row;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid var(--border-subtle);
}

.field--toggle .field__label {
  flex: 1;
  margin: 0;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.field__label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.field__req {
  color: var(--danger);
}

.field__input {
  background: #ffffff;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  padding: 9px 12px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  width: 100%;
}

.field__input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-glow);
}

.field__input::placeholder {
  color: var(--text-muted);
}

.field__select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%2364748b'%3E%3Cpath fill-rule='evenodd' d='M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z' clip-rule='evenodd'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px;
  cursor: pointer;
}

.field__textarea {
  resize: vertical;
  min-height: 72px;
}

/* Toggle */
.toggle {
  position: relative;
  width: 40px;
  height: 22px;
  border-radius: 11px;
  background: var(--border-default);
  border: none;
  cursor: pointer;
  transition: background 0.2s;
  padding: 0;
  flex-shrink: 0;
}

.toggle--on {
  background: var(--accent);
}

.toggle__thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #e2dede;
  transition: transform 0.2s;
  display: block;
}

.toggle--on .toggle__thumb {
  transform: translateX(18px);
}

.toggle__label {
  font-size: 12px;
  color: var(--text-secondary);
}

/* Buttons */
.add-modal__footer {
  padding: 16px 20px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 16px;
  border-radius: 8px;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: background 0.15s, opacity 0.15s;
  flex: 1;
  justify-content: center;
}

.btn--ghost {
  background: #ffffff;
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
}

.btn--ghost:hover {
  background: var(--border-subtle);
  color: var(--text-primary);
}

.btn--primary {
  background: #3e4fd1;
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
}

.btn--primary:hover {
  background: var(--border-subtle);
  color: var(--text-primary);
}

.btn--primary:disabled {
  opacity: 0.95;
  cursor: not-allowed;
}

.spin {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
