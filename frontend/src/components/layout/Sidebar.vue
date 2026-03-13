<script setup>
</script>

<template>
  <aside class="sidebar">

    <h2 class="logo">SPOTING</h2>

    <nav>
      <router-link to="/dashboard">Paparan Muka</router-link>

      <router-link to="/organisasi">Organisasi</router-link>

      <router-link to="/tapak">Tapak</router-link>

      <router-link to="/profil">Profil</router-link>

      <router-link to="/tugasan">Tugasan</router-link>

      <router-link to="/tetapan">Tetapan</router-link>

      <router-link to="/pengguna">Senarai Pengguna</router-link>
    </nav>

  </aside>
</template>

<style scoped>

.sidebar {
  width: 240px;
  height: 100vh;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  padding: 20px;
}

.logo {
  margin-bottom: 30px;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

a {
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 500;
}

.router-link-active {
  color: var(--primary);
}

</style>