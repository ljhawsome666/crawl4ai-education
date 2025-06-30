<template>
  <div class="task-manager">
    <h2>任务管理</h2>

    <table class="task-table">
      <thead>
        <tr>
          <th>网址</th>
          <th>关键词</th>
          <th>深度</th>
          <th>策略</th>
          <th>包含外链</th>
          <th>状态</th>
          <th>进度</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id">
          <td><input v-model="task.url" :disabled="task.status === 'running'" /></td>
          <td><input v-model="task.keyword" :disabled="task.status === 'running'" /></td>
          <td><input v-model.number="task.max_depth" type="number" min="1" :disabled="task.status === 'running'" /></td>
          <td>
            <select v-model="task.strategy" :disabled="task.status === 'running'">
              <option value="bfs">BFS</option>
              <option value="dfs">DFS</option>
              <option value="bestfirst">智能优先</option>
            </select>
          </td>
          <td><input type="checkbox" v-model="task.include_external" :disabled="task.status === 'running'" /></td>
          <td>{{ task.status }}</td>
          <td>
            <div v-if="task.status === 'running'">
              {{ task.progress }}%
            </div>
            <div v-else>-</div>
          </td>
          <td>
            <button @click="updateTask(task)" :disabled="task.status === 'running' || task.isStarting">保存</button>
            <button @click="startTask(task)" :disabled="task.status !== 'pending' || task.isStarting">
              <span v-if="task.isStarting">启动中...</span>
              <span v-else>启动</span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const tasks = ref([])
const pollingTimers = {}

const fetchTasks = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/tasks/', { timeout: 5000 })
    if (Array.isArray(response.data)) {
      tasks.value = response.data.map(task => ({
        ...task,
        progress: 0,
        isStarting: false
      }))
    } else {
      console.error('任务接口返回的数据不是数组：', response.data)
      tasks.value = []
    }
  } catch (e) {
    console.error('获取任务失败:', e)
  }
}

const updateTask = async (task) => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/tasks/${task.id}/`, task)
    alert("任务更新成功")
  } catch (e) {
    alert("任务更新失败: " + (e.response?.data?.error || e.message))
  }
}


const startTask = async (task) => {
  if (task.isStarting || task.status !== 'pending') return
  task.isStarting = true

  try {
    // 触发后端启动任务，通常只需要task.id即可，参数都存在数据库里
    await axios.post(`http://127.0.0.1:8000/api/tasks/${task.id}/start/`, null, { timeout: 10000 })

    task.status = 'running'
    task.progress = 0

    // 启动后马上请求一次进度，提升体验
    await pollProgress(task)

    // 清理已有定时器，避免重复
    if (pollingTimers[task.id]) clearInterval(pollingTimers[task.id])
    pollingTimers[task.id] = setInterval(() => pollProgress(task), 2000)

  } catch (e) {
    alert("启动任务失败: " + (e.response?.data?.detail || e.message))
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

    if (task.status !== 'running' && pollingTimers[task.id]) {
      clearInterval(pollingTimers[task.id])
      delete pollingTimers[task.id]
    }
  } catch (e) {
    console.error("查询任务进度失败", e)
    if (pollingTimers[task.id]) {
      clearInterval(pollingTimers[task.id])
      delete pollingTimers[task.id]
    }
  }
}

onMounted(fetchTasks)
</script>

<style scoped>
.task-manager {
  padding: 20px;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
}

.task-table th,
.task-table td {
  border: 1px solid #ddd;
  padding: 8px;
}
</style>
