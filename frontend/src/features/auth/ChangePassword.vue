<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services//api"

const router = useRouter()

const password = ref("")
const confirmPassword = ref("")
const error = ref("")

async function submit() {

  error.value = ""

  if (!password.value || !confirmPassword.value) {
    error.value = "Sila isi semua maklumat"
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = "Password tidak sama"
    return
  }

  try {

    const username =
      localStorage.getItem("username")

    await api.post("/auth/change-password", {
      username,
      password: password.value
    })

    localStorage.removeItem(
  "forcePasswordChange"
)

    const role = localStorage.getItem("role")

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
    error.value = "Gagal tukar password"
  }
}
</script>

<template>
  <div class="page">

    <div class="card">

      <h2>Tukar Kata Laluan</h2>

      <p class="desc">
        Anda perlu menukar kata laluan sementara.
      </p>

      <input
        v-model="password"
        type="password"
        placeholder="Password baru"
      />

      <input
        v-model="confirmPassword"
        type="password"
        placeholder="Sahkan password"
      />

      <p v-if="error" class="error">
        {{ error }}
      </p>

      <button @click="submit">
        Simpan Password
      </button>

    </div>
  </div>
</template>

<style scoped>
.page{
  min-height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  background:#f3f4f6;
}

.card{
  width:350px;
  background:white;
  padding:30px;
  border-radius:12px;
}

input{
  width:100%;
  margin-top:12px;
  padding:10px;
}

button{
  width:100%;
  margin-top:16px;
  padding:12px;
}

.error{
  color:red;
  margin-top:10px;
}

.desc{
  margin-bottom:10px;
}
</style>