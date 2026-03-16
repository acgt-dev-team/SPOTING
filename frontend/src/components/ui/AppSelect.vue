<script setup>
defineProps({
  label: String,
  options: Array,
  modelValue: String
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>

<div class="field">

<label>{{ label }}</label>

<select
:value="modelValue"
@change="emit('update:modelValue',$event.target.value)"
>

<option disabled value="">Pilih</option>

<option
v-for="opt in options"
:key="opt"
:value="opt"
>
{{ opt }}
</option>

</select>

</div>

</template>

<style scoped>

.field{
display:flex;
flex-direction:column;
gap:6px;
}

label{
font-size:13px;
color:#374151;
}

select{
height:40px;
border-radius:8px;
border:1px solid #e5e7eb;
background:white;
padding:0 10px;
}

</style>