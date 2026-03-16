<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

import logo from "../../assets/images/Spoting-logo.png"

import AppInput from "../../components/ui/AppInput.vue"
import AppButton from "../../components/ui/AppButton.vue"
import AppCard from "../../components/ui/AppCard.vue"

const router = useRouter()

const username = ref("")
const password = ref("")

function login(){

  if(username.value && password.value){
    router.push("/dashboard")
  }

}

function forgotPassword(){
  router.push("/forgot-password")
}

</script>

<template>

<div class="container">

<img :src="logo" class="logo"/>

<AppCard>

<AppInput
label="Nama pengguna"
v-model="username"
/>

<AppInput
label="Kata laluan"
type="password"
v-model="password"
/>

<AppButton
text="Log masuk"
@click="login"
/>

<div class="links">

<span class="forgot" @click="forgotPassword">
Lupa kata laluan
</span>

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

.links{
margin-top:15px;
display:flex;
justify-content:flex-end;
font-size:13px;
}

.forgot{
color:#6366f1;
cursor:pointer;
}

.forgot:hover{
text-decoration:underline;
}

</style>