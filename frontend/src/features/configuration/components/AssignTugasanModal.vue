<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Icon } from '@iconify/vue'
import AddTugasanModal from './AddTugasanModal.vue'
import api from '../../../services/api'

// emit
const emit = defineEmits(['close', 'assigned'])

// route
const route = useRoute()
const profileId = route.params.profileId

// state
const tugasanList = ref([])
const showAdd = ref(false)
const search = ref('')
const selectedIds = ref([])
const originalIds = ref([])

// 🔥 LOAD ALL TUGASAN
async function loadTugasan() {
  try {
    const res = await api.get('/tugasan/')
    tugasanList.value = res.data
  } catch (err) {
    console.error('Failed to load tugasan:', err)
  }
}

// 🔥 LOAD ASSIGNED (IMPORTANT)
async function loadAssigned() {
  try {
    const res = await api.get(`/tugasan/profil/${profileId}`)

    selectedIds.value = res.data.map(t => t.id)
    originalIds.value = [...selectedIds.value]

  } catch (err) {
    console.error('Failed to load assigned:', err)
  }
}



// 🔍 FILTER
const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return tugasanList.value

  return tugasanList.value.filter(t =>
    t.nama?.toLowerCase().includes(q) ||
    t.kod?.toLowerCase().includes(q) ||
    t.protocol?.toLowerCase().includes(q)
  )
})

// 🔥 AFTER ADD NEW
function onSaved() {
  loadTugasan()
  showAdd.value = false
}

async function handleSubmit() {
  try {
    const toAdd = selectedIds.value.filter(id => !originalIds.value.includes(id))
    const toRemove = originalIds.value.filter(id => !selectedIds.value.includes(id))

    // ADD
    for (const id of toAdd) {
      await api.post(`/tugasan/profil/${profileId}`, {
        tugasan_id: id,
        status: -1
      })
    }

    // REMOVE
    for (const id of toRemove) {
      await api.delete(`/tugasan/profil/${profileId}/${id}`)
    }

    emit('assigned')
    emit('close')

  } catch (err) {
    console.error('Update failed:', err)
  }
}

// ✅ SELECT ALL / NONE
const allChecked = computed(() => {
  const ids = filtered.value.map(t => t.id)
  return ids.length > 0 && ids.every(id => selectedIds.value.includes(id))
})

const someChecked = computed(() => {
  const ids = filtered.value.map(t => t.id)
  return ids.some(id => selectedIds.value.includes(id)) && !allChecked.value
})

function toggleAll() {
  const ids = filtered.value.map(t => t.id)

  if (allChecked.value) {
    // remove all visible
    selectedIds.value = selectedIds.value.filter(id => !ids.includes(id))
  } else {
    // add all visible (avoid duplicates)
    selectedIds.value = [...new Set([...selectedIds.value, ...ids])]
  }
}


// 🎨 PROTOCOL COLOR
function protocolColor(p) {
  const map = {
    TCP: '#3b82f6',
    UDP: '#8b5cf6',
    HTTP: '#22c55e',
    HTTPS: '#10b981',
    ICMP: '#f59e0b',
    SSH: '#ef4444'
  }
  return map[p] || '#64748b'
}

onMounted(() => {
  loadTugasan()
  loadAssigned()
})
</script>

<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal-wrapper">

```
  <!-- MAIN MODAL -->
  <div class="modal">

    <!-- HEADER -->
    <div class="modal__header">
      <div class="modal__header-left">
        <div class="modal__icon-wrap">
          <Icon icon="mdi:clipboard-list-outline" />
        </div>
        <div>
          <h2>Assign Tugasan</h2>
          <p>Pilih tugasan untuk ditetapkan</p>
        </div>
      </div>

      <button @click="$emit('close')">✕</button>
    </div>

    <!-- ACTION BAR -->
    <div class="modal__actions-bar">
      <button @click="showAdd = true">
        + Tambah Tugasan Baru
      </button>

      <input
        v-model="search"
        placeholder="Cari tugasan..."
      />
    </div>

    <!-- LIST -->
    <div class="modal__body">

      <!-- HEADER -->
      <div class="list-header">
        <input
  type="checkbox"
  :checked="allChecked"
  :indeterminate.prop="someChecked"
  @change="toggleAll"
/>
        <span>Nama / Kod</span>
        <span>Protokol</span>
        <span>IP Range</span>
        <span>Status</span>
      </div>

      <!-- ITEMS -->
      <div class="tugasan-list">

        <label
          v-for="t in filtered"
          :key="t.id"
          class="tugasan-item"
        >
       <input
  type="checkbox"
  :value="t.id"
  v-model="selectedIds"
/>

          <div>
            <div>{{ t.nama }}</div>
            <small>{{ t.kod }}</small>
          </div>

          <div>
            <span :style="{ color: protocolColor(t.protocol) }">
              {{ t.protocol || '-' }}
            </span>
          </div>

          <div>
            {{ t.ip_start }} → {{ t.ip_end }}
          </div>

          <div>
            {{ t.aktif ? 'Aktif' : 'Tidak' }}
          </div>
        </label>

      </div>
    </div>

    <!-- FOOTER -->
    <div class="modal__footer">
      <button class="btn btn--ghost" @click="$emit('close')">Batal</button>

      <button class="btn btn--primary"
        :disabled="selectedIds.length === 0"
        @click="handleSubmit"
      >
        Tetapkan
      </button>
    </div>

  </div>

  <!-- SIDE MODAL -->
  <Transition name="slide">
    <AddTugasanModal
      v-if="showAdd"
      @close="showAdd = false"
      @saved="onSaved"
    />
  </Transition>

</div>
```

  </div>
