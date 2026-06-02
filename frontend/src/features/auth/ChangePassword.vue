<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"

const router = useRouter()

const password = ref("")
const confirmPassword = ref("")
const error = ref("")
const loading = ref(false)

async function submit(e) {
  if (e) e.preventDefault()

  error.value = ""

  if (!password.value || !confirmPassword.value) {
    error.value = "Sila isi semua maklumat"
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = "Password tidak sama"
    return
  }

  loading.value = true

  try {

    const username =
      sessionStorage.getItem("username")

    await api.post("/auth/change-password", {
      username,
      password: password.value
    })

    sessionStorage.removeItem(
      "forcePasswordChange"
    )

    const role =
      sessionStorage.getItem("role")

    if (
      role === "admin" ||
      role === "super admin"
    ) {
      router.push("/admin/configuration")
    } else {
      router.push("/admin/dashboard")
    }

  } catch (err) {
    console.error(err)
    error.value =
      "Gagal tukar password"
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">

    <div class="change-wrapper">

      <div class="card">

        <h2 class="title">
          Tukar Kata Laluan
        </h2>

        <p class="desc">
          Anda perlu menukar kata laluan sementara.
        </p>

        <form @submit.prevent="submit">

          <AppInput
            label="Password Baru"
            type="password"
            v-model="password"
          />

          <AppInput
            label="Sahkan Password"
            type="password"
            v-model="confirmPassword"
          />

          <p
            v-if="error"
            class="error"
          >
            {{ error }}
          </p>

          <AppButton
            text="Simpan Password"
            type="button"
            class="submit-btn"
            @click="submit"
          />

        </form>

      </div>

    </div>

  </div>
</template>

<style scoped>
/* PAGE BACKGROUND */
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    linear-gradient(
      135deg,
      #eef2ff,
      #f8fafc
    );
}

/* CENTER WRAPPER */
.change-wrapper {
  width: 100%;
  max-width: 400px;
}

/* CARD */
.card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow:
    0 10px 30px rgba(0,0,0,0.08);
}

/* TITLE */
.title {
  text-align: center;
  margin-bottom: 8px;
  font-weight: 600;
}

/* DESCRIPTION */
.desc {
  text-align: center;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 24px;
  line-height: 1.5;
}

/* BUTTON */
.submit-btn {
  width: 100%;
  margin-top: 15px;
}

/* ERROR */
.error {
  color: red;
  font-size: 12px;
  margin-top: 6px;
}
</style>