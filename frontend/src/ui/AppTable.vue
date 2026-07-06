<script setup>
import { t } from "../i18n"

defineProps({
  columns: Array,
  data: Array
})

const emit = defineEmits(["delete"])
</script>

<template>
  <div class="ui-table">
    <div class="ui-table__row ui-table__header">
      <div v-for="col in columns" :key="col">
        {{ col }}
      </div>
      <div></div>
    </div>

    <div v-for="item in data" :key="item.id" class="ui-table__row">
      <slot :item="item" />

      <div class="ui-table__actions">
        <button class="ui-table__delete" @click="$emit('delete', item.id)">
          {{ t("common.delete") }}
        </button>
      </div>
    </div>

    <div v-if="data.length === 0" class="ui-empty-state">
      {{ t("common.noData") }}
    </div>
  </div>
</template>
