<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import logo from "../../assets/images/spoting-logo.png"

const router = useRouter()

const nama = ref("")
const username = ref("")
const emel = ref("")
const organisasi = ref("")
const password = ref("")
const confirm = ref("")

function submit(){
  console.log("Register user")
}

function cancel(){
  router.push("/")
}

</script>

<template>

<div class="container">

<img :src="logo" class="logo"/>

<div class="form">

<div class="grid">

<div>
<label>Nama</label>
<input v-model="nama">
</div>

<div>
<label>Nama pengguna</label>
<input v-model="username">
</div>

<div>
<label>Emel</label>
<input v-model="emel">
</div>

<div>
<label>Organisasi</label>
<select v-model="organisasi">
<option>Pilih di sini</option>
<option>Organisasi A</option>
<option>Organisasi B</option>
</select>
</div>

<div>
<label>Kata laluan</label>
<input type="password" v-model="password">
</div>

<div>
<label>Sahkan kata laluan</label>
<input type="password" v-model="confirm">
</div>

</div>

<div class="buttons">

<button class="cancel" @click="cancel">
Batal
</button>

<button class="submit" @click="submit">
Hantar
</button>

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
margin-bottom:30px;
}

.form{
width:650px;
}

.grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:20px;
}

label{
font-size:14px;
margin-bottom:6px;
display:block;
color:#d0d6ff;
}

input,select{
width:100%;
background:#1b223f;
border:none;
padding:12px;
border-radius:6px;
color:white;
}

.buttons{
margin-top:30px;
display:flex;
gap:15px;
}

.cancel{
background:transparent;
border:1px solid #3aa0ff;
color:#3aa0ff;
padding:10px 20px;
border-radius:6px;
cursor:pointer;
}

.submit{
background:linear-gradient(90deg,#8b2cff,#d12bff);
border:none;
padding:10px 20px;
border-radius:6px;
color:white;
cursor:pointer;
}

</style>