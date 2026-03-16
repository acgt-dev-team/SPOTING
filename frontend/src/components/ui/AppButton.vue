<script setup>
defineProps({
  text: String
})
</script>

<template>

<button class="btn">
  {{ text }}
</button>

</template>

<style scoped>

.btn{
margin-top:10px;
padding:12px;
border:none;
border-radius:6px;
background:linear-gradient(90deg,#8b2cff,#d12bff);
color:white;
font-weight:600;
cursor:pointer;
width:100%;
}

</style>