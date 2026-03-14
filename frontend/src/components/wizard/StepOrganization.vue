<script setup>
import { ref } from "vue"

const organisasi = ref("")
</script>

<template>

<div class="form">

<h2 class="title">Isi butiran organisasi</h2>

<p class="desc">
Organisasi boleh jadi Pihak Berkuasa Tempatan (PBT) atau agensi
</p>

<div class="field">
<label>Nama organisasi</label>

<input
v-model="organisasi"
class="input"
placeholder="Masukkan nama organisasi"
/>
</div>

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

/* your original CSS unchanged */

.form{
max-width:520px;
}

.title{
font-size:22px;
font-weight:600;
margin-bottom:6px;
}

.desc{
font-size:14px;
color:#64748b;
margin-bottom:28px;
}

.field{
margin-bottom:28px;
}

label{
font-size:14px;
font-weight:500;
display:block;
margin-bottom:8px;
}

.input{
width:100%;
height:44px;
padding:0 14px;
border-radius:8px;
border:1px solid #e5e7eb;
font-size:14px;
transition:all 0.15s ease;
}

.input:focus{
outline:none;
border-color:#a855f7;
box-shadow:0 0 0 2px rgba(168,85,247,0.15);
}

.buttons{
display:flex;
gap:14px;
margin-top:10px;
}

.back{
background:white;
border:1px solid #3b82f6;
color:#3b82f6;
padding:10px 22px;
border-radius:8px;
font-size:14px;
cursor:pointer;
}

.next{
background:#a855f7;
color:white;
padding:10px 22px;
border:none;
border-radius:8px;
font-size:14px;
cursor:pointer;
}

.next:hover{
background:#9333ea;
}

</style>