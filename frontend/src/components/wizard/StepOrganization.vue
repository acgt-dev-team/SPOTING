<script setup>
import { ref } from "vue"

import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"

const emit = defineEmits(["next","back"])

const organisasi = ref("")
</script>

<template>

<div class="form">

  <h2 class="title">Isi butiran organisasi</h2>

  <p class="desc">
    Organisasi boleh jadi Pihak Berkuasa Tempatan (PBT) atau agensi
  </p>

  <AppInput
    label="Nama organisasi"
    placeholder="Masukkan nama organisasi"
    v-model="organisasi"
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
      @click="emit('next',{ organisasi })"
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
font-weight:600;
margin-bottom:6px;
}

.desc{
font-size:14px;
color:#64748b;
margin-bottom:24px;
}

.buttons{
display:flex;
gap:12px;
margin-top:10px;
}

</style>