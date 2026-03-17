<script setup>
import Sidebar from "./Sidebar.vue"
</script>

<template>

<div class="layout">

  <Sidebar />

  <main class="content">
    <router-view />
  </main>

</div>

</template>

<style scoped>

.layout{
  display:flex;
  height:100vh;
  background:#f5f7fb;
}

.content{
  flex:1;
  padding:40px;
  overflow:auto;
}

</style>