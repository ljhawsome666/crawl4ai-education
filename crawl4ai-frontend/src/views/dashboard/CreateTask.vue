<template>
  <div class="task-form-container">
    <h2 class="form-title">新建爬取任务</h2>

    <form @submit.prevent="submitTask" class="task-form">
      <!-- URL 输入 -->
      <div class="form-group">
        <label for="url" class="form-label">目标网页 URL:</label>
        <input
          id="url"
          v-model.trim="form.url"
          type="url"
          required
          placeholder="https://example.com"
          class="form-input"
          :class="{ 'input-error': errors.url }"
          @input="clearError('url')"
        />
        <span v-if="errors.url" class="error-message">{{ errors.url }}</span>
      </div>

      <!-- 关键词输入 -->
      <div class="form-group">
        <label for="keywords" class="form-label">Instruction:</label>
        <input
          id="keywords"
          v-model.trim="form.raw_keyword"
          type="text"
          required
          placeholder="关键词1, 关键词2"
          class="form-input"
          :class="{ 'input-error': errors.raw_keyword }"
          @input="clearError('raw_keyword')"
        />
        <span v-if="errors.raw_keyword" class="error-message">{{ errors.raw_keyword }}</span>
      </div>

      <!-- 爬取深度 -->
      <div class="form-group">
        <label for="max-depth" class="form-label">最大爬取深度:</label>
        <input
          id="max-depth"
          v-model.number="form.max_depth"
          type="number"
          min="1"
          max="10"
          class="form-input"
        />
      </div>

      <!-- 外部链接选项 -->
      <div class="form-group checkbox-group">
        <input
          id="include-external"
          v-model="form.include_external"
          type="checkbox"
          class="form-checkbox"
        />
        <label for="include-external" class="checkbox-label">允许爬取外部链接</label>
      </div>

      <!-- 爬取策略 -->
      <div class="form-group">
        <label for="strategy" class="form-label">爬取策略:</label>
        <select
          id="strategy"
          v-model="form.strategy"
          class="form-select"
        >
          <option value="bfs">广度优先 BFS</option>
          <option value="dfs">深度优先 DFS</option>
          <option value="bestfirst">智能优先 BestFirst</option>
        </select>
      </div>

      <!-- 提交按钮 -->
      <button
        type="submit"
        class="submit-button"
        :disabled="isSubmitting"
      >
        <span v-if="isSubmitting">提交中...</span>
        <span v-else>提交任务</span>
      </button>

      <!-- 状态消息 -->
      <div v-if="message" class="status-message" :class="messageType">
        {{ message }}
      </div>
    </form>
  </div>
</template>

<script setup>
import {onMounted, reactive, ref} from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const form = reactive({
  url: '',
  raw_keyword: '',
  max_depth: 1,
  include_external: false,
  strategy: 'bfs',
})

onMounted(() => {
  form.url = route.query.url || ''
  form.raw_keyword = route.query.raw_keyword || ''
  form.max_depth = Number(route.query.max_depth || 1)
  form.include_external = route.query.include_external === 'true'
  form.strategy = route.query.strategy || 'bfs'
})

const errors = reactive({
  url: '',
  raw_keyword: ''
})

const message = ref('')
const messageType = ref('') // 'success' or 'error'
const isSubmitting = ref(false)

function validateForm() {
  let isValid = true

  // 验证 URL
  if (!form.url) {
    errors.url = '请输入目标网页 URL'
    isValid = false
  } else if (!isValidUrl(form.url)) {
    errors.url = '请输入有效的 URL (以 http:// 或 https:// 开头)'
    isValid = false
  }

  // 验证关键词
  if (!form.raw_keyword) {
    errors.raw_keyword = '请输入至少一个关键词'
    isValid = false
  }

  return isValid
}

function isValidUrl(url) {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

function clearError(field) {
  errors[field] = ''
}

async function submitTask() {
  if (!validateForm()) return

  isSubmitting.value = true
  message.value = ''
  messageType.value = ''

  try {
    const res = await axios.post('http://localhost:8000/api/create-task/', form)
    message.value = `任务创建成功！任务 ID：${res.data.task_id}`
    messageType.value = 'success'

    // 可选：重置表单
    // Object.assign(form, {
    //   url: '',
    //   raw_keyword: '',
    //   max_depth: 1,
    //   include_external: false,
    //   strategy: 'bfs'
    // })
  } catch (err) {
    const errorMsg = err.response?.data?.error || err.message
    message.value = `提交失败：${errorMsg}`
    messageType.value = 'error'
    console.error('任务提交错误:', err)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.task-form-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-title {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  text-align: center;
}

.task-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: #333;
}

.form-input, .form-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.input-error {
  border-color: #e74c3c;
}

.error-message {
  color: #e74c3c;
  font-size: 0.85rem;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
  gap: 0.75rem;
}

.form-checkbox {
  width: auto;
}

.checkbox-label {
  margin: 0;
}

.submit-button {
  padding: 0.75rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #2980b9;
}

.submit-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.status-message {
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
}

.status-message.success {
  background-color: #d4edda;
  color: #155724;
}

.status-message.error {
  background-color: #f8d7da;
  color: #721c24;
}
</style>