<script setup>
import { ref } from "vue"

import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"

const emit = defineEmits(["next","back"])

const tapak = ref("")
</script>

<template>

<div class="form">

  <h2 class="title">Isi butiran tapak</h2>

  <AppInput
    label="Nama tapak"
    placeholder="Masukkan nama tapak"
    v-model="tapak"
  />

  <div class="buttons">

    <AppButton
      text="Kembali"
      variant="outline"
      :full="false"
      @click="emit('back')"
    />

    <AppButton
      text="Seterusnya"
      :full="false"
      @click="emit('next',{ tapak })"
    />

  </div>

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

.buttons{
display:flex;
gap:12px;
}

</style>