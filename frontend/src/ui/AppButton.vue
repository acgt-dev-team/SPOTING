<script setup>
defineEmits(["click"])

defineProps({
  text: String,
  variant: {
    type: String,
    default: "primary"
  },
  full: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <button
    :class="['btn', ...variant.split(' '), { full }]"
    @click="$emit('click')"
    type="button"
  >
    {{ text }}
  </button>
</template>

<style scoped>
.btn{
  min-height:46px;
  padding:0 20px;
  border-radius:14px;
  font-size:14px;
  font-weight:700;
  cursor:pointer;
  border:none;
  transition:.18s;
  white-space:nowrap;
  display:inline-flex;
  align-items:center;
  justify-content:center;
}

.full{
  width:100%;
}

/* PRIMARY */

.primary{
  background:#4F46E5;
  color:white;
  box-shadow:0 8px 18px rgba(79,70,229,.18);
}

.primary:hover{
  background:#4338CA;
}

/* OUTLINE */

.outline{
  background:white;
  border:1px solid #E2E8F0;
  color:#475569;
}

.outline:hover{
  background:#F8FAFC;
  border-color:#CBD5E1;
}

/* SECONDARY */

.secondary{
  background:#EEF2FF;
  color:#4F46E5;
}

.secondary:hover{
  background:#E0E7FF;
}

/* LINK */

.link{
  background:none;
  color:#4F46E5;
  text-decoration:none;
  padding:0;
  min-height:auto;
  border-radius:0;
  box-shadow:none;
}

.link:hover{
  color:#4338CA;
}

/* DANGER */

.danger{
  background:#DC2626;
  color:white;
}

.danger:hover{
  background:#B91C1C;
}

/* OUTLINE DANGER */

.outline.danger{
  background:white;
  border:1px solid #DC2626;
  color:#DC2626;
}

.outline.danger:hover{
  background:#FEF2F2;
}
</style>