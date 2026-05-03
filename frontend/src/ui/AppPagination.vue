<script setup>
const props = defineProps({
  currentPage: Number,
  totalPages: Number
})

const emit = defineEmits(["update:currentPage", "update:page"])

const changePage = (page) => {
  if (page < 1 || page > props.totalPages) return

  emit("update:currentPage", page)
  emit("update:page", page)
}
</script>

<template>
  <div class="pagination">

    <button
      class="page-btn"
      :disabled="currentPage === 1"
      @click="changePage(currentPage - 1)"
    >
      ←
    </button>

    <span class="page-info">
      {{ currentPage }} / {{ totalPages }}
    </span>

    <button
      class="page-btn"
      :disabled="currentPage === totalPages"
      @click="changePage(currentPage + 1)"
    >
      →
    </button>

  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 18px;
}

.page-btn {
  border: none;
  padding: 8px 14px;
  border-radius: 10px;
  background: #eef1ff;
  color: #020265;
  font-weight: 700;
  cursor: pointer;
  transition: 0.2s ease;
  outline: none;
}

/* Hover only if clickable */
.page-btn:hover:not(:disabled) {
  background: #dde3ff;
}

/* Disabled state */
.page-btn:disabled {
  opacity: 0.4;
  cursor: default;
}

/* kill focus ring */
.page-btn:focus {
  outline: none;
  box-shadow: none;
}

/* kill active (click) ring */
.page-btn:active {
  outline: none;
  box-shadow: none;
}

/* double safety for disabled */
.page-btn:disabled:focus,
.page-btn:disabled:active {
  outline: none;
  box-shadow: none;
}

.page-info {
  font-size: 14px;
  font-weight: 700;
}
</style>