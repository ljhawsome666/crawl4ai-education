<template>
  <div class="task-form">
    <h2>新建爬取任务</h2>
    <form @submit.prevent="submitTask">
      <label>目标网页 URL:</label>
      <input v-model="form.url" type="url" required />

      <label>关键词（多个用逗号分隔）:</label>
      <input v-model="form.raw_keyword" type="text" required />

      <label>最大爬取深度:</label>
      <input v-model.number="form.max_depth" type="number" min="1" max="10" />

      <label>
        <input v-model="form.include_external" type="checkbox" />
        允许爬取外部链接
      </label>

      <label>爬取策略:</label>
      <select v-model="form.strategy">
        <option value="bfs">广度优先 BFS</option>
        <option value="dfs">深度优先 DFS</option>
        <option value="bestfirst">智能优先 BestFirst</option>
      </select>

      <button type="submit">提交任务</button>
    </form>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'

const form = reactive({
  url: '',
  raw_keyword: '',
  max_depth: 1,
  include_external: false,
  strategy: 'bfs',
})

const message = ref('')

async function submitTask() {
  try {
    const res = await axios.post('http://localhost:8000/api/create-task/', form)
    message.value = `任务创建成功，任务 ID：${res.data.task_id}`
  } catch (err) {
    message.value = `提交失败：${err.response?.data?.error || err.message}`
  }
}
</script>

<style scoped>
.task-form {
  max-width: 500px;
  margin: auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.task-form label {
  display: block;
  margin-top: 1rem;
}
.task-form input,
.task-form select {
  width: 100%;
  padding: 0.5rem;
}
</style>
