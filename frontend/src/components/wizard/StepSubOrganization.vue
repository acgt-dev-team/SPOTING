<script setup>
import { ref } from "vue"

const subOrganisasi = ref("")
</script>

<template>

<div>

<h2 class="title">Isi butiran sub organisasi</h2>

<p class="desc">
Unit di dalam organisasi
</p>

<label>Nama sub organisasi</label>

<input 
  v-model="subOrganisasi" 
  class="input"
  placeholder="Masukkan nama sub organisasi"
/>

<div class="buttons">

<button class="back" @click="$emit('back')">
Kembali
</button>

<button class="next" @click="$emit('next')">
Seterusnya
</button>

</div>

</div>

</template>

<style scoped>

.title{
font-size:20px;
margin-bottom:8px;
}

.desc{
font-size:14px;
color:#64748b;
margin-bottom:20px;
}

.input{
width:100%;
padding:12px;
border-radius:8px;
border:1px solid #e5e7eb;
margin-top:8px;
margin-bottom:24px;
}

.buttons{
display:flex;
gap:12px;
}

.back{
background:white;
border:1px solid #3b82f6;
color:#3b82f6;
padding:10px 24px;
border-radius:8px;
}

.next{
background:#a855f7;
color:white;
padding:10px 24px;
border:none;
border-radius:8px;
}

</style>