<script setup>

defineProps({
  text: String,
  variant: {
    type: String,
    default: "primary"
  },
  full: {
    type: Boolean,
    default: true
  }
})

</script>

<template>

<button
:class="['btn', variant, { full }]"
>
{{ text }}
</button>

</template>

<style scoped>

.btn{
padding:12px 16px;
border-radius:8px;
font-size:14px;
cursor:pointer;
border:none;
}

.full{
width:100%;
}

.primary{
background:linear-gradient(90deg,#8b2cff,#d12bff);
color:white;
}

.outline{
background:white;
border:1px solid #3b82f6;
color:#3b82f6;
}

.secondary{
background:#9333ea;
color:white;
}

.link{
background:none;
color:#9333ea;
text-decoration:underline;
padding:0;
}

</style>