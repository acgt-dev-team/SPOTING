<script setup>
defineProps({
  status: String
})
</script>

<template>

<span :class="['pill', status]">
{{ status }}
</span>

</template>

<style scoped>

.pill{
padding:6px 12px;
border-radius:8px;
font-size:13px;
font-weight:500;
}

.Selesai{
background:#22c55e;
color:white;
}

.Proses{
background:#fde047;
color:black;
}

.Penjadualan{
background:#38bdf8;
color:black;
}

.Belum{
background:#ef4444;
color:white;
}

</style>