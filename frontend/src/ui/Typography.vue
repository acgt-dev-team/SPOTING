<script setup>
import { t } from "../i18n"
</script>

<template>
  <div class="typography">
    <h1 class="ui-heading-1">{{ t("common.name") }}</h1>
    <h2 class="ui-heading-2">{{ t("common.description") }}</h2>
    <h3 class="ui-heading-3">{{ t("common.status") }}</h3>
    <h4 class="ui-heading-4">{{ t("common.actions") }}</h4>

    <p class="ui-text-body">{{ t("common.noData") }}</p>
    <span class="ui-text-caption">{{ t("common.emptyValue") }}</span>
  </div>
</template>
