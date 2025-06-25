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

        <div class="preview-image">
          <img src="https://via.placeholder.com/800x450?text=Dashboard+Preview" alt="平台预览">
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

        <el-carousel :interval="4000" type="card" height="300px">
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
          <p><el-icon><Message /></el-icon> support@spider.com</p>
          <p><el-icon><Iphone /></el-icon> 400-123-4567</p>
          <div class="social-links">
            <el-icon :size="24"><ChatDotRound /></el-icon>
            <el-icon :size="24"><ChatLineRound /></el-icon>
            <el-icon :size="24"><Platform /></el-icon>
          </div>
        </div>
      </div>

      <div class="copyright">
        <p>© 2023 数据爬虫平台 版权所有 | 隐私政策 | 服务条款</p>
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
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.header {
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: 60px;
  display: flex;
  align-items: center;
}

.header-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.2rem;
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
  gap: 30px;
}

.user-actions {
  display: flex;
  gap: 10px;
}

.main-content {
  flex: 1;
  padding: 0;
}

.hero-section {
  max-width: 1200px;
  margin: 40px auto;
  text-align: center;
  padding: 60px 20px;
}

.title {
  font-size: 2.8rem;
  color: #333;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.2;
}

.subtitle {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 40px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.action-button {
  padding: 15px 30px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.button-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.preview-image {
  margin-top: 60px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.preview-image img {
  width: 100%;
  height: auto;
  display: block;
}

.features-section {
  max-width: 1200px;
  margin: 80px auto;
  padding: 0 20px;
  text-align: center;
}

.section-title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 50px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.feature-card {
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  margin-bottom: 20px;
}

.feature-card h3 {
  margin: 0 0 15px;
  color: #333;
  font-size: 1.3rem;
}

.feature-card p {
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
}

.use-cases-section {
  max-width: 1200px;
  margin: 80px auto;
  padding: 0 20px;
  text-align: center;
}

.case-card {
  height: 100%;
  background: white;
  padding: 30px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.case-card h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
}

.case-card p {
  color: #666;
  margin-bottom: 20px;
}

.footer {
  background-color: #2c3e50;
  color: white;
  padding: 60px 0 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  padding: 0 20px;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.footer-section h4 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #fff;
}

.footer-section p {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #bdc3c7;
  margin: 5px 0;
}

.social-links {
  display: flex;
  gap: 15px;
  margin-top: 15px;
}

.copyright {
  text-align: center;
  padding: 20px;
  margin-top: 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #bdc3c7;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 15px;
  }

  .nav-links {
    margin: 15px 0;
    flex-wrap: wrap;
    justify-content: center;
  }

  .title {
    font-size: 2rem;
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
}
</style>