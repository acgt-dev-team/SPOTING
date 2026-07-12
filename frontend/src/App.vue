<script setup>
import AppToast from "./ui/AppToast.vue"
</script>

<template>
  <router-view />
  <AppToast />
</template>

<style>
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}
</style>
