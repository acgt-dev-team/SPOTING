<script setup>
defineProps({
  show: Boolean,
  title: String
})

const emit = defineEmits(["close"])
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="modal-overlay">

      <div class="modal-card">

        <div class="modal-header">
          <h2>{{ title }}</h2>

          <button class="close-btn" @click="$emit('close')">
            ✕
          </button>
        </div>

        <div class="modal-body">
          <slot />
        </div>

      </div>

    </div>
  </transition>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-card {
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.modal-header h2 {
  font-size: 24px;
  font-weight: 800;
}

.close-btn {
  border: none;
  background: #f3f4f6;
  width: 40px;
  height: 40px;
  border-radius: 999px;
  cursor: pointer;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>