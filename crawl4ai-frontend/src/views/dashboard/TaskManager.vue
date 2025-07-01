<template>
  <div class="task-manager-container">
    <div class="header-section">
      <h2 class="page-title">爬取任务管理</h2>
      <div class="controls">
        <button @click="fetchTasks" class="refresh-button">
          <span class="icon">↻</span> 刷新列表
        </button>
      </div>
    </div>

    <div class="table-responsive">
      <table class="task-table">
        <thead>
          <tr>
            <th class="url-col">网址</th>
            <th class="keyword-col">任务描述</th>
            <th class="depth-col">深度</th>
            <th class="strategy-col">策略</th>
            <th class="external-col">外链</th>
            <th class="status-col">状态</th>
            <th class="progress-col">进度</th>
            <th class="actions-col">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id" :class="`status-${task.status}`">
            <!-- URL -->
            <td>
              <input
                v-model.trim="task.url"
                :disabled="task.status === 'running'"
                class="table-input"
                placeholder="https://example.com"
              />
            </td>

            <!-- 关键词 -->
            <td>
              <input
                v-model.trim="task.keyword"
                :disabled="task.status === 'running'"
                class="table-input"
                placeholder="关键词1, 关键词2"
              />
            </td>

            <!-- 深度 -->
            <td>
              <input
                v-model.number="task.max_depth"
                type="number"
                min="1"
                max="10"
                :disabled="task.status === 'running'"
                class="table-input number-input"
              />
            </td>

            <!-- 策略 -->
            <td>
              <select
                v-model="task.strategy"
                :disabled="task.status === 'running'"
                class="table-select"
              >
                <option value="bfs">BFS</option>
                <option value="dfs">DFS</option>
                <option value="bestfirst">智能优先</option>
              </select>
            </td>

            <!-- 外链 -->
            <td class="text-center">
              <input
                type="checkbox"
                v-model="task.include_external"
                :disabled="task.status === 'running'"
                class="table-checkbox"
              />
            </td>

            <!-- 状态 -->
            <td>
              <span class="status-badge" :class="task.status">
                {{ getStatusText(task.status) }}
              </span>
            </td>

            <!-- 进度 -->
            <td>
              <div v-if="task.status === 'running'" class="progress-container">
                <div class="progress-bar" :style="{ width: task.progress + '%' }"></div>
                <span class="progress-text">{{ task.progress }}%</span>
              </div>
              <div v-else class="progress-empty">-</div>
            </td>

            <!-- 操作 -->
            <td class="actions">
              <button
                @click="updateTask(task)"
                :disabled="task.status === 'running' || task.isStarting"
                class="action-button save-button"
              >
                保存
              </button>
              <button
                @click="startTask(task)"
                :disabled="task.status !== 'pending' || task.isStarting"
                class="action-button start-button"
              >
                <span v-if="task.isStarting" class="loading-text">
                  <span class="spinner">⏳</span> 启动中
                </span>
                <span v-else>启动</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="tasks.length === 0" class="empty-state">
      <p>暂无任务数据</p>
      <button @click="fetchTasks" class="refresh-button">刷新列表</button>
    </div>

    <div v-if="loading" class="loading-overlay">
      <div class="spinner">⏳</div>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const tasks = ref([])
const loading = ref(false)
const pollingTimers = ref({})

const statusTextMap = {
  pending: '等待中',
  running: '运行中',
  completed: '已完成',
  failed: '失败',
  paused: '已暂停'
}

const getStatusText = (status) => {
  return statusTextMap[status] || status
}

const fetchTasks = async () => {
  loading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/tasks/', { timeout: 5000 })
    if (Array.isArray(response.data)) {
      tasks.value = response.data.map(task => ({
        ...task,
        progress: task.progress || 0,
        isStarting: false
      }))
      // 为所有运行中的任务启动轮询
      tasks.value.filter(t => t.status === 'running').forEach(pollProgress)
    }
  } catch (e) {
    console.error('获取任务失败:', e)
  } finally {
    loading.value = false
  }
}

const updateTask = async (task) => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/tasks/${task.id}/`, task)
    showToast('任务更新成功', 'success')
  } catch (e) {
    showToast(`任务更新失败: ${e.response?.data?.error || e.message}`, 'error')
  }
}

const startTask = async (task) => {
  if (task.isStarting || task.status !== 'pending') return
  task.isStarting = true

  try {
    await axios.post(`http://127.0.0.1:8000/api/tasks/${task.id}/start/`, null, { timeout: 10000 })
    task.status = 'running'
    task.progress = 0
    await pollProgress(task)
    pollingTimers.value[task.id] = setInterval(() => pollProgress(task), 2000)
  } catch (e) {
    showToast(`启动任务失败: ${e.response?.data?.detail || e.message}`, 'error')
  } finally {
    task.isStarting = false
  }
}

const pollProgress = async (task) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/tasks/${task.id}/progress/`, { timeout: 5000 })
    const data = response.data
    if (typeof data.progress === 'number') task.progress = data.progress
    if (typeof data.status === 'string') task.status = data.status

    if (task.status !== 'running' && pollingTimers.value[task.id]) {
      clearInterval(pollingTimers.value[task.id])
      delete pollingTimers.value[task.id]
    }
  } catch (e) {
    console.error("查询任务进度失败", e)
    if (pollingTimers.value[task.id]) {
      clearInterval(pollingTimers.value[task.id])
      delete pollingTimers.value[task.id]
    }
  }
}

const showToast = (message, type = 'info') => {
  // 这里可以替换为更完善的通知系统
  alert(`${type.toUpperCase()}: ${message}`)
}

onMounted(() => {
  fetchTasks()
  // 清理定时器
  return () => {
    Object.values(pollingTimers.value).forEach(timer => clearInterval(timer))
  }
})
</script>

<style scoped>
.task-manager-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  color: #2c3e50;
  margin: 0;
}

.refresh-button {
  padding: 8px 16px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.refresh-button:hover {
  background-color: #e9ecef;
}

.table-responsive {
  overflow-x: auto;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.task-table th {
  background-color: #f8f9fa;
  padding: 12px 8px;
  text-align: left;
  font-weight: 500;
  color: #495057;
  border-bottom: 2px solid #dee2e6;
}

.task-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #e9ecef;
  vertical-align: middle;
}

.task-table tr:hover {
  background-color: #f8f9fa;
}

.table-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 13px;
}

.table-input:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.number-input {
  width: 60px;
}

.table-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 13px;
  background-color: white;
}

.table-checkbox {
  width: 16px;
  height: 16px;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
  min-width: 60px;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.running {
  background-color: #cce5ff;
  color: #004085;
}

.status-badge.completed {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.failed {
  background-color: #f8d7da;
  color: #721c24;
}

.progress-container {
  position: relative;
  height: 24px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #4dabf7;
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 12px;
  color: #fff;
  text-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}

.progress-empty {
  color: #adb5bd;
}

.actions {
  display: flex;
  gap: 8px;
}

.action-button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.save-button {
  background-color: #e2e3e5;
  color: #383d41;
}

.save-button:hover:not(:disabled) {
  background-color: #d6d8db;
}

.start-button {
  background-color: #d4edda;
  color: #155724;
}

.start-button:hover:not(:disabled) {
  background-color: #c3e6cb;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 4px;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 40px 0;
  color: #6c757d;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-overlay .spinner {
  font-size: 40px;
  margin-bottom: 16px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .actions {
    flex-direction: column;
  }

  .action-button {
    width: 100%;
  }
}
</style>