<template>
  <el-form :model="form" class="form-box" @submit.prevent="submitRegister">
    <el-form-item label="用户名" required>
      <el-input v-model="form.username" autocomplete="off" />
    </el-form-item>
    <el-form-item label="邮箱" required>
      <el-input v-model="form.email" autocomplete="off" />
    </el-form-item>
    <el-form-item label="密码" required>
      <el-input type="password" v-model="form.password" autocomplete="off" />
    </el-form-item>
    <el-form-item>
      <el-button type="success" @click="submitRegister">注册</el-button>
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
  email: '',
  password: ''
})

const submitRegister = async () => {
  if (!form.value.username || !form.value.email || !form.value.password) {
    ElMessage.warning('请填写完整信息')
    return
  }
  try {
    await axios.post('http://localhost:8000/api/user/register/', form.value)
    ElMessage.success('注册成功，返回首页')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.response?.data?.username?.[0] || error.response?.data?.email?.[0] || '注册失败')
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
