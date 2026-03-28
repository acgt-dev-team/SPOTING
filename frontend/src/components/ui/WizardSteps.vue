<script setup>
const props = defineProps({
  active: String,
  completed: Object
})

const emit = defineEmits(["change"])

const steps = [
  { key: "organization", label: "Organisasi" },
  { key: "suborg", label: "Sub organisasi" },
  { key: "site", label: "Tapak" },
  { key: "profil", label: "Profil" },
  { key: "tugasan", label: "Tugasan" }
]

function select(key) {
  emit("change", key)
}
</script>

<template>

<div class="sidebar">

  <div
    v-for="(item,i) in steps"
    :key="i"
    class="step"
    @click="select(item.key)"
  >

    <div
      class="indicator"
      :class="{
        done: completed[item.key],
        first: i === 0,
        last: i === steps.length - 1
      }"
    >

      <div
        class="circle"
        :class="{
          active: active === item.key,
          done: completed[item.key]
        }"
      >
        {{ i+1 }}
      </div>

    </div>

    <div class="label">
      {{ item.label }}
      <span v-if="completed[item.key]">Selesai</span>
    </div>

  </div>

</div>

</template>

<style scoped>
.sidebar{
  width:220px;
}

.step{
  display:flex;
  align-items:center;
  margin-bottom:28px;
  cursor:pointer;
}

.indicator{
  position:relative;
  width:36px;
  height:36px;
  margin-right:14px;
}

.indicator::before{
  content:"";
  position:absolute;
  left:50%;
  transform:translateX(-1px);
  top:-28px;
  width:2px;
  height:28px;
  background:#e5e7eb;
}

.indicator::after{
  content:"";
  position:absolute;
  left:50%;
  transform:translateX(-1px);
  bottom:-28px;
  width:2px;
  height:28px;
  background:#e5e7eb;
}

.indicator.first::before{
  display:none;
}

.indicator.last::after{
  display:none;
}

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
</style>