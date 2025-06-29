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
          <td>
            <input v-model="task.url" />
          </td>
          <td>
            <input v-model="task.keyword" />
          </td>
          <td>
            <input v-model.number="task.max_depth" type="number" min="1" />
          </td>
          <td>
            <select v-model="task.strategy">
              <option value="bfs">BFS</option>
              <option value="dfs">DFS</option>
              <option value="bestfirst">智能优先</option>
            </select>
          </td>
          <td>
            <input type="checkbox" v-model="task.include_external" />
          </td>
          <td>{{ task.status }}</td>
          <td>
            <div v-if="task.status === 'running'">
              {{ task.progress }}%
            </div>
            <div v-else>-</div>
          </td>
          <td>
            <button @click="updateTask(task)">保存</button>
            <button @click="startTask(task)" :disabled="task.status !== 'pending'">启动</button>
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

const fetchTasks = async () => {
  const response = await axios.get('http://localhost:8000/api/tasks/')

  if (Array.isArray(response.data)) {
    tasks.value = response.data.map(task => ({...task, progress: 0}))
  } else {
    console.error('任务接口返回的数据不是数组：', response.data)
  tasks.value = []
  }
}

const updateTask = async (task) => {
  await axios.put(`/api/tasks/${task.id}/`, task)
  alert("任务更新成功")
}

const startTask = async (task) => {
  task.status = 'running'
  await axios.post(`/api/tasks/${task.id}/start/`)
  pollProgress(task)
}

const pollProgress = (task) => {
  const interval = setInterval(async () => {
    const response = await axios.get(`/api/tasks/${task.id}/progress/`)
    task.progress = response.data.progress
    task.status = response.data.status
    if (task.status !== 'running') {
      clearInterval(interval)
    }
  }, 2000)
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
