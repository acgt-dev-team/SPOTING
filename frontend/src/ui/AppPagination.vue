<script setup>
import { ArrowLeft, ArrowRight } from "lucide-vue-next"
import { t } from "../i18n"

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
  <div class="ui-pagination">

    <button
      class="ui-pagination__button"
      :title="t('common.previousPage')"
      :aria-label="t('common.previousPage')"
      :disabled="currentPage === 1"
      @click="changePage(currentPage - 1)"
    >
      <ArrowLeft :size="18" aria-hidden="true" />
    </button>

    <span class="ui-pagination__info">
      {{ currentPage }} / {{ totalPages }}
    </span>

    <button
      class="ui-pagination__button"
      :title="t('common.nextPage')"
      :aria-label="t('common.nextPage')"
      :disabled="currentPage === totalPages"
      @click="changePage(currentPage + 1)"
    >
      <ArrowRight :size="18" aria-hidden="true" />
    </button>

  </div>
</template>
