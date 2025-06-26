<!-- src/components/dashboard/TaskResults.vue -->
<template>
  <div>
    <h2>任务爬取结果</h2>
    <p><strong>关键词：</strong>{{ keyword }}</p>
    <p><strong>URL：</strong>{{ url }}</p>

    <hr />
    <div v-if="results.length === 0">暂无爬取结果。</div>
    <div v-else>
      <div v-for="item in results" :key="item.url" style="margin-bottom: 20px;">
        <h3>{{ item.keyword }}</h3>
        <p><a :href="item.url" target="_blank">{{ item.url }}</a></p>
        <div v-html="item.content_preview"></div>
      </div>
    </div>

    <router-link to="/dashboard/task">返回任务列表</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const taskId = route.params.id
const url = ref('')
const keyword = ref('')
const results = ref([])

const loadData = async () => {
  const taskRes = await axios.get(`/api/tasks/${taskId}/`)
  url.value = taskRes.data.url
  keyword.value = taskRes.data.keyword

  const res = await axios.get('/api/results/', {
    params: { url: url.value, keyword: keyword.value }
  })
  results.value = res.data
}

onMounted(() => {
  loadData()
})
</script>
