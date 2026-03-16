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
background:#f5f6fa;
color:#1b223f;
}

.logo{
width:180px;
margin-bottom:40px;
}

.form{
width:320px;
display:flex;
flex-direction:column;
background:white;
padding:30px;
border-radius:10px;
box-shadow:0 4px 20px rgba(0,0,0,0.08);
}

label{
font-size:14px;
margin-bottom:6px;
color:#333;
}

input{
background:#f1f3f8;
border:1px solid #dcdfe6;
padding:12px;
border-radius:6px;
margin-bottom:20px;
color:#333;
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
justify-content:flex-end;
font-size:13px;
color:#666;
}

</style>