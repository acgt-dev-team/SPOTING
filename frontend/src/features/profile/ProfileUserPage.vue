<script setup>
import { ref, onMounted } from "vue"
import api from "../../services/api"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"

const nama = ref("")
const username = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")

const successMessage = ref("")
const errorMessage = ref("")

async function loadProfile() {
  try {
    const currentUsername =
      sessionStorage.getItem("username")

    const res = await api.get(
      `/auth/profile/${currentUsername}`
    )

    nama.value = res.data.nama
    username.value = res.data.username
    email.value = res.data.email || ""
    phone.value = res.data.phone || ""

  } catch (err) {
    console.error(err)

    errorMessage.value =
      "Gagal mendapatkan maklumat profil."
  }
}

async function saveProfile() {

  successMessage.value = ""
  errorMessage.value = ""

  try {

    await api.put(
      `/auth/profile/${username.value}`,
      {
        nama: nama.value,
        email: email.value,
        phone: phone.value,
        password: password.value || null
      }
    )

    password.value = ""

    successMessage.value =
      "Profil berjaya dikemaskini."

  } catch (err) {

    console.error(err)

    errorMessage.value =
      "Gagal mengemaskini profil."

  }
}

onMounted(loadProfile)
</script>

<template>
  <div>

    <!-- HEADER -->
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>Profil Saya</h2>

        <p class="section-desc">
          Sistem membenarkan pengguna mengemaskini
          maklumat akaun dan kata laluan mereka.
        </p>
      </div>
    </div>

    <!-- FORM CARD -->
    <AppCard class="profile-card">

      <div class="card-header">
        <h3>Maklumat Akaun</h3>
      </div>

      <div class="form-grid">

        <AppInput
          v-model="nama"
          label="Nama"
          placeholder="Masukkan nama"
        />

        <AppInput
          v-model="username"
          label="Nama Pengguna"
          disabled
        />

        <AppInput
          v-model="email"
          label="Emel"
          placeholder="Masukkan emel"
        />

        <AppInput
          v-model="phone"
          label="Telefon"
          placeholder="Masukkan nombor telefon"
        />

        <AppInput
          v-model="password"
          label="Kata Laluan Baru"
          type="password"
          placeholder="Kosongkan jika tidak mahu tukar"
        />

      </div>

      <div
        v-if="successMessage"
        class="success-message"
      >
        {{ successMessage }}
      </div>

      <div
        v-if="errorMessage"
        class="error-message"
      >
        {{ errorMessage }}
      </div>

      <div class="action-bar">
        <AppButton
          text="Simpan Perubahan"
          @click="saveProfile"
        />
      </div>

    </AppCard>

  </div>
</template>

<style scoped>

/* PAGE HEADER */
.hierarchy-card {
  margin-bottom: 20px;
}

.hierarchy-left h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
}

.section-desc {
  margin-top: 8px;
  color: #6b7280;
  max-width: 700px;
  line-height: 1.6;
}

/* CARD */
.profile-card {
  padding: 24px;
}

.card-header {
  margin-bottom: 24px;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

/* FORM */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

/* STATUS */
.success-message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 8px;
  background: #ecfdf5;
  color: #065f46;
  font-size: 14px;
}

.error-message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 8px;
  background: #fef2f2;
  color: #991b1b;
  font-size: 14px;
}

/* BUTTON */
.action-bar {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

/* MOBILE */
@media (max-width: 768px) {

  .form-grid {
    grid-template-columns: 1fr;
  }

}

</style>