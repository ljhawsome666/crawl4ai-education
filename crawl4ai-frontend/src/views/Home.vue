<template>
  <div style="text-align:center; margin-top: 100px;">
    <el-button type="primary" @click="goLogin" style="margin-right: 20px;">登录</el-button>
    <el-button type="success" @click="goRegister">注册</el-button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const goLogin = () => {
  router.push('/login')
}
const goRegister = () => {
  router.push('/register')
}
</script>
