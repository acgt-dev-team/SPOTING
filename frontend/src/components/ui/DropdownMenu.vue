<script setup>
const emit = defineEmits(["copy","edit","delete"])
</script>

<template>

<div class="menu">

<div @click="emit('copy')">Salin</div>
<div @click="emit('edit')">Kemaskini</div>
<div class="delete" @click="emit('delete')">Padam</div>

</div>

</template>

<style scoped>

.menu{
background:white;
border:1px solid #e5e7eb;
border-radius:8px;
width:140px;
padding:8px;
display:flex;
flex-direction:column;
gap:6px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
}

.menu div{
padding:6px 10px;
cursor:pointer;
}

.menu div:hover{
background:#f3f4f6;
border-radius:6px;
}

.delete{
color:#ef4444;
}

</style>