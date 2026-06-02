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

        <p class="eyebrow">
          KESELAMATAN AKAUN
        </p>

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
            text="Simpan Kata Laluan"
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

.change-wrapper{
  width:100%;
  max-width:480px;
}

.card{
  background:white;
  border:1px solid var(--border);
  border-radius:20px;
  padding:32px;
  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.title{
  margin:0;
  text-align:center;
  font-size:28px;
  font-weight:800;
  color:var(--text);
  letter-spacing:-0.02em;
}

.desc{
  text-align:center;
  font-size:14px;
  color:var(--muted);
  margin:12px 0 28px;
  line-height:1.6;
}

form{
  display:flex;
  flex-direction:column;
  gap:18px;
}

.submit-btn{
  width:100%;
  margin-top:6px;
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

.eyebrow{
  text-align:center;
  color:#4F46E5;
  font-size:12px;
  font-weight:700;
  letter-spacing:.12em;
  margin-bottom:12px;
}

@media(max-width:640px){

  .page{
    padding:16px;
  }

  .card{
    padding:24px;
  }

  .title{
    font-size:24px;
  }

}
</style>