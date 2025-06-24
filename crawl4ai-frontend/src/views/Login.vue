<template>
  <el-form :model="form" class="form-box" @submit.prevent="submitLogin">
    <el-form-item label="用户名" required>
      <el-input v-model="form.username" autocomplete="off" />
    </el-form-item>
    <el-form-item label="密码" required>
      <el-input type="password" v-model="form.password" autocomplete="off" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitLogin">登录</el-button>
      <el-button @click="backHome" style="margin-left: 20px;">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
  username: '',
  password: ''
})

const submitLogin = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请填写完整信息')
    return
  }
  try {
    const res = await axios.post('http://localhost:8000/api/user/login/', form.value)
    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)
    ElMessage.success('登录成功，跳转到功能页')
    router.push('/dashboard')
  } catch (error) {
    ElMessage.error(error.response?.data?.msg || '登录失败')
  }
}

const backHome = () => {
  router.push('/')
}
</script>

<style scoped>
.form-box {
  max-width: 400px;
  margin: 50px auto;
}
</style>
