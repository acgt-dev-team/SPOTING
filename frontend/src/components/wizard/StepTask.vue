<script setup>

const emit = defineEmits(["back"])

</script>

<template>

<h2>Isi butiran tugasan</h2>

<div class="form-group">
<label>Nama tugasan</label>
<input class="input" placeholder="Masukkan nama tugasan">
</div>

<div class="form-group">
<label>Jenis tugasan</label>

<select class="input">
<option>Pilih disini</option>
</select>

</div>

<div class="form-group">
<label>Jenis protocol</label>

<div class="radio-group">
<label><input type="radio" name="protocol"> v4</label>
<label><input type="radio" name="protocol"> v6</label>
</div>

</div>

<div class="form-group">

<label>Julat alamat IP</label>

<div class="range">

<input class="input">

<span>-</span>

<input class="input">

</div>

</div>

<div class="actions">

<button class="outline" @click="emit('back')">
Kembali
</button>

<button class="primary">
Hantar
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

.radio-group{
display:flex;
gap:20px;
}

.range{
display:flex;
gap:10px;
align-items:center;
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