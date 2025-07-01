<template>
  <div class="history-container">
    <!-- 头部区域 -->
    <div class="history-header">
      <div class="header-content">
        <h1 class="page-title">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          历史记录
        </h1>
        <p class="page-subtitle">查看您的爬取历史记录</p>
      </div>
      <div class="header-actions">
        <button @click="refreshData" class="refresh-btn">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          刷新
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </div>
      <p class="loading-text">正在加载历史数据...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <div class="error-content">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h3 class="error-title">加载失败</h3>
        <p class="error-message">{{ error }}</p>
        <button @click="refreshData" class="retry-btn">
          重试
        </button>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else-if="showcases.length === 0" class="empty-state">
      <div class="empty-content">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="empty-title">暂无历史记录</h3>
        <p class="empty-message">您还没有任何爬取记录，开始一个新的爬取任务吧</p>
        <button @click="$router.push('/new-task')" class="new-task-btn">
          新建爬取任务
        </button>
      </div>
    </div>

    <!-- 内容展示 -->
    <div v-else class="history-grid">
      <div v-for="(item, index) in showcases" :key="index" class="history-card">
        <!-- 卡片头部 -->
        <div class="card-header">
          <span class="keyword-tag" :style="{ backgroundColor: getTagColor(item.keyword) }">
            {{ item.keyword }}
          </span>
          <span class="card-date">{{ formatDate(item.created_at) }}</span>
        </div>

        <!-- 内容区域 -->
        <div class="card-content">
          <a :href="item.url" target="_blank" rel="noopener noreferrer" class="content-link">
            <h3 class="content-title">{{ getDomainFromUrl(item.url) }}</h3>
            <p class="content-url">{{ item.url }}</p>
          </a>

          <div class="content-preview">
            <p>{{ item.content_preview }}</p>
            <div class="fade-out"></div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="card-actions">
          <button @click="copyUrl(item.url)" class="action-btn copy-btn">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
            </svg>
            复制链接
          </button>

          <button @click="showDetail(item)" class="action-btn detail-btn">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            查看详情
          </button>
        </div>
      </div>
    </div>

    <!-- 详情模态框 -->
    <div v-if="selectedItem" class="detail-modal" @click.self="selectedItem = null">
    <div class="modal-content">
      <div class="modal-header">
        <button @click="selectedItem = null" class="back-btn">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          返回
        </button>
        <h3 class="modal-title">{{ selectedItem.keyword }}</h3>
        <button @click="selectedItem = null" class="modal-close">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

        <div class="modal-body">
          <div class="modal-section">
            <h4 class="section-title">目标网址</h4>
            <a :href="selectedItem.url" target="_blank" rel="noopener noreferrer" class="section-content link">
              {{ selectedItem.url }}
            </a>
          </div>

          <div class="modal-section">
            <h4 class="section-title">爬取时间</h4>
            <p class="section-content">{{ formatDate(selectedItem.created_at, true) }}</p>
          </div>

          <div class="modal-section">
            <h4 class="section-title">内容预览</h4>
            <div class="content-preview full-content">
              {{ selectedItem.content_preview }}
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="copyUrl(selectedItem.url)" class="modal-btn copy-btn">
            复制链接
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showcases = ref([])
const loading = ref(true)
const error = ref('')
const selectedItem = ref(null)

function copyUrl(url) {
  navigator.clipboard.writeText(url).then(() => {
    alert('链接已复制到剪贴板')
  }, () => {
    alert('复制失败，请手动复制')
  })
}

function refreshData() {
  loading.value = true
  error.value = ''
  fetchData()
}

function showDetail(item) {
  selectedItem.value = item
}

function formatDate(dateString, withTime = false) {
  if (!dateString) return '2025-7-1'
  const date = new Date(dateString)
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  if (withTime) {
    options.hour = '2-digit'
    options.minute = '2-digit'
  }
  return date.toLocaleDateString('zh-CN', options)
}

function getDomainFromUrl(url) {
  try {
    const domain = new URL(url).hostname.replace('www.', '')
    return domain.charAt(0).toUpperCase() + domain.slice(1)
  } catch {
    return url.slice(0, 30) + (url.length > 30 ? '...' : '')
  }
}

