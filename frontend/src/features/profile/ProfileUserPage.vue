<script setup>
import { computed, onMounted, ref } from "vue"
import api from "../../services/api"
import { t } from "../../i18n"
import { useToast } from "../../ui/AppToast.vue"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"
import AppCard from "../../ui/AppCard.vue"
import PageHeader from "../../ui/PageHeader.vue"

const toast = useToast()

const nama = ref("")
const username = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")
const confirmPassword = ref("")

const loading = ref(true)
const saving = ref(false)
const submitAttempted = ref(false)
const loadError = ref("")

const passwordRuleChecks = computed(() => [
  {
    label: t("profileUser.passwordRules.length"),
    passed: password.value.length >= 8
  },
  {
    label: t("profileUser.passwordRules.upper"),
    passed: /[A-Z]/.test(password.value)
  },
  {
    label: t("profileUser.passwordRules.lower"),
    passed: /[a-z]/.test(password.value)
  },
  {
    label: t("profileUser.passwordRules.number"),
    passed: /\d/.test(password.value)
  }
])

const isPasswordStrong = computed(() =>
  !password.value || passwordRuleChecks.value.every((rule) => rule.passed)
)

const fieldErrors = computed(() => {
  const errors = {}
  const emailValue = email.value.trim()
  const phoneValue = phone.value.trim()

  if (!nama.value.trim()) {
    errors.nama = t("validation.nameRequired")
  }

  if (emailValue && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue)) {
    errors.email = t("profileUser.emailInvalid")
  }

  if (phoneValue && !/^[0-9+\-()\s]{7,20}$/.test(phoneValue)) {
    errors.phone = t("profileUser.phoneInvalid")
  }

  if (password.value && !isPasswordStrong.value) {
    errors.password = t("profileUser.passwordWeak")
  }

  if (password.value && password.value !== confirmPassword.value) {
    errors.confirmPassword = t("profileUser.passwordMismatch")
  }

  if (!password.value && confirmPassword.value) {
    errors.confirmPassword = t("profileUser.passwordMismatch")
  }

  return errors
})

const nameError = computed(() =>
  fieldErrors.value.nama || ""
)

const emailError = computed(() =>
  email.value || submitAttempted.value ? fieldErrors.value.email || "" : ""
)

const phoneError = computed(() =>
  phone.value || submitAttempted.value ? fieldErrors.value.phone || "" : ""
)

const passwordError = computed(() =>
  password.value || submitAttempted.value ? fieldErrors.value.password || "" : ""
)

const confirmPasswordError = computed(() =>
  password.value || confirmPassword.value || submitAttempted.value
    ? fieldErrors.value.confirmPassword || ""
    : ""
)

const canSave = computed(() =>
  !loading.value &&
  !saving.value &&
  Object.keys(fieldErrors.value).length === 0
)

async function loadProfile() {
  loading.value = true
  loadError.value = ""

  try {
    const currentUsername = sessionStorage.getItem("username")

    const res = await api.get(`/auth/profile/${currentUsername}`)

    nama.value = res.data.nama || ""
    username.value = res.data.username || ""
    email.value = res.data.email || ""
    phone.value = res.data.phone || ""
  } catch (err) {
    console.error(err)
    loadError.value = t("profileUser.errorLoad")
    toast.error(t("profileUser.errorLoad"))
  } finally {
    loading.value = false
  }
}

async function saveProfile() {
  submitAttempted.value = true

  if (!canSave.value) {
    toast.warning(t("validation.completeBeforeSave"))
    return
  }

  saving.value = true

  try {
    await api.put(`/auth/profile/${username.value}`, {
      nama: nama.value.trim(),
      email: email.value.trim() || null,
      phone: phone.value.trim() || null,
      password: password.value || null
    })

    password.value = ""
    confirmPassword.value = ""
    submitAttempted.value = false

    toast.success(t("profileUser.successSave"))
  } catch (err) {
    console.error(err)
    toast.error(t("profileUser.errorSave"))
  } finally {
    saving.value = false
  }
}

onMounted(loadProfile)
</script>

