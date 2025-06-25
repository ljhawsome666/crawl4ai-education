<template>
  <div class="p-8 max-w-7xl mx-auto">
    <h1 class="text-4xl font-extrabold text-center text-blue-700 mb-10">📊 数据广场</h1>

    <div v-if="loading" class="flex justify-center items-center text-gray-500 space-x-3">
      <svg class="animate-spin h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
      </svg>
      <span>正在加载数据...</span>
    </div>

    <div v-else-if="error" class="text-center text-red-600 font-semibold">{{ error }}</div>

    <div v-else-if="showcases.length === 0" class="text-center text-gray-400 italic">暂无可展示内容</div>

    <div class="grid gap-8 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="(item, index) in showcases" :key="index"
           class="bg-white border border-gray-200 rounded-3xl shadow-sm hover:shadow-xl transition-shadow duration-300 p-6 flex flex-col justify-between">

        <div>
          <span class="inline-block bg-indigo-100 text-indigo-800 text-xs font-semibold px-3 py-1 rounded-full tracking-wide">
            {{ item.keyword }}
          </span>
          <h2 class="mt-4 font-semibold text-lg text-gray-800 truncate" :title="item.keyword">{{ item.keyword }}</h2>

          <a :href="item.url" target="_blank" rel="noopener"
             class="block mt-2 text-blue-600 hover:text-blue-800 font-medium truncate break-all" :title="item.url">
            🔗 {{ item.url }}
          </a>

          <p class="mt-4 text-gray-700 text-sm bg-gray-50 rounded-md p-3 whitespace-pre-wrap line-clamp-5">
            {{ item.content_preview }}
          </p>
        </div>

        <button @click="copyUrl(item.url)"
                class="mt-5 self-start bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition">
          复制链接
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const showcases = ref([])
const loading = ref(true)
const error = ref('')

function copyUrl(url) {
  navigator.clipboard.writeText(url).then(() => {
    alert('链接已复制到剪贴板')
  }, () => {
    alert('复制失败，请手动复制')
  })
}

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/showcase/')
    if (!res.ok) throw new Error(`加载失败：${res.status}`)
    showcases.value = await res.json()
  } catch (err) {
    error.value = err.message || '请求数据失败'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.line-clamp-5 {
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
}
</style>
