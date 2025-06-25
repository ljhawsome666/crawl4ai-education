<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <el-icon :size="36" color="#67C23A"><Collection /></el-icon>
        <h2>创建新账户</h2>
        <p>加入数据爬虫平台，开启您的数据采集之旅</p>
      </div>

      <el-form :model="form" class="auth-form" @submit.prevent="submitRegister">
        <el-form-item>
          <el-input
            v-model="form.username"
            placeholder="用户名"
            size="large"
            :prefix-icon="User"
          />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.email"
            placeholder="电子邮箱"
            size="large"
            :prefix-icon="Message"
          />
        </el-form-item>
        <el-form-item>
          <el-input
            type="password"
            v-model="form.password"
            placeholder="密码"
            size="large"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <div class="form-actions">
          <el-button
            type="success"
            size="large"
            native-type="submit"
            class="submit-btn"
          >
            注册
          </el-button>

          <div class="auth-links">
            <el-link type="info" @click="goLogin">已有账号？立即登录</el-link>
          </div>
        </div>
      </el-form>

      <div class="terms">
        <el-checkbox v-model="agreeTerms">我已阅读并同意</el-checkbox>
        <el-link type="primary" :underline="false">服务条款</el-link>
        <span>和</span>
        <el-link type="primary" :underline="false">隐私政策</el-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import {
  User, Message, Lock, Collection
} from '@element-plus/icons-vue'

const router = useRouter()
const form = ref({
  username: '',
  email: '',
  password: ''
})
const agreeTerms = ref(false)

const submitRegister = async () => {
  if (!form.value.username || !form.value.email || !form.value.password) {
    ElMessage.warning('请填写完整信息')
    return
  }

  if (!agreeTerms.value) {
    ElMessage.warning('请阅读并同意服务条款和隐私政策')
    return
  }

  try {
    await axios.post('http://localhost:8000/api/user/register/', form.value)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    ElMessage.error(error.response?.data?.username?.[0] || error.response?.data?.email?.[0] || '注册失败')
  }
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8f9fa;
  background-image: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 40px;
  transition: all 0.3s ease;
}

.auth-card:hover {
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h2 {
  font-size: 1.8rem;
  color: #333;
  margin: 15px 0 8px;
}

.auth-header p {
  color: #666;
  font-size: 0.95rem;
}

.auth-form {
  margin-top: 30px;
}

.submit-btn {
  width: 100%;
  margin-top: 10px;
  font-size: 1rem;
  padding: 15px;
}

.auth-links {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  font-size: 0.9rem;
}

.terms {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 30px;
  font-size: 0.9rem;
  color: #666;
  flex-wrap: wrap;
  gap: 5px;
}

:deep(.el-input__wrapper) {
  padding: 5px 15px;
}

:deep(.el-input__prefix-inner) {
  margin-right: 10px;
}
</style>