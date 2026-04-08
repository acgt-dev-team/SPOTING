<script setup>
import { ref } from "vue"

import logo from "../../assets/images/spoting-logo.png"

import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"

const emit = defineEmits(["back"])

const email = ref("")
const sent = ref(false)

function sendReset(){
  if(email.value){
    sent.value = true
  }
}

function backToLogin(){
  emit("back")
}
</script>

<template>
  <div class="container">

    <img :src="logo" class="logo"/>

    <div class="card">

      <h3 class="title">
        Tetapkan Semula Kata Laluan
      </h3>

      <p class="desc">
        Masukkan emel anda untuk menerima pautan reset kata laluan
      </p>

      <div v-if="!sent">

        <AppInput
          label="Alamat emel"
          v-model="email"
        />

        <AppButton
          text="Hantar pautan reset"
          class="submit-btn"
          @click="sendReset"
        />

        <div class="links">
          <span class="back" @click="backToLogin">
            Kembali ke login
          </span>
        </div>

      </div>

      <div v-else class="success">

        <p class="body">
          Pautan reset telah dihantar ke emel anda.
        </p>

        <AppButton
          text="Kembali ke login"
          @click="backToLogin"
        />

      </div>

    </div>

  </div>
</template>

<style scoped>
.container{
  height:100vh;
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  background:#f3f4f6;
}

.logo{
  width:200px;
  margin-bottom:40px;
}

.card{
  width:360px;
  background:white;
  padding:32px;
  border-radius:12px;
  box-shadow:0 10px 25px rgba(0,0,0,0.08);
  display:flex;
  flex-direction:column;
}

.title{
  font-size:22px;
  font-weight:600;
  margin-bottom:8px;
}

.desc{
  font-size:14px;
  color:#64748b;
  margin-bottom:20px;
}

.submit-btn{
  margin-top:6px;
}

.links{
  margin-top:14px;
  display:flex;
  justify-content:flex-end;
}

.back{
  font-size:12px;
  color:#6366f1;
  cursor:pointer;
}

.back:hover{
  text-decoration:underline;
}

.body{
  font-size:14px;
}

.success{
  text-align:center;
}
</style>