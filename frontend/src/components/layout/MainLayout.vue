<template>
  <div class="flex h-screen bg-[#060B1A] text-white">
    
    <!-- Sidebar -->
    <Sidebar />

    <!-- Content -->
    <div class="flex flex-col flex-1">

      <Topbar />

      <main class="p-8 overflow-y-auto flex-1">
        <router-view />
      </main>

    </div>

  </div>
</template>

<script setup>
import Sidebar from "./Sidebar.vue"
import Topbar from "./Topbar.vue"
</script>