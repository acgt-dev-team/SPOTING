<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

import logo from "../../assets/images/Spoting-logo.png"

import AppInput from "../../components/ui/AppInput.vue"
import AppButton from "../../components/ui/AppButton.vue"

const router = useRouter()

const username = ref("")
const password = ref("")

function login(){

  if(username.value && password.value){

    // temporary login state
    localStorage.setItem("token","loggedin")

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

<div class="card">

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
class="login-btn"
@click="login"
/>

<div class="links">

<span class="forgot" @click="forgotPassword">
Lupa kata laluan
</span>

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

.login-btn{
margin-top:6px;
}

.links{
margin-top:14px;
display:flex;
justify-content:flex-end;
}

.forgot{
font-size:12px;
color:#6366f1;
cursor:pointer;
}

.forgot:hover{
text-decoration:underline;
}

</style>