<script setup>
defineProps({
  modelValue: String,
  placeholder: String
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>

<div class="search">

<span class="icon">🔍</span>

<input
:type="text"
:placeholder="placeholder"
:value="modelValue"
@input="emit('update:modelValue',$event.target.value)"
/>

</div>

</template>

<style scoped>

.search{
display:flex;
align-items:center;
border:1px solid #e5e7eb;
border-radius:8px;
padding:8px 10px;
background:white;
}

.icon{
margin-right:8px;
color:#6b7280;
}

input{
border:none;
outline:none;
width:100%;
}

</style>