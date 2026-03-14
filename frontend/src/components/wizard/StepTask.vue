<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { submitWizard } from "../../services/wizardService"

const router = useRouter()

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

<div>

<h2 class="title">Isi butiran tugasan</h2>

<!-- Row 1 -->
<div class="grid">

<div>
<label>Nama tugasan</label>
<input 
  v-model="namaTugasan" 
  class="input"
  placeholder="Masukkan nama tugasan"
/>
</div>

<div>

<div class="label-row">
<label>Jenis tugasan</label>
<a class="link">Tambah jenis</a>
</div>

<select v-model="jenisTugasan" class="input">
<option>Pilih disini</option>
</select>

</div>

</div>

<!-- Row 2 -->
<div class="grid">

<div>

<label>Jenis protocol</label>

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

<label>Julat alamat IP</label>

<div class="ip-range">

<input 
  v-model="ipStart" 
  class="input"
  placeholder="IP mula"
/>

<span class="dash">-</span>

<input 
  v-model="ipEnd" 
  class="input"
  placeholder="IP akhir"
/>

</div>

</div>

</div>

<!-- Buttons -->
<div class="buttons">

<button class="back" @click="$emit('back')">
Kembali
</button>

<button class="next" @click="submitWizardData">
Hantar
</button>

</div>

</div>

</template>

<style scoped>

.title{
font-size:20px;
margin-bottom:24px;
}

.grid{
display:grid;
grid-template-columns:1fr 1fr;
column-gap:40px;
row-gap:28px;
margin-bottom:28px;
}

.label-row{
display:flex;
justify-content:space-between;
align-items:center;
}

.link{
font-size:14px;
color:#a855f7;
cursor:pointer;
}

.input{
width:100%;
padding:12px;
border-radius:8px;
border:1px solid #e5e7eb;
margin-top:8px;
}

.radio-group{
display:flex;
gap:24px;
margin-top:10px;
}

.radio{
display:flex;
align-items:center;
gap:6px;
}

.ip-range{
display:flex;
align-items:center;
gap:16px;
margin-top:8px;
}

.dash{
color:#94a3b8;
}

.buttons{
display:flex;
gap:12px;
margin-top:20px;
}

.back{
background:white;
border:1px solid #3b82f6;
color:#3b82f6;
padding:10px 24px;
border-radius:8px;
}

.next{
background:#a855f7;
color:white;
padding:10px 24px;
border:none;
border-radius:8px;
cursor:pointer;
}

</style>