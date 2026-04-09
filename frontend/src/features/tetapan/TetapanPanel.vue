<script setup>
const taskTypes = [
  { no: 1, nama: "Windows client" },
  { no: 2, nama: "Mac client" },
  { no: 3, nama: "Linux client" },
  { no: 4, nama: "Peranti rangkaian" }
]
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <p class="eyebrow">KONFIGURASI</p>
        <h1 class="title">Tetapan</h1>
        <p class="subtitle">Urus tetapan asas sistem dan pilihan pengguna.</p>
      </div>
    </div>

    <div class="panel">
      <div class="menu">
        <div>Profil</div>
        <div>Ubah kata laluan</div>
        <div>Ubah organisasi</div>
        <div class="active">Jenis tugasan</div>
      </div>

      <div class="content">
        <div class="content-top">
          <h2>Jenis Tugasan</h2>
          <button class="primary-btn">+ Tambah Jenis</button>
        </div>

        <div class="table">
          <div class="row header">
            <div>No</div>
            <div>Nama</div>
          </div>

          <div v-for="item in taskTypes" :key="item.no" class="row">
            <div>{{ item.no }}</div>
            <div>{{ item.nama }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.eyebrow {
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
}

.title {
  font-size: 30px;
  font-weight: 800;
  color: #111827;
  margin-bottom: 6px;
}

.subtitle {
  font-size: 15px;
  color: #6b7280;
}

.panel {
  display: flex;
  background: white;
  border-radius: 22px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.menu {
  width: 240px;
  border-right: 1px solid #eef2f7;
  padding: 28px 20px;
  background: #f8fafc;
}

.menu div {
  padding: 12px 14px;
  margin-bottom: 10px;
  border-radius: 12px;
  cursor: pointer;
  color: #374151;
  font-weight: 500;
}

.menu div:hover {
  background: #eef2ff;
}

.active {
  background: #eef4ff;
  color: #1d4ed8 !important;
  font-weight: 700 !important;
}

.content {
  flex: 1;
  padding: 28px;
}

.content-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.content-top h2 {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
}

.primary-btn {
  background: #1d4ed8;
  color: white;
  border: none;
  padding: 12px 18px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.table {
  border: 1px solid #eef2f7;
  border-radius: 16px;
  overflow: hidden;
}

.row {
  display: grid;
  grid-template-columns: 80px 1fr;
  padding: 16px 18px;
  border-bottom: 1px solid #f1f5f9;
}

.header {
  font-weight: 700;
  background: #f8fafc;
}
</style>