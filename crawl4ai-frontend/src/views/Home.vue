<template>
  <div class="page-container">
    <!-- 头部导航栏 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <el-icon :size="28" color="#409EFF"><Collection /></el-icon>
          <span class="logo-text">数据爬虫平台</span>
        </div>
        <div class="nav-links">
          <el-link type="primary" :underline="false">首页</el-link>
          <el-link type="info" :underline="false">产品功能</el-link>
          <el-link type="info" :underline="false">使用文档</el-link>
          <el-link type="info" :underline="false">价格方案</el-link>
          <el-link type="info" :underline="false">联系我们</el-link>
        </div>
        <div class="user-actions">
          <el-button type="primary" @click="goLogin" size="small" plain>登录</el-button>
          <el-button type="success" @click="goRegister" size="small">注册</el-button>
        </div>
      </div>
    </el-header>

    <!-- 主体内容 -->
    <el-main class="main-content">
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="title">专业级网络数据采集平台</h1>
          <p class="subtitle">提供高效、稳定、智能的网络爬虫解决方案，助力您的数据驱动业务</p>

          <div class="action-buttons">
            <el-button
              type="primary"
              @click="goLogin"
              size="large"
              class="action-button"
            >
              <span class="button-content">
                <el-icon><User /></el-icon>
                立即开始
              </span>
            </el-button>

            <el-button
              type="info"
              size="large"
              class="action-button"
              plain
            >
              <span class="button-content">
                <el-icon><VideoPlay /></el-icon>
                观看演示
              </span>
            </el-button>
          </div>
        </div>
      </div>

      <div class="features-section">
        <h2 class="section-title">核心功能</h2>
        <p class="section-subtitle">我们提供全方位的网络数据采集与管理功能</p>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48" color="#409EFF"><MagicStick /></el-icon>
            </div>
            <h3>智能爬取</h3>
            <p>基于AI的智能识别技术，自动适应各种网页结构变化</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48" color="#67C23A"><Cpu /></el-icon>
            </div>
            <h3>高性能处理</h3>
            <p>分布式架构支持，每秒可处理数千页面请求</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48" color="#E6A23C"><DataLine /></el-icon>
            </div>
            <h3>数据可视化</h3>
            <p>直观的数据展示与分析图表，洞察数据价值</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48" color="#F56C6C"><AlarmClock /></el-icon>
            </div>
            <h3>定时任务</h3>
            <p>灵活配置定时采集任务，自动获取最新数据</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48" color="#909399"><Lock /></el-icon>
            </div>
            <h3>安全防护</h3>
            <p>完善的防封禁机制，保障爬虫稳定运行</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <el-icon :size="48" color="#8E44AD"><Download /></el-icon>
            </div>
            <h3>多种导出</h3>
            <p>支持CSV、Excel、JSON等多种数据导出格式</p>
          </div>
        </div>
      </div>

      <div class="use-cases-section">
        <h2 class="section-title">应用场景</h2>
        <p class="section-subtitle">我们的解决方案适用于各种行业需求</p>

        <el-carousel :interval="4000" type="card" height="400px">
          <el-carousel-item v-for="item in useCases" :key="item.title">
            <div class="case-card">
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
              <el-icon :size="36"><component :is="item.icon" /></el-icon>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>
    </el-main>

    <!-- 页脚 -->
    <el-footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h4>产品</h4>
          <el-link type="info" :underline="false">功能特性</el-link>
          <el-link type="info" :underline="false">价格方案</el-link>
          <el-link type="info" :underline="false">更新日志</el-link>
        </div>

        <div class="footer-section">
          <h4>资源</h4>
          <el-link type="info" :underline="false">文档中心</el-link>
          <el-link type="info" :underline="false">API接口</el-link>
          <el-link type="info" :underline="false">帮助中心</el-link>
        </div>

        <div class="footer-section">
          <h4>公司</h4>
          <el-link type="info" :underline="false">关于我们</el-link>
          <el-link type="info" :underline="false">联系我们</el-link>
          <el-link type="info" :underline="false">加入我们</el-link>
        </div>

        <div class="footer-section">
          <h4>联系我们</h4>
          <p><el-icon><Message /></el-icon> kalve089@gmail.com</p>
          <p><el-icon><Iphone /></el-icon> 400-123-4567</p>
          <div class="social-links">
            <el-icon :size="24"><ChatDotRound /></el-icon>
            <el-icon :size="24"><ChatLineRound /></el-icon>
            <el-icon :size="24"><Platform /></el-icon>
          </div>
        </div>
      </div>

      <div class="copyright">
        <p>© 2025 数据爬虫平台 版权所有 | 隐私政策 | 服务条款</p>
      </div>
    </el-footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import {
  User, VideoPlay, Collection, MagicStick,
  Cpu, DataLine, AlarmClock, Lock,
  Download, Message, Iphone, ChatDotRound,
  ChatLineRound, Platform
} from '@element-plus/icons-vue'
import { ref } from 'vue'

const router = useRouter()
const goLogin = () => {
  router.push('/login')
}
const goRegister = () => {
  router.push('/register')
}

