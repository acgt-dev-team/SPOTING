<script setup>
import { ref } from "vue"

import StepUser from "./StepUser.vue"
import StepOrganization from "./StepOrganization.vue"
import StepSubOrganization from "./StepSubOrganization.vue"
import StepSite from "./StepSite.vue"
import StepProfile from "./StepProfile.vue"
import StepTask from "./StepTask.vue"

const step = ref(1)

const steps = [
  StepUser,
  StepOrganization,
  StepSubOrganization,
  StepSite,
  StepProfile,
  StepTask
]

const labels = [
  "Pengguna",
  "Organisasi",
  "Sub organisasi",
  "Tapak",
  "Profil",
  "Tugasan"
]

function next() {
  if (step.value < steps.length) {
    step.value++
  }
}

function back() {
  if (step.value > 1) {
    step.value--
  }
}
</script>

<template>

<div class="wizard-container">

<h1 class="title">Pendaftaran</h1>

<div class="wizard-card">

  <div class="progress">

    <div
      v-for="(label,index) in labels"
      :key="index"
      class="step"
    >

      <div
        class="circle"
        :class="{
          active: step === index + 1,
          done: step > index + 1
        }"
      >
        {{ index + 1 }}
      </div>

      <div class="label">
        {{ label }}

        <span
          v-if="step > index + 1"
          class="done-text"
        >
          Selesai
        </span>

      </div>

    </div>

  </div>

  <div class="divider"></div>

  <div class="content">

    <component
      :is="steps[step - 1]"
      @next="next"
      @back="back"
    />

  </div>

</div>

</div>

</template>

<style scoped>

.wizard-container{
  background:#f7f9fc;
  min-height:100vh;
  padding:40px;
}

.title{
  margin-bottom:20px;
}

.wizard-card{
  background:white;
  border-radius:16px;
  padding:40px;

  display:flex;
  gap:30px;

  box-shadow:0 10px 25px rgba(0,0,0,0.05);
}

.progress{
  width:200px;
}

.step{
  display:flex;
  align-items:center;
  margin-bottom:20px;
}

.circle{
  width:32px;
  height:32px;

  border-radius:50%;

  border:2px solid #3b82f6;

  display:flex;
  align-items:center;
  justify-content:center;

  margin-right:10px;
}

.active{
  border-color:#9333ea;
  color:#9333ea;
}

.done{
  border-color:#22c55e;
  color:#22c55e;
}

.done-text{
  font-size:12px;
  margin-left:6px;
  color:#22c55e;
}

.divider{
  width:1px;
  background:#e5e7eb;
}

.content{
  flex:1;
}

</style>