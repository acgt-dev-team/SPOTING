<script setup>
const cards = [
  { value: "43", label: "Jumlah organisasi", color: "blue" },
  { value: "120", label: "Jumlah profil", color: "blue" },
  { value: "2.4k", sub: "/ 10.2k", label: "Jumlah tugasan", color: "green" },
  { value: "9.4k", label: "Jumlah peranti selesai", color: "green" }
]

const organizations = [
  {
    bil: 1,
    nama: "Kementerian Dalam Negeri",
    tugasan: "1,233 / 9,000"
  },
  {
    bil: 2,
    nama: "Kementerian Kesihatan Malaysia",
    tugasan: "850 / 4,200"
  },
  {
    bil: 3,
    nama: "Kementerian Pendidikan Malaysia",
    tugasan: "2,145 / 6,400"
  }
]
</script>

<template>
  <div class="dashboard-page">
    <div class="hero">
      <div>
        <p class="eyebrow">SELAMAT DATANG</p>
        <h1 class="title">Gambaran keseluruhan</h1>
        <p class="subtitle">
          Ringkasan status semasa sistem, organisasi dan kemajuan tugasan.
        </p>
      </div>

      <div class="hero-badge">
        <span class="dot"></span>
        Sistem Aktif
      </div>
    </div>

    <div class="cards">
      <div v-for="(card, index) in cards" :key="index" class="card">
        <div class="number" :class="card.color">
          {{ card.value }}
          <span v-if="card.sub">{{ card.sub }}</span>
        </div>
        <div class="label">{{ card.label }}</div>
      </div>
    </div>

    <div class="content-grid">
      <div class="panel large">
        <div class="panel-header">
          <h2>Organisasi</h2>
          <button class="ghost-btn">Lihat semua</button>
        </div>

        <div class="table">
          <div class="row header">
            <div>Bil</div>
            <div>Nama</div>
            <div>Tugasan</div>
          </div>

          <div v-for="item in organizations" :key="item.bil" class="row">
            <div>{{ item.bil }}</div>
            <div>{{ item.nama }}</div>
            <div class="green">{{ item.tugasan }}</div>
          </div>
        </div>
      </div>

      <div class="panel side">
        <div class="panel-header">
          <h2>Aktiviti Ringkas</h2>
        </div>

        <div class="activity-list">
          <div class="activity-item">
            <div class="activity-dot blue"></div>
            <div>
              <div class="activity-title">Tugasan baru telah ditambah</div>
              <div class="activity-time">5 minit lalu</div>
            </div>
          </div>

          <div class="activity-item">
            <div class="activity-dot green"></div>
            <div>
              <div class="activity-title">Profil berjaya dikemaskini</div>
              <div class="activity-time">1 jam lalu</div>
            </div>
          </div>

          <div class="activity-item">
            <div class="activity-dot orange"></div>
            <div>
              <div class="activity-title">Organisasi baharu didaftarkan</div>
              <div class="activity-time">Hari ini</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #2563eb;
  margin-bottom: 8px;
}

.title {
  font-size: 32px;
  font-weight: 800;
  color: #111827;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 15px;
  color: #6b7280;
  max-width: 700px;
}

.hero-badge {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 999px;
  padding: 10px 14px;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #111827;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #22c55e;
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.card {
  background: white;
  padding: 24px;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

.number {
  font-size: 34px;
  font-weight: 800;
  line-height: 1;
}

.number span {
  font-size: 14px;
  color: #6b7280;
  margin-left: 6px;
}

.blue {
  color: #2563eb;
}

.green {
  color: #16a34a;
  font-weight: 700;
}

.label {
  margin-top: 10px;
  font-size: 14px;
  color: #6b7280;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.panel {
  background: white;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  padding: 24px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.panel-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

.ghost-btn {
  background: #eff6ff;
  color: #1d4ed8;
  border: none;
  padding: 10px 14px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.table {
  border: 1px solid #eef2f7;
  border-radius: 16px;
  overflow: hidden;
}

.row {
  display: grid;
  grid-template-columns: 80px 1fr 200px;
  padding: 16px 18px;
  border-bottom: 1px solid #f1f5f9;
  align-items: center;
}

.header {
  font-weight: 700;
  background: #f8fafc;
  color: #374151;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.activity-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.activity-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 6px;
}

.activity-dot.blue {
  background: #2563eb;
}

.activity-dot.green {
  background: #22c55e;
}

.activity-dot.orange {
  background: #f59e0b;
}

.activity-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.activity-time {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
}
</style>