const useCases = ref([
  {
    title: '电商价格监控',
    description: '实时监控竞品价格变化，制定最优定价策略',
    icon: 'ShoppingCart'
  },
  {
    title: '舆情分析',
    description: '采集社交媒体数据，分析公众舆论趋势',
    icon: 'Comment'
  },
  {
    title: '金融数据采集',
    description: '获取金融市场数据，支持投资决策分析',
    icon: 'TrendCharts'
  },
  {
    title: '学术研究',
    description: '收集学术文献数据，支持科研分析',
    icon: 'Notebook'
  },
  {
    title: '招聘数据分析',
    description: '分析招聘市场趋势，了解人才需求变化',
    icon: 'UserFilled'
  }
])
</script>

<style scoped>
/* 基础样式重置 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* 主容器 - 添加渐变背景 */
.page-container {
  background: linear-gradient(135deg,
    #56ccf2 0%,
    #2f80ed 50%,
    #1fa2ff 100%);
  background-attachment: fixed;
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  aspect-ratio: 16/9;
  overflow: auto;
  position: absolute;
  right: 0;
  top: 0;
}

/* 头部样式 */
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
}

.logo-text {
  background: linear-gradient(90deg, #409EFF, #67C23A);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.user-actions {
  display: flex;
  gap: 10px;
}

/* 主体内容 */
.main-content {
  flex: 1;
  padding: 0;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.85);
}

/* 英雄区域 - 减少底部padding */
.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 100px 40px 30px; /* 底部padding从60px减少到30px */
  min-height: calc(100% - 80px - 30px); /* 同步调整 */
  box-sizing: border-box;
  flex-grow: 1;
  background: transparent;
}

.title {
  font-size: 3.2rem;
  color: #2c3e50;
  margin-bottom: 24px;
  font-weight: 600;
  line-height: 1.2;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 1.4rem;
  color: #34495e;
  margin-bottom: 50px;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 40px;
}

.action-button {
  padding: 18px 36px;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.button-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 核心功能区域 - 减少上边距 */
.features-section {
  max-width: 1400px;
  margin: 30px auto 0; /* 上边距从60px减少到30px */
  padding: 0 40px;
  text-align: center;
  background: transparent;
}

.section-title {
  font-size: 2.4rem;
  color: #2c3e50;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-subtitle {
  font-size: 1.2rem;
  color: #34495e;
  margin-bottom: 30px; /* 从60px减少到30px */
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 40px;
  margin-top: 30px; /* 可选：减少网格上边距 */
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(5px);
  padding: 50px 40px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  margin-bottom: 25px;
}

.feature-card h3 {
  margin: 0 0 20px;
  color: #333;
  font-size: 1.5rem;
}

.feature-card p {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
}

/* 应用场景区域 */
.use-cases-section {
  max-width: 1400px;
  margin: 100px auto;
  padding: 0 40px;
  text-align: center;
  background: transparent;
}

.case-card {
  height: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(5px);
  padding: 40px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.case-card h3 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #333;
}

.case-card p {
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1rem;
  line-height: 1.6;
}

/* 页脚 */
.footer {
  background-color: #2c3e50;
  color: white;
  padding: 80px 0 0;
  flex-shrink: 0;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 50px;
  padding: 0 40px;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.footer-section h4 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #fff;
}

.footer-section p {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #bdc3c7;
  margin: 8px 0;
  font-size: 1.05rem;
}

.social-links {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.copyright {
  text-align: center;
  padding: 30px;
  margin-top: 60px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #bdc3c7;
  font-size: 1rem;
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .header-content,
  .hero-section,
  .features-section,
  .use-cases-section,
  .footer-content {
    padding-left: 30px;
    padding-right: 30px;
  }

  .title {
    font-size: 2.8rem;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .page-container {
    background: linear-gradient(135deg,
      #56ccf2 0%,
      #2f80ed 70%,
      #1fa2ff 100%);
  }

  .main-content {
    background: rgba(255, 255, 255, 0.92);
  }

  .header-content {
    flex-direction: column;
    height: auto;
    padding: 20px;
  }

  .nav-links {
    margin: 20px 0;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }

  .title {
    font-size: 2.2rem;
  }

  .subtitle {
    font-size: 1.1rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 15px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .hero-section {
    padding: 80px 20px 20px; /* 移动端减少底部padding */
    height: auto;
    min-height: auto;
  }

  .features-section {
    margin: 20px auto 0; /* 移动端进一步减少上边距 */
  }

  .section-subtitle {
    margin-bottom: 20px; /* 移动端减少下边距 */
  }

  .feature-card,
  .case-card {
    padding: 30px 20px;
  }

  .footer-content {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 60px 15px 15px; /* 小屏幕进一步减少 */
  }

  .features-section {
    margin: 15px auto 0;
  }

  .footer-content {
    grid-template-columns: 1fr;
  }

  .title {
    font-size: 1.8rem;
  }

  .section-title {
    font-size: 1.8rem;
  }
}
</style>
