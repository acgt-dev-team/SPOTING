<script setup>
defineProps({
  modelValue: String,
  label: String,
  placeholder: String,
  type: {
    type: String,
    default: "text"
  }
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>

<div class="field">

<label v-if="label" class="label">
{{ label }}
</label>

<input
:type="type"
:placeholder="placeholder"
:value="modelValue"
@input="emit('update:modelValue',$event.target.value)"
/>

</div>

</template>

<style scoped>

.field{
display:flex;
flex-direction:column;
gap:6px;
margin-bottom:18px;
}

.label{
font-size:12px;
color:#6b7280;
}

input{
height:44px;
padding:0 12px;
border-radius:8px;
border:1px solid #d1d5db;
background:white;
font-size:14px;
}

input:focus{
outline:none;
border-color:#a855f7;
box-shadow:0 0 0 2px rgba(168,85,247,0.15);
}

</style>