<script setup>
import { ref } from "vue"

import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"

const emit = defineEmits(["next","back"])

const subOrganisasi = ref("")
</script>

<template>

<div class="form">

  <h2 class="title">Isi butiran sub organisasi</h2>

  <p class="desc">
    Unit di dalam organisasi
  </p>

  <AppInput
    label="Nama sub organisasi"
    placeholder="Masukkan nama sub organisasi"
    v-model="subOrganisasi"
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
      @click="emit('next',{ sub_organisasi: subOrganisasi })"
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
margin-bottom:6px;
}

.desc{
font-size:14px;
color:#64748b;
margin-bottom:20px;
}

.buttons{
display:flex;
gap:12px;
}

</style>