<template>
  <div>
    <PageHeader
      :title="t('profileUser.title')"
      :description="t('profileUser.description')"
    />

    <div v-if="loadError" class="profile-alert">
      <strong>{{ loadError }}</strong>
      <button
        class="ui-button ui-button--outline"
        type="button"
        :disabled="loading"
        @click="loadProfile"
      >
        {{ t("dashboard.refresh") }}
      </button>
    </div>

    <AppCard v-if="loading" class="profile-card profile-loading">
      {{ t("profileUser.loading") }}
    </AppCard>

    <div v-else class="profile-layout">
      <AppCard class="profile-card">
        <div class="card-header">
          <p class="eyebrow">{{ t("profileUser.eyebrow") }}</p>
          <h3>{{ t("profileUser.accountInfo") }}</h3>
          <p>{{ t("profileUser.accountInfoDescription") }}</p>
        </div>

        <div class="form-grid">
          <AppInput
            v-model="nama"
            :label="t('common.name')"
            :placeholder="t('profileUser.namePlaceholder')"
            :disabled="saving"
            :error="nameError"
            autocomplete="name"
          />

          <AppInput
            v-model="username"
            :label="t('auth.username')"
            disabled
            autocomplete="username"
          />

          <AppInput
            v-model="email"
            :label="t('profileUser.email')"
            :placeholder="t('profileUser.emailPlaceholder')"
            :disabled="saving"
            :error="emailError"
            autocomplete="email"
          />

          <AppInput
            v-model="phone"
            :label="t('profileUser.phone')"
            :placeholder="t('profileUser.phonePlaceholder')"
            :disabled="saving"
            :error="phoneError"
            autocomplete="tel"
          />
        </div>
      </AppCard>

      <AppCard class="profile-card">
        <div class="card-header">
          <p class="eyebrow">{{ t("profileUser.security") }}</p>
          <h3>{{ t("profileUser.newPassword") }}</h3>
          <p>{{ t("profileUser.securityDescription") }}</p>
        </div>

        <div class="form-grid">
          <AppInput
            v-model="password"
            :label="t('profileUser.newPassword')"
            type="password"
            :placeholder="t('profileUser.passwordPlaceholder')"
            :disabled="saving"
            :error="passwordError"
            :hint="t('profileUser.passwordHint')"
            autocomplete="new-password"
          />

          <AppInput
            v-model="confirmPassword"
            :label="t('profileUser.confirmPassword')"
            type="password"
            :placeholder="t('profileUser.confirmPasswordPlaceholder')"
            :disabled="saving"
            :error="confirmPasswordError"
            autocomplete="new-password"
          />
        </div>

        <div
          v-if="password"
          class="password-rules"
          aria-live="polite"
        >
          <span
            v-for="rule in passwordRuleChecks"
            :key="rule.label"
            class="password-rule"
            :class="{ passed: rule.passed }"
          >
            {{ rule.label }}
          </span>
        </div>
      </AppCard>

      <div class="action-bar">
        <AppButton
          :text="saving ? t('common.saving') : t('common.saveChanges')"
          :disabled="!canSave"
          @click="saveProfile"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  padding: 32px !important;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
}

.profile-loading {
  min-height: 180px;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-bold);
}

.profile-alert {
  margin-bottom: 20px;
  padding: 16px;
  border: 1px solid rgba(220, 38, 38, 0.22);
  border-radius: var(--radius-xl);
  background: var(--color-surface);
  color: var(--color-text);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.eyebrow {
  margin: 0 0 8px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: var(--font-weight-extrabold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.card-header {
  margin-bottom: 24px;
}

.card-header h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 22px;
  font-weight: var(--font-weight-extrabold);
}

.card-header p:last-child {
  max-width: 760px;
  margin: 8px 0 0;
  color: var(--color-text-muted);
  line-height: 1.6;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.password-rules {
  margin-top: 4px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.password-rule {
  min-height: 30px;
  padding: 0 10px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  color: var(--color-text-muted);
  display: inline-flex;
  align-items: center;
  font-size: 12px;
  font-weight: var(--font-weight-bold);
}

.password-rule.passed {
  border-color: transparent;
  background: var(--color-success-soft);
  color: var(--color-success);
}

.action-bar {
  padding-top: 4px;
  display: flex;
  justify-content: flex-end;
}

@media(max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    padding: 24px !important;
  }

  .profile-alert {
    align-items: stretch;
    flex-direction: column;
  }

  .profile-alert .ui-button,
  .action-bar .ui-button {
    width: 100%;
  }
}
</style>
