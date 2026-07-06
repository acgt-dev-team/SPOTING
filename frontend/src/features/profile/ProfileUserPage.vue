<script setup>
import { ref, onMounted } from "vue"
import api from "../../services/api"
import { t } from "../../i18n"

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

    errorMessage.value = t("profileUser.errorLoad")
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

    successMessage.value = t("profileUser.successSave")

  } catch (err) {

    console.error(err)

    errorMessage.value = t("profileUser.errorSave")

  }
}

onMounted(loadProfile)
</script>

<template>
  <div>

    <!-- HEADER -->
    <div class="hierarchy-card">
      <div class="hierarchy-left">
        <h2>{{ t("profileUser.title") }}</h2>

        <p class="section-desc">
          {{ t("profileUser.description") }}
        </p>
      </div>
    </div>

    <!-- FORM CARD -->
    <AppCard class="profile-card">

      <div class="card-header">
        <p class="eyebrow">{{ t("profileUser.eyebrow") }}</p>
        <h3>{{ t("profileUser.accountInfo") }}</h3>
      </div>

      <div class="form-grid">

        <AppInput
          v-model="nama"
          :label="t('common.name')"
          :placeholder="t('profileUser.namePlaceholder')"
        />

        <AppInput
          v-model="username"
          :label="t('auth.username')"
          disabled
        />

        <AppInput
          v-model="email"
          :label="t('profileUser.email')"
          :placeholder="t('profileUser.emailPlaceholder')"
        />

        <AppInput
          v-model="phone"
          :label="t('profileUser.phone')"
          :placeholder="t('profileUser.phonePlaceholder')"
        />

        <AppInput
          v-model="password"
          :label="t('profileUser.newPassword')"
          type="password"
          :placeholder="t('profileUser.passwordPlaceholder')"
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
          :text="t('common.saveChanges')"
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

.eyebrow{
  color:#4F46E5;
  font-size:12px;
  letter-spacing:.12em;
  font-weight:700;
  margin-bottom:8px;
}

/* CARD */
:root{
  --primary:#4F46E5;
  --primary-soft:#EEF2FF;
  --text:#0F172A;
  --muted:#64748B;
  --border:#E2E8F0;
  --bg:#F8FAFC;
}

/* HEADER */

.hierarchy-card{
  background:white;
  border:1px solid var(--border);
  border-radius:20px;
  padding:32px;
  margin-bottom:32px;
  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.hierarchy-left h2{
  margin:0;
  font-size:32px;
  font-weight:800;
  color:var(--text);
}

.section-desc{
  margin-top:8px;
  color:var(--muted);
  font-size:15px;
  line-height:1.6;
  max-width:720px;
}

/* CARD */

.profile-card{
  padding:32px !important;
  border-radius:20px;
  border:1px solid var(--border);
  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.card-header{
  margin-bottom:28px;
}

.card-header h3{
  margin:0;
  font-size:22px;
  font-weight:800;
  color:var(--text);
}

/* FORM */

.form-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:20px;
}

/* SUCCESS */

.success-message{
  margin-top:24px;
  padding:14px 16px;
  border-radius:14px;
  background:#ECFDF5;
  border:1px solid #BBF7D0;
  color:#166534;
  font-size:14px;
  font-weight:600;
}

/* ERROR */

.error-message{
  margin-top:24px;
  padding:14px 16px;
  border-radius:14px;
  background:#FEF2F2;
  border:1px solid #FECACA;
  color:#B91C1C;
  font-size:14px;
  font-weight:600;
}

/* ACTIONS */

.action-bar{
  margin-top:32px;
  padding-top:24px;
  border-top:1px solid #F1F5F9;
  display:flex;
  justify-content:flex-end;
}

/* MOBILE */

@media(max-width:768px){

  .form-grid{
    grid-template-columns:1fr;
  }

  .profile-card{
    padding:24px !important;
  }

  .hierarchy-card{
    padding:24px;
  }

  .hierarchy-left h2{
    font-size:28px;
  }

}
</style>
