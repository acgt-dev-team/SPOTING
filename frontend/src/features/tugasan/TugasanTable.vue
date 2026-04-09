<script setup>
const tasks = [
  {
    bil: 1,
    nama: "Tugasan 1",
    protokol: "v4",
    julatIp: "127.0.0.1 - 127.0.0.245",
    peranti: "1,233 / 1,233",
    status: "Selesai"
  },
  {
    bil: 2,
    nama: "Tugasan 2",
    protokol: "v6",
    julatIp: "192.168.1.1 - 192.168.1.255",
    peranti: "523 / 1,100",
    status: "Dalam Proses"
  },
  {
    bil: 3,
    nama: "Tugasan 3",
    protokol: "v4",
    julatIp: "10.0.0.1 - 10.0.0.150",
    peranti: "120 / 800",
    status: "Belum Mula"
  }
]
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <p class="eyebrow">OPERASI</p>
        <h1 class="title">Tugasan</h1>
        <p class="subtitle">Pantau status pelaksanaan tugasan semasa.</p>
      </div>

      <button class="primary-btn">+ Tambah Tugasan</button>
    </div>

    <div class="table-card">
      <div class="table-toolbar">
        <input class="search" type="text" placeholder="Cari tugasan..." />
      </div>

      <div class="table">
        <div class="row header">
          <div>Bil</div>
          <div>Nama</div>
          <div>Protokol</div>
          <div>Julat IP</div>
          <div>Peranti</div>
          <div>Status</div>
        </div>

        <div v-for="task in tasks" :key="task.bil" class="row">
          <div>{{ task.bil }}</div>
          <div class="bold">{{ task.nama }}</div>
          <div>{{ task.protokol }}</div>
          <div>{{ task.julatIp }}</div>
          <div class="green">{{ task.peranti }}</div>
          <div>
            <span
              class="status"
              :class="{
                done: task.status === 'Selesai',
                progress: task.status === 'Dalam Proses',
                pending: task.status === 'Belum Mula'
              }"
            >
              {{ task.status }}
            </span>
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

.row {
  display: grid;
  grid-template-columns: 60px 1fr 100px 2fr 1fr 160px;
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

.green {
  color: #16a34a;
  font-weight: 700;
}

.status {
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  display: inline-block;
}

.done {
  background: #dcfce7;
  color: #15803d;
}

.progress {
  background: #dbeafe;
  color: #1d4ed8;
}

.pending {
  background: #fef3c7;
  color: #b45309;
}
</style>