</template>


<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: var(--bg-overlay);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 24px;
  animation: fadeIn 0.18s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

.modal-wrapper {
  display: flex;
  height: min(680px, 90vh);
  max-width: 960px;
  width: 100%;
  border-radius: 14px;
  overflow: hidden;
  box-shadow:
    0 0 0 1px var(--border-subtle),
    0 24px 60px rgba(0,0,0,0.6);
  animation: popIn 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes popIn {
  from { transform: scale(0.94); opacity: 0; }
  to   { transform: scale(1);    opacity: 1; }
}

.modal {
  background: #ffffff;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

/* Header */
.modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.modal__header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.modal__icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--accent-glow);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(59, 130, 246, 0.35);
}

.modal__icon {
  font-size: 20px;
  color: var(--accent);
}

.modal__title {
  margin: 0;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.modal__subtitle {
  margin: 2px 0 0;
  font-size: 12px;
  color: var(--text-muted);
}

.modal__close {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  border-radius: 8px;
  font-size: 18px;
  display: flex;
  transition: color 0.15s, background 0.15s;
}

.modal__close:hover {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

/* Actions bar */
.modal__actions-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 24px;
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.btn-add {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: var(--accent-glow);
  border: 1px solid rgba(59, 130, 246, 0.4);
  border-radius: 8px;
  color: #93c5fd;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn-add:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.6);
}

.search-wrap {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 16px;
}

.search-input {
  width: 100%;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  padding: 8px 12px 8px 34px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.search-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-glow);
}

.search-input::placeholder { color: var(--text-muted); }

/* Selection bar */
.modal__selection-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 24px;
  background: rgba(59, 130, 246, 0.08);
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
  font-size: 12px;
  color: #93c5fd;
  font-weight: 500;
  flex-shrink: 0;
}

.sel-icon { font-size: 14px; }

.sel-clear {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 11px;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  transition: color 0.15s;
}

.sel-clear:hover { color: var(--danger); }

/* List */
.modal__body {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.list-header {
  display: grid;
  grid-template-columns: 36px 1fr 90px 180px 80px;
  align-items: center;
  padding: 8px 24px;
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.list-header > span {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.list-header__check {
  display: flex;
  align-items: center;
}

.tugasan-list {
  flex: 1;
  overflow-y: auto;
}

.tugasan-item {
  display: grid;
  grid-template-columns: 36px 1fr 90px 180px 80px;
  align-items: center;
  padding: 12px 24px;
  border-bottom: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: background 0.12s;
  gap: 0;
}

.tugasan-item:last-child { border-bottom: none; }

.tugasan-item:hover {
  background: var(--bg-elevated);
}

.tugasan-item--selected {
  background: rgba(59, 130, 246, 0.07);
}

.tugasan-item--selected:hover {
  background: rgba(59, 130, 246, 0.12);
}

.tugasan-item__check {
  accent-color: var(--accent);
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.tugasan-item__info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.tugasan-item__nama {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tugasan-item__kod {
  font-size: 11px;
  color: var(--text-muted);
  font-family: 'Courier New', monospace;
}

.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  border: 1px solid;
  letter-spacing: 0.04em;
}

.tugasan-item__ip {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: var(--text-secondary);
  font-family: 'Courier New', monospace;
  white-space: nowrap;
  overflow: hidden;
}

.ip-sep { color: var(--text-muted); }

.tugasan-item__status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-dot--on  { background: var(--success); box-shadow: 0 0 6px var(--success); }
.status-dot--off { background: var(--text-muted); }

/* Empty */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  color: var(--text-muted);
  gap: 12px;
}

.empty-icon { font-size: 36px; }
.empty-state p { margin: 0; font-size: 14px; }

/* Footer */
.modal__footer {
  display: flex;
  gap: 10px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
  flex-shrink: 0;
  background: #ffffff;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 8px;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: background 0.15s, opacity 0.15s;
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
  position: relative;
  background: #3e4fd1;
  color: #ffffff;
  border: 1px solid var(--border-subtle);
}

.btn--primary:hover {
  background: #2a40b0;
  color: var(--text-primary);
}

/* Side panel transition */
.slide-enter-active { animation: slideIn 0.22s ease; }
.slide-leave-active { animation: slideIn 0.18s ease reverse; }

@keyframes slideIn {
  from { transform: translateX(20px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}

/* Checkbox indeterminate support */
input[type="checkbox"] {
  accent-color: var(--accent);
  width: 16px;
  height: 16px;
  cursor: pointer;
}
</style>
