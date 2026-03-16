<script setup>
defineProps({
  modelValue: String,
  type: {
    type: String,
    default: "text"
  },
  label: String
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>

<div class="field">

<label>{{ label }}</label>

<input
  :type="type"
  :value="modelValue"
  @input="emit('update:modelValue', $event.target.value)"
/>

</div>

</template>

<style scoped>

.field{
display:flex;
flex-direction:column;
margin-bottom:20px;
}

label{
font-size:14px;
margin-bottom:6px;
color:#333;
}

input{
background:#f1f3f8;
border:1px solid #dcdfe6;
padding:12px;
border-radius:6px;
color:#333;
}

</style>