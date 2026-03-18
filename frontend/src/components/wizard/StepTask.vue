<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { submitWizard } from "../../services/wizardService"

import AppInput from "../ui/AppInput.vue"
import AppButton from "../ui/AppButton.vue"
import AppSelect from "../ui/AppSelect.vue"

const router = useRouter()

const emit = defineEmits(["back"])

const props = defineProps({
  wizardData: Object
})

const namaTugasan = ref("")
const jenisTugasan = ref("")
const protocol = ref("v4")
const ipStart = ref("")
const ipEnd = ref("")

async function submitWizardData() {
  const payload = {
    ...props.wizardData,
    task_name: namaTugasan.value,
    task_type: jenisTugasan.value,
    protocol: protocol.value,
    ip_start: ipStart.value,
    ip_end: ipEnd.value
  }

  try {
    await submitWizard(payload)
    localStorage.setItem("wizardCompleted","true")
    router.push("/login")
  } catch (error) {
    console.error(error)
    alert("Wizard setup failed")
  }
}
</script>

<template>

<div class="form">

  <h2 class="title">Isi butiran tugasan</h2>

  <!-- Row 1 -->
  <div class="grid">

    <AppInput
      label="Nama tugasan"
      placeholder="Masukkan nama tugasan"
      v-model="namaTugasan"
    />

    <div>
      <div class="label-row">
        <span class="label">Jenis tugasan</span>
        <span class="link">Tambah jenis</span>
      </div>

      <AppSelect
        :options="['Pilih disini']"
        v-model="jenisTugasan"
      />
    </div>

  </div>

  <!-- Row 2 -->
  <div class="grid">

    <div>
      <label class="label">Jenis protocol</label>

      <div class="radio-group">
        <label class="radio">
          <input type="radio" value="v4" v-model="protocol"/>
          <span>v4</span>
        </label>

        <label class="radio">
          <input type="radio" value="v6" v-model="protocol"/>
          <span>v6</span>
        </label>
      </div>
    </div>

    <div>
      <label class="label">Julat alamat IP</label>

      <div class="ip-range">

        <AppInput
          placeholder="IP mula"
          v-model="ipStart"
        />

        <span class="dash">-</span>

        <AppInput
          placeholder="IP akhir"
          v-model="ipEnd"
        />

      </div>
    </div>

  </div>

  <div class="buttons">

    <AppButton
      text="Kembali"
      variant="outline"
      :full="false"
      @click="emit('back')"
    />

    <AppButton
      text="Hantar"
      :full="false"
      @click="submitWizardData"
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
margin-bottom:24px;
}

.grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:20px; /* 🔥 tighter & cleaner */
margin-bottom:20px;
}

.label{
font-size:13px;
color:#374151;
}

.label-row{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:6px;
}

.link{
font-size:13px;
color:#a855f7;
cursor:pointer;
}

.radio-group{
display:flex;
gap:16px;
margin-top:8px;
}

.radio{
display:flex;
align-items:center;
gap:6px;
}

.ip-range{
display:flex;
align-items:center;
gap:10px;
margin-top:6px;
}

.dash{
color:#94a3b8;
}

.buttons{
display:flex;
gap:12px;
margin-top:16px;
}

</style>