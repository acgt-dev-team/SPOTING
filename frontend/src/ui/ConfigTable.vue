<script setup>
import { computed } from "vue"
import { t } from "../i18n"
import AppTableState from "./AppTableState.vue"

const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  empty: {
    type: Boolean,
    default: false
  },
  loadingMessage: {
    type: String,
    default: ""
  },
  emptyMessage: {
    type: String,
    default: ""
  },
  emptyActionText: {
    type: String,
    default: ""
  },
  minWidth: {
    type: String,
    default: ""
  },
  tableClass: {
    type: [String, Array, Object],
    default: ""
  }
})

const emit = defineEmits(["empty-action"])

const tableStyle = computed(() => (
  props.minWidth ? { minWidth: props.minWidth } : {}
))
</script>

<template>
  <div class="config-table-card">
    <div class="config-table-scroll">
      <table
        class="config-table"
        :class="tableClass"
        :style="tableStyle"
      >
        <colgroup>
          <col
            v-for="column in columns"
            :key="column.key"
            :style="column.width ? { width: column.width } : null"
          />
        </colgroup>

        <thead>
          <tr>
            <th
              v-for="column in columns"
              :key="column.key"
              :class="{
                'config-table__nowrap': column.nowrap,
                'config-table__center': column.align === 'center'
              }"
            >
              {{ column.label }}
            </th>
          </tr>
        </thead>

        <tbody>
          <AppTableState
            v-if="loading"
            :colspan="columns.length"
            :message="loadingMessage || t('common.loading')"
            loading
          />

          <AppTableState
            v-else-if="empty"
            :colspan="columns.length"
            :message="emptyMessage || t('common.noData')"
            :action-text="emptyActionText"
            @action="emit('empty-action')"
          />

          <slot v-else />
        </tbody>
      </table>
    </div>
  </div>
</template>
