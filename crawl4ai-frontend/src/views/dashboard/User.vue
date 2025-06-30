<template>
  <div class="user-info-container">
    <el-card shadow="hover" class="user-card">
      <div class="card-content">
        <div class="avatar-section">
          <el-avatar :size="120" :src="avatarUrl" class="avatar">
            <span class="avatar-text">{{ username ? username.charAt(0).toUpperCase() : 'U' }}</span>
          </el-avatar>
          <div class="status-indicator" :class="{'online': isOnline}"></div>
        </div>

        <div class="user-details">
          <h2 class="username">{{ username || '加载中...' }}</h2>
          <p class="email">
            <el-icon><Message /></el-icon>
            <span>{{ email || '加载中...' }}</span>
          </p>


        </div>
      </div>

      <div class="action-buttons">
        <el-button type="primary" plain round @click="editProfile">
          <el-icon><Edit /></el-icon>
          <span>编辑资料</span>
        </el-button>
        <el-button type="danger" plain round @click="logout">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  ElAvatar, ElButton, ElCard, ElIcon, ElMessage
} from 'element-plus'
import {
  Message, Calendar, Clock, Edit, SwitchButton
} from '@element-plus/icons-vue'

const username = ref('')
const email = ref('')
const joinDate = ref('')
const lastLogin = ref('')
const isOnline = ref(true)
const avatarUrl = ref('')
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  try {
    const res = await axios.get('http://localhost:8000/api/user/profile/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    username.value = res.data.username
    email.value = res.data.email
    joinDate.value = formatDate(res.data.date_joined)
    lastLogin.value = formatDate(res.data.last_login)

    // 模拟在线状态
    isOnline.value = Math.random() > 0.5
  } catch (err) {
    console.error('获取用户信息失败：', err)
    ElMessage.error('获取用户信息失败')
  }
})

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const editProfile = () => {
  ElMessage.info('编辑资料功能即将上线')
}

const logout = () => {
  localStorage.removeItem('access_token')
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.user-info-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.user-card {
  width: 100%;
  max-width: 600px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: none;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 30px 30px;
}

.avatar-section {
  position: relative;
  margin-bottom: 25px;
}

.avatar {
  background: linear-gradient(45deg, #409EFF, #67C23A);
  font-size: 48px;
  font-weight: bold;
  color: white;
  transition: all 0.3s ease;
}

.avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(64, 158, 255, 0.4);
}

.avatar-text {
  font-size: 48px;
}

.status-indicator {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  border: 3px solid white;
}

.status-indicator.online {
  background-color: #67C23A;
}

.status-indicator.offline {
  background-color: #909399;
}

.user-details {
  text-align: center;
  width: 100%;
}

.username {
  margin: 0 0 10px;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  letter-spacing: 0.5px;
}

.email {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 0 0 25px;
  font-size: 16px;
  color: #606266;
}

.stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
  padding: 15px 0;
  border-top: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #909399;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 20px;
  background-color: #f5f7fa;
  border-top: 1px solid #ebeef5;
}

.action-buttons .el-button {
  padding: 10px 20px;
  font-weight: 500;
}

.action-buttons .el-button span {
  margin-left: 6px;
}

@media (max-width: 768px) {
  .user-card {
    max-width: 90%;
  }

  .card-content {
    padding: 30px 20px;
  }

  .username {
    font-size: 24px;
  }

  .stats {
    flex-direction: column;
    gap: 12px;
  }

  .action-buttons {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
