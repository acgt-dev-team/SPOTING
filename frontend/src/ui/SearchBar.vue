<script setup>
import { Search } from "lucide-vue-next"

defineProps({
  modelValue: String,
  placeholder: String
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>
  <div class="ui-search">
    <Search class="ui-search__icon" :size="18" aria-hidden="true" />

    <input
      type="text"
      class="ui-search__input"
      :placeholder="placeholder"
      :value="modelValue"
      @input="emit('update:modelValue',$event.target.value)"
    />
  </div>
</template>
