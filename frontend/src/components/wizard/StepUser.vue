<script setup>
const emit = defineEmits(["next"])
</script>

<template>

<h2>Isi butiran pengguna</h2>

<div class="form-group">
<label>Nama pelanggan</label>
<input class="input" placeholder="Masukkan nama pelanggan">
</div>

<button class="primary" @click="emit('next')">
Seterusnya
</button>

</template>

<style scoped>

.form-group{
margin-bottom:20px;
}

.input{
width:100%;
padding:10px 12px;
border:1px solid #e5e7eb;
border-radius:8px;
}

.primary{
background:#9333ea;
color:white;
border:none;
padding:10px 18px;
border-radius:8px;
cursor:pointer;
}

</style>