function getTagColor(keyword) {
  const colors = [
    '#EFF6FF', '#DBEAFE', '#BFDBFE', '#93C5FD', '#60A5FA',
    '#3B82F6', '#2563EB', '#1D4ED8', '#1E40AF', '#1E3A8A'
  ]
  const hash = Array.from(keyword).reduce((acc, char) => char.charCodeAt(0) + acc, 0)
  return colors[hash % colors.length]
}

async function fetchData() {
  try {
    const res = await fetch('http://localhost:8000/api/showcase/')
    if (!res.ok) throw new Error(`加载失败：${res.status}`)
    showcases.value = await res.json()
  } catch (err) {
    error.value = err.message || '请求数据失败'
    console.error('获取历史记录失败:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.history-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: calc(100vh - 4rem);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e40af;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0;
}

.page-subtitle {
  color: #6b7280;
  margin-top: 0.5rem;
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #fff;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  color: #374151;
  font-weight: 500;
  transition: all 0.2s;
}

.refresh-btn:hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.refresh-btn svg {
  width: 1.25rem;
  height: 1.25rem;
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
}

.spinner {
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1rem;
  color: #6b7280;
  font-size: 1.125rem;
}

.error-content {
  max-width: 28rem;
}

.error-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-top: 1rem;
}

.error-message {
  color: #6b7280;
  margin-top: 0.5rem;
}

.retry-btn {
  margin-top: 1.5rem;
  padding: 0.5rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 0.2s;
}

.retry-btn:hover {
  background-color: #2563eb;
}

.empty-content {
  max-width: 28rem;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-top: 1rem;
}

.empty-message {
  color: #6b7280;
  margin-top: 0.5rem;
}

.new-task-btn {
  margin-top: 1.5rem;
  padding: 0.5rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 0.2s;
}

.new-task-btn:hover {
  background-color: #2563eb;
}

.history-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.history-card {
  background-color: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.history-card:hover {
  transform: translateY(-0.25rem);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.keyword-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #1e40af;
}

.card-date {
  font-size: 0.75rem;
  color: #6b7280;
}

.card-content {
  padding: 1.25rem;
  flex-grow: 1;
}

.content-link {
  display: block;
  margin-bottom: 1rem;
  text-decoration: none;
}

.content-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  line-height: 1.5;
}

.content-url {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
  word-break: break-all;
  line-height: 1.5;
}

.content-preview {
  position: relative;
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.7;
  max-height: 7.5rem;
  overflow: hidden;
}

.content-preview p {
  margin: 0;
}

.fade-out {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2.5rem;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));
}

.card-actions {
  display: flex;
  padding: 0.75rem 1.25rem;
  border-top: 1px solid #e5e7eb;
  background-color: #f9fafb;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.copy-btn {
  background-color: #eff6ff;
  color: #1d4ed8;
  margin-right: 0.75rem;
}

.copy-btn:hover {
  background-color: #dbeafe;
}

.detail-btn {
  background-color: #f8fafc;
  color: #4b5563;
}

.detail-btn:hover {
  background-color: #e5e7eb;
}

.action-btn svg {
  width: 1.25rem;
  height: 1.25rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f3f4f6;
  border-radius: 0.375rem;
  color: #4b5563;
  font-weight: 500;
  transition: all 0.2s;
  position: absolute;
  left: 1.5rem;
}

.back-btn:hover {
  background-color: #e5e7eb;
}

.modal-header {
  position: relative;
  padding-left: 5rem;
}

.detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.modal-content {
  background-color: white;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 48rem;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.modal-close {
  color: #6b7280;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
}

.modal-close:hover {
  color: #4b5563;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex-grow: 1;
}

.modal-section {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.section-content {
  font-size: 1rem;
  color: #1f2937;
  line-height: 1.7;
}

.link {
  color: #3b82f6;
  word-break: break-all;
}

.link:hover {
  text-decoration: underline;
}

.full-content {
  max-height: none;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  font-family: 'Noto Sans SC', sans-serif;
  line-height: 1.8;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.modal-btn {
  padding: 0.5rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.copy-btn {
  background-color: #3b82f6;
  color: white;
}

.copy-btn:hover {
  background-color: #2563eb;
}

@media (max-width: 640px) {
  .history-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .history-grid {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .copy-btn {
    margin-right: 0;
  }
}
</style>