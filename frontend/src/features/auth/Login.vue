<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"

import logo from "../../assets/images/spoting-logo.png"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"

const router = useRouter()

const username = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

async function login(e){
  if (e) e.preventDefault()

  error.value = ""

  if(!username.value || !password.value){
    error.value = "Sila isi semua maklumat"
    return
  }

  loading.value = true

  try {
    const res = await api.post("/auth/login", {
      username: username.value,
      password: password.value
    })

    const token = res.data.access_token
    const role = res.data.role || "user"

    if(!token){
      throw new Error("Token tidak diterima")
    }

    localStorage.setItem("token", token)
    localStorage.setItem("role", role)

    if(role === "admin"){
      router.push("/admin/configuration")
    } else {
      router.push("/app/profil")
    }

  } catch (err) {
    console.error("Login error:", err)

    if (
      err.response?.status === 401 ||
      err.response?.status === 400
    ) {
      error.value = "Nama pengguna atau kata laluan tidak sah"
    } else {
      error.value = "Login gagal"
    }

  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">

    <div class="login-wrapper">

      <img :src="logo" class="logo"/>

      <div class="card">

        <h2 class="title">Log masuk</h2>

        <form @submit.prevent="login">

          <AppInput
            label="Nama pengguna"
            v-model="username"
          />

          <AppInput
            label="Kata laluan"
            type="password"
            v-model="password"
          />

          <p v-if="error" class="error">{{ error }}</p>

          <AppButton
            text="Log masuk"
            type="button"
            class="login-btn"
            @click="login"
          />

        </form>

        <div class="links">
          <span class="forgot">
            Lupa kata laluan
          </span>
        </div>

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
  background: linear-gradient(135deg, #eef2ff, #f8fafc);
}

/* CENTER WRAPPER */
.login-wrapper {
  width: 100%;
  max-width: 400px;
  text-align: center;
}

/* LOGO */
.logo {
  width: 140px;
  margin-bottom: 20px;
}

/* CARD */
.card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  text-align: left;
}

/* TITLE */
.title {
  text-align: center;
  margin-bottom: 20px;
  font-weight: 600;
}

/* BUTTON */
.login-btn {
  width: 100%;
  margin-top: 15px;
}

/* ERROR */
.error {
  color: red;
  font-size: 12px;
  margin-top: 6px;
}

/* LINKS */
.links {
  margin-top: 12px;
  text-align: center;
}

.forgot {
  font-size: 13px;
  color: #6366f1;
  cursor: pointer;
}

.forgot:hover {
  text-decoration: underline;
}
</style>