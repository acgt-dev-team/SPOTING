<script setup>
import { ref } from "vue"

import WizardLayout from "../../components/wizard/WizardLayout.vue"

import StepUser from "../../components/wizard/StepUser.vue"
import StepOrganization from "../../components/wizard/StepOrganization.vue"
import StepSubOrganization from "../../components/wizard/StepSubOrganization.vue"
import StepSite from "../../components/wizard/StepSite.vue"
import StepProfile from "../../components/wizard/StepProfile.vue"
import StepTask from "../../components/wizard/StepTask.vue"

const step = ref(1)

const steps = [
  StepUser,
  StepOrganization,
  StepSubOrganization,
  StepSite,
  StepProfile,
  StepTask
]

function next() {
  if (step.value < steps.length) step.value++
}

function back() {
  if (step.value > 1) step.value--
}
</script>

<template>
  <WizardLayout :step="step">
    <component
      :is="steps[step - 1]"
      @next="next"
      @back="back"
    />
  </WizardLayout>
</template>