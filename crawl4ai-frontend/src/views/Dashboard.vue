<template>
  <div class="page-container">
    <!-- 头部导航栏 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo" @click="goHome">
          <el-icon :size="28" color="#409EFF"><Collection /></el-icon>
          <span class="logo-text">数据爬虫平台</span>
          <div class="logo-glow"></div>
        </div>
        <div class="nav-actions">
          <el-button
            type="primary"
            class="home-btn"
            @click="goHome"
          >
            <el-icon class="btn-icon"><HomeFilled /></el-icon>
            <span class="btn-text">返回首页</span>
            <span class="btn-ripple"></span>
          </el-button>
        </div>
      </div>
    </el-header>

    <div class="dashboard-layout">
      <aside class="sidebar">
        <div class="sidebar-header">
          <h3>功能导航</h3>
          <div class="sidebar-divider"></div>
        </div>
        <ul class="menu-list">
          <li v-for="item in menuItems" :key="item.name">
            <router-link
              :to="item.route"
              class="nav-link"
              active-class="active"
            >
              <div class="nav-link-content">
                <div class="menu-icon-wrapper">
                  <el-icon class="menu-icon">
                    <component :is="item.icon" />
                  </el-icon>
                </div>
                <span class="menu-text">{{ item.name }}</span>
              </div>
              <div class="link-highlight"></div>
              <div class="link-wave"></div>
            </router-link>
          </li>
        </ul>
      </aside>

      <el-main class="main-content">
        <router-view />
      </el-main>
    </div>

    <!-- 页脚 -->
    <el-footer class="footer">
      <div class="copyright">
        <p>© 2025 数据爬虫平台 版权所有 | 隐私政策 | 服务条款</p>
      </div>
    </el-footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import {
  Collection, HomeFilled,
  User, DocumentAdd, List, Files, Clock
} from '@element-plus/icons-vue'

const router = useRouter()

const menuItems = [
  { name: '用户中心', route: '/dashboard/user', icon: 'User' },
  { name: '新建任务', route: '/dashboard/createTask', icon: 'DocumentAdd' },
  { name: '任务管理', route: '/dashboard/task', icon: 'List' },
  { name: '模板库', route: '/dashboard/case', icon: 'Files' },
  { name: '历史记录', route: '/dashboard/dataShowcase', icon: 'Clock' }
]

const goHome = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
/* 全局样式优化 */
.page-container {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg,
    rgba(86, 204, 242, 0.1) 0%,
    rgba(47, 128, 237, 0.15) 50%,
    rgba(31, 162, 255, 0.1) 100%);
  background-attachment: fixed;
  overflow: auto;
  position: absolute;
  right: 0;
  top: 0;
}

/* 头部导航栏优化 */
.header {
  background: linear-gradient(to right,
    rgba(255, 255, 255, 0.98) 0%,
    rgba(255, 255, 255, 0.95) 100%);
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
  height: 80px;
  display: flex;
  align-items: center;
  flex-shrink: 0;
  backdrop-filter: blur(5px);
  z-index: 10;
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
  transition: all 0.3s ease;
  position: relative;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(64, 158, 255, 0.2) 0%, transparent 70%);
  transform: translateY(-50%) scale(0.9);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo:hover .logo-glow {
  opacity: 1;
}

.logo-text {
  background: linear-gradient(90deg, #409EFF, #67C23A);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
}

/* 返回首页按钮优化 */
.home-btn {
  position: relative;
  padding: 10px 20px;
  border-radius: 30px;
  font-weight: 500;
  transition: all 0.4s cubic-bezier(0.2, 0.8, 0.4, 1);
  overflow: hidden;
  border: none;
  background: linear-gradient(135deg, #409EFF, #67C23A);
  color: white;
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.3);
}

.home-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.4);
}

.home-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.btn-ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 100%;
  transform: scale(1) translate(-50%, -50%);
  opacity: 0;
}

.home-btn:hover .btn-ripple {
  animation: ripple 1s ease-out;
}

@keyframes ripple {
  0% {
    transform: scale(0) translate(-50%, -50%);
    opacity: 1;
  }
  100% {
    transform: scale(20) translate(-50%, -50%);
    opacity: 0;
  }
}

.btn-icon {
  margin-right: 8px;
  font-size: 16px;
  transition: transform 0.3s ease;
}

.home-btn:hover .btn-icon {
  transform: translateX(2px);
}

/* 侧边栏优化 */
.dashboard-layout {
  display: flex;
  flex: 1;
  background: rgba(255, 255, 255, 0.85);
}

.sidebar {
  width: 220px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.05);
  padding: 0;
  backdrop-filter: blur(5px);
  z-index: 5;
}

.sidebar-header {
  padding: 24px 24px 16px;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #303133;
  letter-spacing: 0.5px;
  position: relative;
}

.sidebar-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(0, 0, 0, 0.1), transparent);
  margin-top: 12px;
}

.menu-list {
  list-style: none;
  padding: 12px 0;
  margin: 0;
}

/* 导航按钮优化 */
.nav-link {
  display: block;
  margin: 6px 12px;
  color: #2c3e50;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.4s cubic-bezier(0.2, 0.8, 0.4, 1);
  position: relative;
  overflow: hidden;
}

.nav-link-content {
  display: flex;
  align-items: center;
  padding: 14px 24px;
  position: relative;
  z-index: 3;
}

.link-wave {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(64, 158, 255, 0.1) 0%, transparent 70%);
  transform: scale(0);
  opacity: 0;
  transition: transform 0.6s ease, opacity 0.6s ease;
}

.nav-link:hover {
  background-color: rgba(64, 158, 255, 0.05);
  color: #409EFF;
  transform: translateX(4px);
}

.nav-link:hover .link-wave {
  transform: scale(1);
  opacity: 1;
}

.nav-link:hover .menu-icon {
  color: #409EFF;
  transform: scale(1.1);
}

.active {
  background-color: rgba(64, 158, 255, 0.08);
  color: #409EFF;
  font-weight: 500;
}

.active .menu-icon {
  color: #409EFF;
}

.link-highlight {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, #409EFF, #67C23A);
  transform: scaleY(0);
  transform-origin: top;
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.4, 1);
}

.active .link-highlight,
.nav-link:hover .link-highlight {
  transform: scaleY(1);
}

.menu-icon-wrapper {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  transition: all 0.3s ease;
}

.menu-icon {
  flex-shrink: 0;
  color: #606266;
  transition: all 0.3s ease;
  font-size: 18px;
}

.menu-text {
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
  flex: 1;
}

.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  background: transparent;
}

/* 页脚优化 */
.footer {
  background: linear-gradient(to right, #2c3e50, #34495e);
  color: white;
  padding: 30px 0;
  flex-shrink: 0;
}

.copyright {
  text-align: center;
  color: rgba(189, 195, 199, 0.8);
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }

  .nav-link-content {
    padding: 12px 20px;
  }

  .main-content {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .dashboard-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    padding: 0;
  }

  .menu-list {
    display: flex;
    overflow-x: auto;
    padding: 8px;
  }

  .nav-link {
    margin: 0 6px;
    min-width: 120px;
  }

  .nav-link-content {
    padding: 10px 16px;
  }

  .menu-icon {
    margin-right: 8px;
    font-size: 16px;
  }

  .home-btn {
    padding: 8px 12px;
    font-size: 0.85rem;
  }
}
</style>
