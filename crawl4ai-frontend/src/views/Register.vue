<template>
  <div class="page-container">
    <!-- 头部导航栏 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo" @click="goHome">
          <el-icon :size="28" color="#409EFF"><Collection /></el-icon>
          <span class="logo-text">数据爬虫平台</span>
        </div>
        <div class="nav-actions">
          <el-link type="info" :underline="false" @click="goHome">返回首页</el-link>
        </div>
      </div>
    </el-header>

    <!-- 注册表单主体 -->
    <el-main class="main-content auth-main">
      <div class="auth-container">
        <div class="auth-card">
          <div class="auth-header">
            <el-icon :size="36" color="#67C23A"><Collection /></el-icon>
            <h2 class="auth-title">创建新账户</h2>
            <p class="auth-subtitle">加入数据爬虫平台，开启您的数据采集之旅</p>
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
                <span class="button-content">
                  <el-icon><User /></el-icon>
                  立即注册
                </span>
              </el-button>

              <div class="auth-links">
                <el-link type="info" :underline="false" @click="goLogin">已有账号？立即登录</el-link>
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
    </el-main>

    <!-- 页脚 -->
    <el-footer class="footer">
      <div class="copyright">
        <p>© 2025 数据爬虫平台 版权所有 | 隐私政策 | 服务条款</p>
      </div>
    </el-footer>
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

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
/* 保持与首页一致的全局样式 */
.page-container {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg,
    #56ccf2 0%,
    #2f80ed 50%,
    #1fa2ff 100%);
  background-attachment: fixed;
  overflow: auto;
  position: absolute;
  right: 0;
  top: 0;
}

.header {
  background-color: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: 80px;
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.header-content {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.4rem;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-text {
  background: linear-gradient(90deg, #409EFF, #67C23A);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-actions {
  display: flex;
  gap: 20px;
  align-items: center;
}

/* 注册页面特有样式 */
.auth-main {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
}

.auth-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 40px;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.auth-card:hover {
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin: 15px 0 8px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.auth-subtitle {
  color: #34495e;
  font-size: 1rem;
}

.auth-form {
  margin-top: 30px;
}

.submit-btn {
  width: 100%;
  margin-top: 10px;
  font-size: 1rem;
  padding: 15px;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.button-content {
  display: flex;
  align-items: center;
  gap: 10px;
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

/* 页脚样式保持与首页一致 */
.footer {
  background-color: #2c3e50;
  color: white;
  padding: 30px 0;
  flex-shrink: 0;
}

.copyright {
  text-align: center;
  color: #bdc3c7;
  font-size: 0.9rem;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .auth-card {
    padding: 30px 20px;
    max-width: 90%;
  }

  .auth-title {
    font-size: 1.6rem;
  }

  .header-content {
    padding: 0 20px;
  }
}

@media (max-width: 480px) {
  .auth-card {
    padding: 25px 15px;
  }

  .auth-title {
    font-size: 1.4rem;
  }

  .terms {
    flex-direction: column;
    align-items: center;
    gap: 5px;
  }
}
</style>
