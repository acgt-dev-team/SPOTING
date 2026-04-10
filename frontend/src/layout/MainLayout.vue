<script setup>
import Sidebar from "./Sidebar.vue"
</script>

<template>
  <div class="layout">
    <Sidebar />

    <main class="content">
      <div class="content-inner">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  background: #f4f7fb;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

.content-inner {
  max-width: 1400px;
  margin: 0 auto;
}
</style>