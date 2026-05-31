<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue"

const props = defineProps({
  label: String,
  options: Array,
  modelValue: String,
  placeholder: {
    type: String,
    default: "Pilih"
  }
})

const emit = defineEmits(["update:modelValue"])

const open = ref(false)
const root = ref(null)

/* Get selected label */
const selectedLabel = computed(() => {
  const found = props.options.find(
    (o) => (o.value || o) === props.modelValue
  )
  return found ? (found.label || found) : props.placeholder
})

/* Select option */
function select(opt) {
  emit("update:modelValue", opt.value || opt)
  open.value = false
}

/* Close when clicking outside */
function handleClickOutside(e) {
  if (root.value && !root.value.contains(e.target)) {
    open.value = false
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside)
})
</script>

<template>
  <div class="field" ref="root">
    <label v-if="label" class="field-label">
      {{ label }}
    </label>

    <div class="custom-select" @click="open = !open">
      <span class="selected-text">
        {{ selectedLabel }}
      </span>

      <span class="arrow">▾</span>

      <div v-if="open" class="dropdown">
        <div
          v-for="opt in options"
          :key="opt.value || opt"
          class="option"
          @click.stop="select(opt)"
        >
          {{ opt.label || opt }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.field-label {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
}

/* Main box */
.custom-select {
  position: relative;
  height: 54px;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  cursor: pointer;
  transition: 0.18s ease;
}

.custom-select:hover {
  background: #f3f4f6;
}

/* Selected text */
.selected-text {
  font-size: 14px;
  color: #111827;
}

/* Arrow */
.arrow {
  font-size: 14px;
  color: #6b7280;
}

/* Dropdown */
.dropdown {
  position: absolute;
  top: 60px;
  left: 0;
  right: 0;
  background: white;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
  overflow: hidden;
  z-index: 50;
}

/* Options */
.option {
  padding: 14px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: 0.15s ease;
}

.option:hover {
  background: #f4f6ff;
}
</style>