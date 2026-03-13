<script setup>
const emit = defineEmits(["next","back"])
</script>

<template>

<h2>Isi butiran organisasi</h2>

<div class="form-group">
<label>Nama organisasi</label>
<input class="input" placeholder="Masukkan nama organisasi">
</div>

<div class="actions">

<button class="outline" @click="emit('back')">
Kembali
</button>

<button class="primary" @click="emit('next')">
Seterusnya
</button>

</div>

</template>

<style scoped>

.form-group{
margin-bottom:20px;
}

.input{
width:100%;
padding:10px;
border:1px solid #e5e7eb;
border-radius:8px;
}

.actions{
display:flex;
gap:10px;
}

.primary{
background:#9333ea;
color:white;
border:none;
padding:10px 18px;
border-radius:8px;
}

.outline{
border:1px solid #3b82f6;
background:white;
color:#3b82f6;
padding:10px 18px;
border-radius:8px;
}

</style>