<template>
  <aside class="w-64 bg-[#070C1F] border-r border-[#121A33] flex flex-col">

    <div class="p-6 text-xl font-bold">
      Spoting
    </div>

    <nav class="flex flex-col gap-2 px-4">

      <RouterLink to="/" class="sidebar-link">Dashboard</RouterLink>

      <RouterLink to="/users" class="sidebar-link">Pengguna</RouterLink>

      <RouterLink to="/organisasi" class="sidebar-link">Organisasi</RouterLink>

      <RouterLink to="/tugasan" class="sidebar-link">Tugasan</RouterLink>

      <RouterLink to="/tetapan" class="sidebar-link">Tetapan</RouterLink>

    </nav>

    <div class="mt-auto p-4 text-sm opacity-70">
      Username
      <div class="text-red-400">Log keluar</div>
    </div>

  </aside>
</template>

<style scoped>

.sidebar-link{
  padding:10px;
  border-radius:8px;
}

.sidebar-link:hover{
  background:#101935;
}

.router-link-active{
  background:#101935;
  color:#c084fc;
}

</style>