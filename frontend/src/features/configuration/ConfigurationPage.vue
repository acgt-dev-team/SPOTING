<script setup>
import AdminLayout from "../../layout/AdminLayout.vue";
import OrganizationPage from "./OrganizationPage.vue"

const breadcrumbs = [{ label: "Organisasi" }]
</script>

<template>
  <AdminLayout :breadcrumbs="breadcrumbs">
    <OrganizationPage />
  </AdminLayout>
</template>