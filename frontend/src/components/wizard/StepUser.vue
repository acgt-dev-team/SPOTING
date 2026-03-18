<script setup>
import { ref } from "vue"

import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"

const emit = defineEmits(["next"])

const pelanggan = ref("")
</script>

<template>

<div class="form">

  <h2 class="title">Isi butiran pengguna</h2>

  <AppInput
    label="Nama pelanggan"
    placeholder="Masukkan nama pelanggan"
    v-model="pelanggan"
  />

  <AppButton
    text="Seterusnya"
    :full="false"
    @click="emit('next',{ pelanggan })"
  />

</div>

</template>

<style scoped>

.form{
max-width:520px;
}

.title{
font-size:22px;
margin-bottom:20px;
}

</style>