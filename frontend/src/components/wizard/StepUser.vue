<script setup>
import { ref } from "vue"

const pelanggan = ref("")
</script>

<template>

<div>

<h2 class="title">Isi butiran pengguna</h2>

<label>Nama pelanggan</label>

<input
  v-model="pelanggan"
  class="input"
/>

<button
  class="next"
  @click="$emit('next')"
>
Seterusnya
</button>

</div>

</template>

<style scoped>

.title{
font-size:20px;
margin-bottom:24px;
}

.input{
width:100%;
padding:12px;
border-radius:8px;
border:1px solid #e5e7eb;
margin-top:8px;
margin-bottom:24px;
}

.next{
background:#a855f7;
color:white;
padding:10px 24px;
border:none;
border-radius:8px;
font-weight:500;
}

</style>