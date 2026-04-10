<script setup>
import { ref, computed } from "vue"

import AppCard from "../../ui/AppCard.vue"
import AppToolbar from "../../ui/AppToolbar.vue"
import AppModal from "../../ui/AppModal.vue"
import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"

const users = ref([
  {
    bil: 1,
    nama: "Khairul Izwan",
    username: "khairulizwan",
    peranan: "Pentadbir",
    email: "khairul.izwan@kkm.com.my"
  }
])

/* ✅ SEARCH (FIXED) */
const search = ref("")

const filteredUsers = computed(() => {
  const keyword = (search.value || "").toLowerCase()

  return users.value.filter((user) =>
    user?.nama?.toLowerCase().includes(keyword) ||
    user?.username?.toLowerCase().includes(keyword) ||
    user?.email?.toLowerCase().includes(keyword)
  )
})

const showModal = ref(false)
const showDeleteModal = ref(false)

const isEdit = ref(false)
const selectedIndex = ref(null)

const form = ref({
  nama: "",
  username: "",
  peranan: "",
  email: ""
})

const roles = ["Pentadbir", "Pengguna"]

/* TOAST */
const toast = ref({
  show: false,
  message: "",
  type: ""
})

function triggerToast(message, type) {
  toast.value = { show: true, message, type }
  setTimeout(() => {
    toast.value.show = false
  }, 2500)
}

function openAdd() {
  isEdit.value = false
  form.value = { nama: "", username: "", peranan: "", email: "" }
  showModal.value = true
}

function openEdit(user, index) {
  isEdit.value = true
  selectedIndex.value = index
  form.value = { ...user }
  showModal.value = true
}

function saveUser() {
  if (!form.value.nama || !form.value.username || !form.value.peranan || !form.value.email) {
    triggerToast("Sila isi nama rekod", "error")
    return
  }

  if (isEdit.value) {
    users.value[selectedIndex.value] = { ...form.value }
    triggerToast("Rekod berjaya dikemaskini", "success")
  } else {
    users.value.push({
      bil: users.value.length + 1,
      ...form.value
    })
    triggerToast("Rekod berjaya ditambah", "success")
  }

  showModal.value = false
}

function openDelete(index) {
  selectedIndex.value = index
  showDeleteModal.value = true
}

function confirmDelete() {
  users.value.splice(selectedIndex.value, 1)
  showDeleteModal.value = false
}
</script>

<template>
<div class="page">

  <!-- HEADER -->
  <div class="page-header">
    <div>
      <p class="eyebrow">PENGURUSAN</p>
      <h1 class="title">Pengurusan Pengguna</h1>
      <p class="subtitle">Senarai pengguna berdaftar dalam sistem.</p>
    </div>

    <button class="primary-btn" @click="openAdd">
      + Tambah Pengguna
    </button>
  </div>

  <!-- TABLE -->
  <AppCard>

    <!-- ✅ FIXED INPUT HANDLING -->
    <AppToolbar
      placeholder="Cari nama atau emel..."
      @input="search = $event.target.value"
    />

    <div class="table">
      <div class="row header">
        <div>Bil</div>
        <div>Nama</div>
        <div>Nama pengguna</div>
        <div>Peranan</div>
        <div>Email</div>
        <div></div>
      </div>

      <div v-for="(user,index) in filteredUsers" :key="user.bil" class="row">
        <div>{{ user.bil }}</div>
        <div class="bold">{{ user.nama }}</div>
        <div>{{ user.username }}</div>
        <div>
          <span class="badge" :class="user.peranan === 'Pentadbir' ? 'admin' : 'user'">
            {{ user.peranan }}
          </span>
        </div>
        <div>{{ user.email }}</div>

        <div>
          <button class="edit" @click="openEdit(user,index)">Edit</button>
          <button class="delete" @click="openDelete(index)">Padam</button>
        </div>
      </div>

      <div v-if="filteredUsers.length === 0" class="row">
        <div>Tiada pengguna dijumpai</div>
      </div>

    </div>

  </AppCard>

  <!-- MODAL -->
  <AppModal
    :show="showModal"
    :title="isEdit ? 'Kemaskini Pengguna' : 'Tambah Pengguna'"
    @close="showModal=false"
  >
    <div class="form-area">

      <AppInput v-model="form.nama" label="Nama" />
      <AppInput v-model="form.username" label="Username" />

      <div class="select-field">
        <label>Peranan</label>
        <select v-model="form.peranan">
          <option value="">Pilih peranan</option>
          <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
        </select>
      </div>

      <AppInput v-model="form.email" label="Email" />

    </div>

    <div class="modal-actions">
      <AppButton text="Batal" variant="outline" @click="showModal=false" />
      <AppButton text="Simpan" variant="primary" @click="saveUser" />
    </div>
  </AppModal>

  <!-- DELETE -->
  <AppModal
    :show="showDeleteModal"
    title="Padam Pengguna"
    @close="showDeleteModal=false"
  >
    <p>Adakah anda pasti mahu padam pengguna ini?</p>

    <div class="modal-actions">
      <AppButton text="Batal" variant="outline" @click="showDeleteModal=false" />
      <AppButton text="Padam" variant="primary" @click="confirmDelete" />
    </div>
  </AppModal>

  <!-- TOAST -->
  <div v-if="toast.show" class="toast">
    <span class="dot" :class="toast.type"></span>
    {{ toast.message }}
  </div>

</div>
</template>

<style scoped>
/* YOUR ORIGINAL STYLES (UNCHANGED) */
.page { display:flex; flex-direction:column; gap:24px; }
.page-header { display:flex; justify-content:space-between; align-items:flex-start; }
.eyebrow { font-size:12px; font-weight:700; color:#2563eb; }
.title { font-size:30px; font-weight:800; }
.subtitle { color:#6b7280; }

.primary-btn {
  background: linear-gradient(135deg,#020265,#0b0b8f);
  color:white;
  padding:12px 18px;
  border-radius:14px;
  border:none;
  font-weight:700;
}

.table { width:100%; }

.row {
  display:grid;
  grid-template-columns:60px 1.2fr 1fr 160px 1.2fr 160px;
  padding:18px 20px;
  border-bottom:1px solid #f1f5f9;
}

.header { font-weight:700; background:#f8fafc; }
.bold { font-weight:700; }

.badge { padding:6px 10px; border-radius:999px; font-size:12px; }
.admin { background:#dbeafe; color:#1d4ed8; }
.user { background:#dcfce7; color:#15803d; }

.edit {
  padding:6px 12px;
  border:1px solid #d1d5db;
  background:white;
  border-radius:8px;
}

.delete {
  padding:6px 12px;
  border:1px solid #fecaca;
  color:#dc2626;
  background:white;
  border-radius:8px;
  margin-left:6px;
}

.form-area { display:flex; flex-direction:column; gap:16px; }

.select-field { display:flex; flex-direction:column; }

select {
  padding:10px;
  border-radius:10px;
  border:1px solid #e5e7eb;
}

.modal-actions {
  display:flex;
  justify-content:flex-end;
  gap:12px;
  margin-top:20px;
}

.toast {
  position:fixed;
  bottom:20px;
  right:20px;
  background:white;
  padding:10px 14px;
  border-radius:8px;
  border:1px solid #e5e7eb;
  display:flex;
  gap:8px;
  z-index: 9999;
}

.dot { width:8px; height:8px; border-radius:50%; }
.dot.success { background:#10b981; }
.dot.error { background:#ef4444; }
</style>