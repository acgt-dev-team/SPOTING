<script setup>

const emit = defineEmits(["next","back"])

</script>

<template>

<h2>Isi butiran profil</h2>

<div class="form-group">
<label>Nama profil</label>
<input class="input" placeholder="Masukkan nama profil">
</div>

<div class="form-group">
<label>Jenis penjadualan</label>

<select class="input">
<option>Segera</option>
<option>Berjadual</option>
</select>

</div>

<div class="form-group">
<label>Cronjob</label>
<input class="input" placeholder="*****">
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
padding:10px 12px;
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
cursor:pointer;
}

.outline{
border:1px solid #3b82f6;
background:white;
color:#3b82f6;
padding:10px 18px;
border-radius:8px;
cursor:pointer;
}

</style>