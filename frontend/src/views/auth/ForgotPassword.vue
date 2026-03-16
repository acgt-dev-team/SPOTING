<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

import AppInput from "../../components/ui/AppInput.vue"
import AppButton from "../../components/ui/AppButton.vue"
import AppCard from "../../components/ui/AppCard.vue"

import logo from "../../assets/images/Spoting-logo.png"

const router = useRouter()

const email = ref("")
const sent = ref(false)

function sendReset(){

  if(email.value){
    sent.value = true
  }

}

function backToLogin(){
  router.push("/login")
}

</script>

<template>

<div class="container">

<img :src="logo" class="logo"/>

<AppCard>

<h2 class="title">Tetapkan Semula Kata Laluan</h2>

<p class="desc">
Masukkan emel anda untuk menerima pautan reset kata laluan
</p>

<!-- BEFORE EMAIL SENT -->
<div v-if="!sent">

<AppInput
label="Alamat emel"
v-model="email"
/>

<AppButton
text="Hantar pautan reset"
@click="sendReset"
/>

<button class="back-btn" @click="backToLogin">
Kembali ke login
</button>

</div>

<!-- AFTER EMAIL SENT -->
<div v-else class="success">

<p>Pautan reset telah dihantar ke emel anda.</p>

<AppButton
text="Kembali ke login"
@click="backToLogin"
/>

</div>

</AppCard>

</div>

</template>

<style scoped>

.container{
height:100vh;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
background:#f5f6fa;
}

.logo{
width:180px;
margin-bottom:40px;
}

.title{
font-size:20px;
margin-bottom:10px;
}

.desc{
font-size:14px;
color:#64748b;
margin-bottom:20px;
}

.success{
text-align:center;
}

.back-btn{
margin-top:12px;
background:none;
border:none;
color:#6366f1;
cursor:pointer;
font-size:14px;
}

.back-btn:hover{
text-decoration:underline;
}

</style>