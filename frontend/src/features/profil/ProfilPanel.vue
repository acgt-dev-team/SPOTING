<script setup>
const profile = {
  nama: "Test User",
  username: "testuser",
  email: "test@example.com",
  peranan: "Pengguna Sistem",
  organisasi: "Kementerian Dalam Negeri",
  telefon: "+60 12-345 6789"
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <p class="eyebrow">PROFIL</p>
        <h1 class="title">Profil Pengguna</h1>
        <p class="subtitle">Maklumat peribadi dan butiran akaun pengguna.</p>
      </div>

      <button class="primary-btn">Kemas Kini Profil</button>
    </div>

    <div class="profile-grid">
      <div class="profile-card">
        <div class="avatar">W</div>
        <h2>{{ profile.nama }}</h2>
        <p>{{ profile.peranan }}</p>
      </div>

      <div class="details-card">
        <div class="info-row">
          <span>Nama</span>
          <strong>{{ profile.nama }}</strong>
        </div>

        <div class="info-row">
          <span>Nama Pengguna</span>
          <strong>{{ profile.username }}</strong>
        </div>

        <div class="info-row">
          <span>Email</span>
          <strong>{{ profile.email }}</strong>
        </div>

        <div class="info-row">
          <span>Peranan</span>
          <strong>{{ profile.peranan }}</strong>
        </div>

        <div class="info-row">
          <span>Organisasi</span>
          <strong>{{ profile.organisasi }}</strong>
        </div>

        <div class="info-row">
          <span>No Telefon</span>
          <strong>{{ profile.telefon }}</strong>
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

.profile-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
}

.profile-card,
.details-card {
  background: white;
  border-radius: 22px;
  border: 1px solid #e5e7eb;
  padding: 28px;
}

.profile-card {
  text-align: center;
}

.avatar {
  width: 84px;
  height: 84px;
  border-radius: 50%;
  background: #1d4ed8;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 800;
  margin: 0 auto 16px;
}

.profile-card h2 {
  font-size: 22px;
  font-weight: 800;
  color: #111827;
  margin-bottom: 6px;
}

.profile-card p {
  color: #6b7280;
  font-size: 14px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 18px 0;
  border-bottom: 1px solid #f1f5f9;
}

.info-row span {
  color: #6b7280;
  font-size: 14px;
}

.info-row strong {
  color: #111827;
  font-size: 15px;
}
</style>