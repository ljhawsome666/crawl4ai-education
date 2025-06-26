<template>
  <div>
    <h2>任务管理</h2>

    <!-- 创建任务表单 -->
    <form @submit.prevent="createTask" class="task-form">
      <input v-model="newUrl" type="url" placeholder="请输入 URL" required />
      <input v-model="newKeyword" type="text" placeholder="请输入关键词" required />
      <button type="submit">创建任务</button>
    </form>

    <!-- 任务列表 -->
    <table class="task-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>URL</th>
          <th>关键词</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id">
          <td>{{ task.id }}</td>
          <td>{{ task.url }}</td>
          <td>{{ task.keyword }}</td>
          <td>{{ task.status }}</td>
          <td>
            <button @click="editTask(task)">编辑</button>
            <button v-if="task.status !== 'completed'" @click="startTask(task)">启动</button>
            <router-link v-if="task.status === 'completed'" :to="`/dashboard/task/${task.id}/results`">查看结果</router-link>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 编辑弹窗 -->
    <div v-if="editingTask" class="modal-overlay">
      <div class="modal">
        <h3>编辑任务</h3>
        <form @submit.prevent="saveEdit">
          <label>URL：</label>
          <input v-model="editingTask.url" type="url" required /><br />
          <label>关键词：</label>
          <input v-model="editingTask.keyword" type="text" required /><br /><br />
          <button type="submit">保存</button>
          <button type="button" @click="cancelEdit">取消</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const newUrl = ref('')
const newKeyword = ref('')
const tasks = ref([])
const editingTask = ref(null)

const fetchTasks = async () => {
  const res = await axios.get('/api/tasks/')
  tasks.value = res.data
}

// ✅ 只保存任务，不启动爬取
const createTask = async () => {
  await axios.post('/api/tasks/', {
    url: newUrl.value,
    keyword: newKeyword.value,
    status: 'pending'
  })
  newUrl.value = ''
  newKeyword.value = ''
  await fetchTasks()
}

// ✅ 编辑任务
const editTask = (task) => {
  editingTask.value = { ...task }
}
const saveEdit = async () => {
  await axios.put(`/api/tasks/${editingTask.value.id}/`, {
    url: editingTask.value.url,
    keyword: editingTask.value.keyword
  })
  editingTask.value = null
  await fetchTasks()
}
const cancelEdit = () => {
  editingTask.value = null
}

// ✅ 启动任务（调用爬虫接口）
const startTask = async (task) => {
  await axios.post('/api/crawl-filter/', {
    url: task.url,
    keyword: task.keyword
  })
  alert('任务已启动并执行完成')
  await fetchTasks()
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.task-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.task-form input {
  flex: 1;
  padding: 6px;
}
.task-table {
  width: 100%;
  border-collapse: collapse;
}
.task-table th, .task-table td {
  border: 1px solid #ccc;
  padding: 8px;
}
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
}
</style>
