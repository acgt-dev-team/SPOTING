<script setup>
defineProps({
  value: Number,
  label: String,
  color: String
})
</script>

<template>

<div class="card">

<div class="value" :style="{color:color}">
{{ value }}
</div>

<div class="label">
{{ label }}
</div>

</div>

</template>

<style scoped>

.card{
background:white;
padding:20px;
border-radius:12px;
width:140px;
text-align:center;
border:1px solid #e5e7eb;
box-shadow:0 4px 12px rgba(0,0,0,0.05);
}

.value{
font-size:30px;
font-weight:600;
}

.label{
font-size:12px;
color:#6b7280;
}

</style>