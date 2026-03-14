<script setup>
const props = defineProps({
  step: Number
})

const steps = [
  "Pengguna",
  "Organisasi",
  "Sub organisasi",
  "Tapak",
  "Profil",
  "Tugasan"
]
</script>

<template>

<div class="page">

  <div class="header">
    <h1>Pendaftaran</h1>
    <a class="cancel">Batal</a>
  </div>

  <div class="wizard-card">

    <!-- sidebar -->
    <div class="sidebar">

      <div
        v-for="(item,i) in steps"
        :key="i"
        class="step"
      >

        <div
          class="indicator"
          :class="{
            done: step > i+1,
            first: i === 0,
            last: i === steps.length - 1
          }"
        >

          <div
            class="circle"
            :class="{
              active: step === i+1,
              done: step > i+1
            }"
          >
            {{ i+1 }}
          </div>

        </div>

        <div class="label">
          {{ item }}
          <span v-if="step > i+1">Selesai</span>
        </div>

      </div>

    </div>

    <div class="divider"></div>

    <div class="content">
      <slot/>
    </div>

  </div>

</div>

</template>

<style scoped>

.page{
  padding:80px 120px;
  background:#f7f8fc;
  min-height:100vh;
}

.header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:40px;
}

.header h1{
  font-size:28px;
  font-weight:600;
}

.cancel{
  color:#e11d48;
  cursor:pointer;
}

.wizard-card{
  display:flex;
  background:white;
  border-radius:16px;
  padding:48px;
  box-shadow:0 20px 40px rgba(0,0,0,0.06);
}

.sidebar{
  width:220px;
}

.step{
  display:flex;
  align-items:center;
  margin-bottom:28px;
}

.indicator{
  position:relative;
  width:36px;
  height:36px;
  margin-right:14px;
}

/* top half line */
.indicator::before{
  content:"";
  position:absolute;
  left:50%;
  transform:translateX(-50%);
  top:-28px;
  width:2px;
  height:28px;
  background:#e5e7eb;
}

/* bottom half line */
.indicator::after{
  content:"";
  position:absolute;
  left:50%;
  transform:translateX(-50%);
  bottom:-28px;
  width:2px;
  height:28px;
  background:#e5e7eb;
}

/* remove top line for first step */
.indicator.first::before{
  display:none;
}

/* remove bottom line for last step */
.indicator.last::after{
  display:none;
}

/* completed connectors */
.indicator.done::before,
.indicator.done::after{
  background:#22c55e;
}

.circle{
  width:36px;
  height:36px;
  border-radius:50%;
  border:2px solid #cbd5e1;
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight:600;
  background:white;
  position:relative;
  z-index:2;
}

.circle.active{
  border-color:#a855f7;
  color:#a855f7;
}

.circle.done{
  border-color:#22c55e;
  color:#22c55e;
}

.label{
  font-size:15px;
}

.label span{
  display:block;
  font-size:12px;
  color:#22c55e;
}

.divider{
  width:1px;
  background:#e5e7eb;
  margin:0 40px;
}

.content{
  flex:1;
  max-width:520px;
}

</style>