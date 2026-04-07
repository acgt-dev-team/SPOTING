<script setup>
import ConfigurationLayout from "./ConfigurationLayout.vue"
import OrganizationPage from "./OrganizationPage.vue"

const breadcrumbs = [{ label: "Organisasi" }]
</script>

<template>
  <ConfigurationLayout :breadcrumbs="breadcrumbs">
    <OrganizationPage />
  </ConfigurationLayout>
</template>