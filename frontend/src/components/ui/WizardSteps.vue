<script setup>

defineProps({
  steps: Array,
  current: Number
})

</script>

<template>

<div class="steps">

<div
v-for="(s,i) in steps"
:key="i"
:class="['step',{active:i+1===current,done:i+1<current}]"
>

<span class="circle">{{ i+1 }}</span>
<span class="label">{{ s }}</span>

</div>

</div>

</template>

<style scoped>

.steps{
display:flex;
gap:24px;
}

.step{
display:flex;
align-items:center;
gap:8px;
color:#6b7280;
}

.circle{
width:28px;
height:28px;
border-radius:50%;
border:2px solid #3b82f6;
display:flex;
align-items:center;
justify-content:center;
font-size:13px;
}

.active{
color:#9333ea;
}

.done{
color:#22c55e;
}

</style>