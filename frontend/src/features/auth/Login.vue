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
    const forcePasswordChange =
      res.data.force_password_change

    if(!token){
      throw new Error("Token tidak diterima")
    }

    sessionStorage.setItem("token", token)
    sessionStorage.setItem("role", role)
    sessionStorage.setItem("username", username.value)
    sessionStorage.setItem("forcePasswordChange", forcePasswordChange.toString())
    if (forcePasswordChange) {
  router.push("/change-password")
  return
}

if (
  role === "admin" ||
  role === "super admin"
) {
  router.push("/admin/configuration")
} else if (role === "user") {
  router.push("/admin/dashboard")
}

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.detail ||
      "Login gagal"

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

        <h2 class="title">
          Log Masuk
        </h2>

        <form @submit.prevent="login">

          <AppInput
            label="ID Pengguna"
            v-model="username"
          />

          <AppInput
            label="Kata Laluan"
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
:root{
  --primary:#4F46E5;
  --primary-hover:#4338CA;
  --text:#0F172A;
  --muted:#64748B;
  --border:#E2E8F0;
  --bg:#F8FAFC;
}

.page{
  min-height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:24px;
  background:#F8FAFC;
}

.login-wrapper{
  width:100%;
  max-width:480px;
  text-align:center;
}

.logo{
  width:160px;
  margin-bottom:16px;
}

.card{
  background:white;
  border:1px solid var(--border);
  border-radius:20px;
  padding:32px;
  text-align:left;
  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.eyebrow{
  text-align:center;
  color:var(--primary);
  font-size:12px;
  font-weight:700;
  letter-spacing:.12em;
  margin-bottom:10px;
}

.title{
  text-align:center;
  margin:0 0 36px;
  font-size:30px;
  font-weight:800;
  color:var(--text);
  letter-spacing:-0.02em;
}

.desc{
  text-align:center;
  color:var(--muted);
  font-size:14px;
  margin:12px 0 40px;
  line-height:1.6;
}

form{
  display:flex;
  flex-direction:column;
  gap:18px;
}

.login-btn{
  width:100%;
  margin-top:4px;
}

.error{
  background:#FEF2F2;
  border:1px solid #FECACA;
  color:#DC2626;
  border-radius:12px;
  padding:12px 14px;
  font-size:13px;
  font-weight:600;
}

.links{
  margin-top:18px;
  text-align:center;
}

.forgot{
  font-size:13px;
  color:var(--primary);
  cursor:pointer;
  font-weight:600;
}

.forgot:hover{
  color:var(--primary-hover);
}

@media(max-width:640px){

  .page{
    padding:16px;
  }

  .card{
    padding:24px;
  }

  .title{
    font-size:26px;
  }

  .logo{
    width:140px;
  }

}
</style>