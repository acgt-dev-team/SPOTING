<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import logo from "../../assets/images/spoting-logo.png"

const router = useRouter()

const username = ref("")
const password = ref("")

function login() {

  // TEMP login
  if(username.value && password.value){
    router.push("/dashboard")
  }

}

function goRegister(){
  router.push("/register")
}

</script>

<template>

<div class="container">

<img :src="logo" class="logo"/>

<div class="form">

<label>Nama pengguna</label>
<input v-model="username" type="text">

<label>Kata laluan</label>
<input v-model="password" type="password">

<button class="login-btn" @click="login">
Log masuk
</button>

<div class="links">

<span>Lupa kata laluan</span>

<span class="register" @click="goRegister">
Daftar baru
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
background:#02071c;
color:white;
}

.logo{
width:180px;
margin-bottom:40px;
}

.form{
width:320px;
display:flex;
flex-direction:column;
}

label{
font-size:14px;
margin-bottom:6px;
color:#d0d6ff;
}

input{
background:#1b223f;
border:none;
padding:12px;
border-radius:6px;
margin-bottom:20px;
color:white;
}

.login-btn{
margin-top:10px;
padding:12px;
border:none;
border-radius:6px;
background:linear-gradient(90deg,#8b2cff,#d12bff);
color:white;
font-weight:600;
cursor:pointer;
}

.links{
margin-top:15px;
display:flex;
justify-content:space-between;
font-size:13px;
color:#b9c2ff;
}

.register{
cursor:pointer;
}

</style>