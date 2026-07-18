<script setup>
import { computed, ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"
import { t } from "../../i18n"
import { getPasswordRuleChecks, isValidPassword } from "../../utils/validation"

import AppInput from "../../ui/AppInput.vue"
import AppButton from "../../ui/AppButton.vue"

const router = useRouter()

const password = ref("")
const confirmPassword = ref("")
const error = ref("")
const loading = ref(false)

const passwordRuleChecks = computed(() => getPasswordRuleChecks(password.value, {
  length: t("auth.changePassword.rules.length"),
  upper: t("auth.changePassword.rules.upper"),
  lower: t("auth.changePassword.rules.lower"),
  number: t("auth.changePassword.rules.number"),
  special: t("auth.changePassword.rules.special")
}))

async function submit(e) {
  if (e) e.preventDefault()
  if (loading.value) return

  error.value = ""

  if (!password.value || !confirmPassword.value) {
    error.value = t("validation.allFieldsRequired")
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = t("validation.passwordMismatch")
    return
  }

  if (!isValidPassword(password.value)) {
    error.value = t("validation.passwordFormat")
    return
  }

  loading.value = true

  try {

    await api.post("/auth/change-password", {
      password: password.value
    })

    sessionStorage.removeItem(
      "forcePasswordChange"
    )

    const role =
      sessionStorage.getItem("role")

    if (
      role === "admin" ||
      role === "super admin"
    ) {
      router.push("/admin/configuration")
    } else {
      router.push("/admin/dashboard")
    }

  } catch (err) {
    console.error(err)
    error.value =
      err.response?.data?.detail ||
      t("auth.changePassword.error")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">

    <div class="change-wrapper">

      <div class="card">

        <p class="eyebrow">
          {{ t("auth.changePassword.eyebrow") }}
        </p>

        <h2 class="title">
          {{ t("auth.changePassword.title") }}
        </h2>

        <p class="desc">
          {{ t("auth.changePassword.description") }}
        </p>

        <form @submit.prevent="submit">

          <AppInput
            :label="t('auth.changePassword.newPassword')"
            type="password"
            v-model="password"
          />

          <AppInput
            :label="t('auth.changePassword.confirmPassword')"
            type="password"
            v-model="confirmPassword"
          />

          <div class="password-rules" aria-live="polite">
            <span
              v-for="rule in passwordRuleChecks"
              :key="rule.label"
              class="password-rule"
              :class="{ passed: rule.passed }"
            >
              {{ rule.label }}
            </span>
          </div>

          <p
            v-if="error"
            class="error"
          >
            {{ error }}
          </p>

          <AppButton
            :text="t('auth.changePassword.submit')"
            type="button"
            class="submit-btn"
            :disabled="loading"
            @click="submit"
          />

        </form>

      </div>

    </div>

  </div>
</template>

<style scoped>
:root{
  --primary:#4F46E5;
  --primary-hover:#4338CA;
  --text:#0F172A;
  --muted:#64748B;
  --border:#E2E8F0;
  --bg:#F8FAFC;
}

.page{
  min-height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:24px;
  background:#F8FAFC;
}

.change-wrapper{
  width:100%;
  max-width:480px;
}

.card{
  background:white;
  border:1px solid var(--border);
  border-radius:20px;
  padding:32px;
  box-shadow:0 1px 2px rgba(15,23,42,.04);
}

.title{
  margin:0;
  text-align:center;
  font-size:28px;
  font-weight:800;
  color:var(--text);
  letter-spacing:-0.02em;
}

.desc{
  text-align:center;
  font-size:14px;
  color:var(--muted);
  margin:12px 0 28px;
  line-height:1.6;
}

form{
  display:flex;
  flex-direction:column;
  gap:18px;
}

.submit-btn{
  width:100%;
  margin-top:6px;
}

.error{
  background:#FEF2F2;
  border:1px solid #FECACA;
  color:#DC2626;
  border-radius:12px;
  padding:12px 14px;
  font-size:13px;
  font-weight:600;
}

.password-rules{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
}

.password-rule{
  padding:6px 10px;
  border:1px solid var(--border);
  border-radius:999px;
  color:var(--muted);
  font-size:12px;
  font-weight:600;
}

.password-rule.passed{
  border-color:#86EFAC;
  background:#F0FDF4;
  color:#15803D;
}

.eyebrow{
  text-align:center;
  color:#4F46E5;
  font-size:12px;
  font-weight:700;
  letter-spacing:.12em;
  margin-bottom:12px;
}

@media(max-width:640px){

  .page{
    padding:16px;
  }

  .card{
    padding:24px;
  }

  .title{
    font-size:24px;
  }

}
</style>
