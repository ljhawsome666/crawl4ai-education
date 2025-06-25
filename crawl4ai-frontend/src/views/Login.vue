<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <el-icon :size="36" color="#409EFF"><Collection /></el-icon>
        <h2>欢迎回来</h2>
        <p>请登录您的数据爬虫平台账户</p>
      </div>

      <el-form :model="form" class="auth-form" @submit.prevent="submitLogin">
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
            type="primary"
            size="large"
            native-type="submit"
            class="submit-btn"
          >
            登录
          </el-button>

          <div class="auth-links">
            <el-link type="info" @click="goRegister">没有账号？立即注册</el-link>
            <el-link type="info" @click="goForgotPassword">忘记密码？</el-link>
          </div>
        </div>
      </el-form>

      <div class="auth-footer">
        <el-divider>其他登录方式</el-divider>
        <div class="social-login">
          <el-icon :size="24"><Platform /></el-icon>
          <el-icon :size="24"><ChatLineRound /></el-icon>
          <el-icon :size="24"><ChatDotRound /></el-icon>
        </div>
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
  User, Lock, Collection,
  Platform, ChatLineRound, ChatDotRound
} from '@element-plus/icons-vue'

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

const goRegister = () => {
  router.push('/register')
}

const goForgotPassword = () => {
  // 跳转到忘记密码页面
  console.log('跳转到忘记密码页面')
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
  justify-content: space-between;
  margin-top: 20px;
  font-size: 0.9rem;
}

.auth-footer {
  margin-top: 30px;
}

.social-login {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
  color: #666;
}

.social-login .el-icon {
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-login .el-icon:hover {
  color: #409EFF;
  transform: translateY(-3px);
}

:deep(.el-input__wrapper) {
  padding: 5px 15px;
}

:deep(.el-input__prefix-inner) {
  margin-right: 10px;
}
</style>