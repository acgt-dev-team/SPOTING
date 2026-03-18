<script setup>
import { ref } from "vue"

import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"
import AppSelect from "../ui/AppSelect.vue"

const emit = defineEmits(["next","back"])

const profil = ref("")
const jadual = ref("Segera")
const cronjob = ref("")
</script>

<template>

<div class="form">

  <h2 class="title">Isi butiran profil</h2>

  <div class="fields">

    <AppInput
      label="Nama profil"
      placeholder="Masukkan nama profil"
      v-model="profil"
    />

    <AppSelect
      label="Jenis penjadualan"
      :options="['Segera']"
      v-model="jadual"
    />

    <AppInput
      label="Cronjob"
      placeholder="Masukkan cronjob"
      v-model="cronjob"
    />

  </div>

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
      @click="emit('next',{ profil, cronjob })"
    />

  </div>

</div>

</template>

<style scoped>

.form{
max-width:460px; /* tighter like design */
}

.title{
font-size:22px;
font-weight:600;
margin-bottom:24px;
}

.fields{
display:flex;
flex-direction:column;
gap:16px; /* 🔥 tighter spacing */
}

.buttons{
display:flex;
gap:12px;
margin-top:20px;
}

</style>