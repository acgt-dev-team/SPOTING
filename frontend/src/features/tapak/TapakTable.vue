<script setup>
const sites = [
  {
    bil: 1,
    nama: "Ibu Pejabat Putrajaya",
    lokasi: "Putrajaya",
    peranti: 230,
    status: "Aktif"
  },
  {
    bil: 2,
    nama: "Cawangan Shah Alam",
    lokasi: "Selangor",
    peranti: 180,
    status: "Aktif"
  },
  {
    bil: 3,
    nama: "Cawangan Johor Bahru",
    lokasi: "Johor",
    peranti: 120,
    status: "Dalam Semakan"
  }
]
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <p class="eyebrow">LOKASI</p>
        <h1 class="title">Tapak</h1>
        <p class="subtitle">Senarai tapak yang berkaitan dengan organisasi semasa.</p>
      </div>

      <button class="primary-btn">+ Tambah Tapak</button>
    </div>

    <div class="table-card">
      <div class="table">
        <div class="row header">
          <div>Bil</div>
          <div>Nama Tapak</div>
          <div>Lokasi</div>
          <div>Jumlah Peranti</div>
          <div>Status</div>
        </div>

        <div v-for="site in sites" :key="site.bil" class="row">
          <div>{{ site.bil }}</div>
          <div class="bold">{{ site.nama }}</div>
          <div>{{ site.lokasi }}</div>
          <div>{{ site.peranti }}</div>
          <div>
            <span class="status" :class="site.status === 'Aktif' ? 'done' : 'review'">
              {{ site.status }}
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

.row {
  display: grid;
  grid-template-columns: 60px 2fr 1fr 1fr 160px;
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

.review {
  background: #fef3c7;
  color: #b45309;
}
</style>