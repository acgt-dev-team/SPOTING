<script setup>
import { ref } from "vue"

import Login from "../../components/auth/Login.vue"
import ForgotPassword from "../../components/auth/ForgotPassword.vue"

const page = ref("login")

function goForgot(){
  page.value = "forgot"
}

function goLogin(){
  page.value = "login"
}
</script>

<template>
  <component
    :is="page === 'login' ? Login : ForgotPassword"
    @forgot="goForgot"
    @back="goLogin"
  />
</template>