<script setup>
const users = [
  {
    bil: 1,
    nama: "Khairul Izwan",
    username: "khairulizwan",
    peranan: "Pentadbir",
    email: "khairul.izwan@kkm.com.my"
  },
  {
    bil: 2,
    nama: "Aina Syafiqah",
    username: "ainasyafiqah",
    peranan: "Pengguna",
    email: "aina.syafiqah@moe.gov.my"
  },
  {
    bil: 3,
    nama: "Hakim Zulkifli",
    username: "hakimz",
    peranan: "Pengguna",
    email: "hakim.zulkifli@kdn.gov.my"
  }
]
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <p class="eyebrow">PENGURUSAN</p>
        <h1 class="title">Pengurusan Pengguna</h1>
        <p class="subtitle">Senarai pengguna berdaftar dalam sistem.</p>
      </div>

      <button class="primary-btn">+ Tambah Pengguna</button>
    </div>

    <div class="table-card">
      <div class="table-toolbar">
        <input class="search" type="text" placeholder="Cari nama atau emel..." />
      </div>

      <div class="table">
        <div class="row header">
          <div>Bil</div>
          <div>Nama</div>
          <div>Nama pengguna</div>
          <div>Peranan</div>
          <div>Email</div>
        </div>

        <div v-for="user in users" :key="user.bil" class="row">
          <div>{{ user.bil }}</div>
          <div class="bold">{{ user.nama }}</div>
          <div>{{ user.username }}</div>
          <div>
            <span class="badge" :class="user.peranan === 'Pentadbir' ? 'admin' : 'user'">
              {{ user.peranan }}
            </span>
          </div>
          <div>{{ user.email }}</div>
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
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

.primary-btn {
  background: #1d4ed8;
  color: white;
  border: none;
  padding: 12px 18px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.table-card {
  background: white;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.table-toolbar {
  padding: 20px;
  border-bottom: 1px solid #eef2f7;
}

.search {
  width: 100%;
  max-width: 340px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid #d1d5db;
  outline: none;
}

.table {
  width: 100%;
}

.row {
  display: grid;
  grid-template-columns: 60px 1.2fr 1fr 160px 1.2fr;
  padding: 18px 20px;
  border-bottom: 1px solid #f1f5f9;
  align-items: center;
}

.header {
  font-weight: 700;
  background: #f8fafc;
}

.bold {
  font-weight: 700;
  color: #111827;
}

.badge {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.admin {
  background: #dbeafe;
  color: #1d4ed8;
}

.user {
  background: #dcfce7;
  color: #15803d;
}
</style>