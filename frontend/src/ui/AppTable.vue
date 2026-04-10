<script setup>
defineProps({
  columns: Array,
  data: Array
})

const emit = defineEmits(["delete"])
</script>

<template>
  <div class="table">
    <div class="row header">
      <div v-for="col in columns" :key="col">
        {{ col }}
      </div>
      <div></div>
    </div>

    <div v-for="item in data" :key="item.id" class="row">
      <slot :item="item" />

      <div class="actions">
        <button class="delete" @click="$emit('delete', item.id)">
          Padam
        </button>
      </div>
    </div>

    <div v-if="data.length === 0" class="empty">
      Tiada data ditemui
    </div>
  </div>
</template>

<style scoped>
.table {
  border-top: 1px solid #eef2f7;
}

.row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)) 120px;
  padding: 16px 0;
  border-bottom: 1px solid #f1f5f9;
  align-items: center;
}

.header {
  font-weight: 700;
  background: #f8fafc;
  padding: 14px 0;
}

.actions {
  text-align: right;
}

.delete {
  color: #ef4444;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
}

.empty {
  padding: 30px;
  text-align: center;
  color: #6b7280;
}
</style>