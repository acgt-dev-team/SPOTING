<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue"
import { ChevronDown } from "lucide-vue-next"
import { t } from "../i18n"

const props = defineProps({
  label: String,
  options: Array,
  modelValue: String,
  placeholder: {
    type: String,
    default: ""
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
  return found ? (found.label || found) : (props.placeholder || t("common.select"))
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
  <div class="ui-field" ref="root">
    <label v-if="label" class="ui-field__label">
      {{ label }}
    </label>

    <div class="ui-select" tabindex="0" @click="open = !open">
      <span class="ui-select__value">
        {{ selectedLabel }}
      </span>

      <ChevronDown class="ui-select__icon" :size="16" aria-hidden="true" />

      <div v-if="open" class="ui-select__menu">
        <div
          v-for="opt in options"
          :key="opt.value || opt"
          class="ui-select__option"
          @click.stop="select(opt)"
        >
          {{ opt.label || opt }}
        </div>
      </div>
    </div>
  </div>
</template>
