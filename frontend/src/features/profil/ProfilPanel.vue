<script setup>
const profiles = [
  {
    kod: "PRF-001",
    nama: "Profil Asas",
    tapak: "-",
    tugasan: ["Imbasan Rangkaian", "Pemantauan Trafik"],
    status: "Aktif"
  },
  {
    kod: "PRF-002",
    nama: "Profil Lanjutan",
    tapak: "-",
    tugasan: ["Imbasan Rangkaian", "Ujian Keselamatan"],
    status: "Aktif"
  },
  {
    kod: "PRF-003",
    nama: "Profil Standard",
    tapak: "Data Centre Selayang",
    tugasan: ["Pemantauan Trafik"],
    status: "Tidak Aktif"
  }
]
</script>

<template>
  <div class="page">
    <!-- HEADER -->
    <div class="page-header">
      <div>
        <p class="eyebrow">PROFIL</p>
        <h1 class="title">Senarai Profil</h1>
        <p class="subtitle">Pengurusan profil sistem dan tugasan berkaitan.</p>
      </div>

      <button class="primary-btn">+ Tambah Profil</button>
    </div>

    <!-- TABLE -->
    <div class="table-card">
      <table class="table">
        <thead>
          <tr>
            <th>Kod</th>
            <th>Nama</th>
            <th>Tapak</th>
            <th>Tugasan</th>
            <th>Status</th>
            <th class="text-right">Tindakan</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="item in profiles" :key="item.kod">
            <td>
              <span class="badge">{{ item.kod }}</span>
            </td>

            <td class="bold">{{ item.nama }}</td>

            <td>{{ item.tapak }}</td>

            <td>
              <div class="chips">
                <span v-for="t in item.tugasan" :key="t" class="chip">
                  {{ t }}
                </span>
              </div>
            </td>

            <td>
              <span
                class="status"
                :class="item.status === 'Aktif' ? 'active' : 'inactive'"
              >
                {{ item.status }}
              </span>
            </td>

            <td class="text-right">
              <button class="btn edit">Edit</button>
              <button class="btn delete">Padam</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* HEADER */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.eyebrow {
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: 0.08em;
  margin-bottom: 6px;
}

.title {
  font-size: 28px;
  font-weight: 800;
  color: #111827;
}

.subtitle {
  font-size: 14px;
  color: #6b7280;
}

.primary-btn {
  background: #1d4ed8;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

/* TABLE */
.table-card {
  background: white;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  font-size: 12px;
  color: #6b7280;
  padding: 14px 16px;
  background: #f9fafb;
}

td {
  padding: 16px;
  border-top: 1px solid #f1f5f9;
  font-size: 14px;
}

.bold {
  font-weight: 600;
}

/* BADGE */
.badge {
  background: #eef2ff;
  color: #1d4ed8;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

/* CHIPS */
.chips {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.chip {
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
}

/* STATUS */
.status {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.status.active {
  background: #dcfce7;
  color: #15803d;
}

.status.inactive {
  background: #fee2e2;
  color: #b91c1c;
}

/* BUTTONS */
.btn {
  border: none;
  padding: 6px 12px;
  border-radius: 8px;
  margin-left: 6px;
  cursor: pointer;
  font-size: 12px;
}

.edit {
  background: #e0f2fe;
  color: #0369a1;
}

.delete {
  background: #fee2e2;
  color: #b91c1c;
}

.text-right {
  text-align: right;
}
</style>