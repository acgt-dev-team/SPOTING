<script setup>
defineProps({
  placeholder: {
    type: String,
    default: "Cari..."
  },
  buttonText: String,
  showButton: Boolean
})

const emit = defineEmits(["action"])
</script>

<template>
  <div class="toolbar">
    <input class="search" :placeholder="placeholder" />

    <button
      v-if="showButton"
      class="primary-btn"
      @click="$emit('action')"
    >
      {{ buttonText }}
    </button>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}

.search {
  width: 320px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid #d1d5db;
  outline: none;
}

.primary-btn {
  background: #1d4ed8;
  color: white;
  padding: 12px 18px;
  border-radius: 12px;
  border: none;
  font-weight: 700;
  cursor: pointer;
}
</style>