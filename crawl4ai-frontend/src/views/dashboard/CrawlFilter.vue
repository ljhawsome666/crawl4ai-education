<template>
  <div
    class="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col items-center py-16 px-6"
  >
    <div
      class="w-full max-w-3xl bg-white/90 backdrop-blur-md rounded-2xl shadow-xl border border-white/40 p-10"
    >
      <!-- Header -->
      <header class="mb-10 text-center select-none">
        <div
          class="inline-flex items-center justify-center mb-4 rounded-lg w-16 h-16 bg-gradient-to-tr from-blue-600 to-teal-400 shadow-lg"
        >
          <i class="fas fa-spider text-white text-3xl"></i>
        </div>
        <h1
          class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-teal-400"
        >
          网页关键词爬取
        </h1>
        <p class="mt-2 text-gray-500 max-w-md mx-auto">
          输入目标网页 URL 和关键词，快速提取包含关键词的内容片段，支持 Markdown 和 LaTeX 渲染
        </p>
      </header>

      <!-- 输入区域 -->
      <div class="space-y-8">
        <div>
          <label for="url" class="flex items-center gap-2 font-semibold text-blue-700 mb-2">
            <i class="fas fa-link"></i> 目标网页 URL
          </label>
          <div class="relative">
            <input
              id="url"
              type="url"
              v-model="url"
              placeholder="https://example.com"
              class="w-full pl-12 pr-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-300 transition"
            />
            <i class="fas fa-globe absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
          </div>
          <p class="mt-1 text-sm text-gray-400 select-text">
            请输入完整的网页地址，包含 http:// 或 https://
          </p>
        </div>

        <div>
          <label for="keyword" class="flex items-center gap-2 font-semibold text-blue-700 mb-2">
            <i class="fas fa-key"></i> 目标关键词
          </label>
          <div class="relative">
            <input
              id="keyword"
              v-model="keyword"
              placeholder="输入要搜索的关键词"
              class="w-full pl-12 pr-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-300 transition"
            />
            <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
          </div>
          <p class="mt-1 text-sm text-gray-400 select-text">
            区分大小写，多个关键词用逗号分隔
          </p>
        </div>

        <div>
          <label for="depth" class="flex items-center gap-2 font-semibold text-blue-700 mb-2">
            <i class="fas fa-layer-group"></i> 爬取深度（max_depth）
          </label>
          <div class="relative">
            <input
              id="depth"
              v-model.number="maxDepth"
              type="number"
              min="1"
              max="5"
              placeholder="默认为 1"
              class="w-full pl-12 pr-4 py-3 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-300 transition"
            />
            <i class="fas fa-arrows-alt-v absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
          </div>
          <p class="mt-1 text-sm text-gray-400 select-text">
            控制爬虫爬取链接的深度，建议不超过 3 层
          </p>
        </div>

        <div>
          <label class="flex items-center gap-2 font-semibold text-blue-700 mb-2">
            <i class="fas fa-external-link-alt"></i> 允许爬取外部链接
          </label>
          <div class="flex items-center space-x-4">
            <label class="inline-flex items-center">
              <input type="checkbox" v-model="includeExternal" class="form-checkbox h-5 w-5 text-blue-600" />
              <span class="ml-2 text-gray-700">启用</span>
            </label>
          </div>
          <p class="mt-1 text-sm text-gray-400 select-text">
            是否允许爬取与起始 URL 不同域名的网页（跨站）
          </p>
        </div>

        <div>
          <label class="flex items-center gap-2 font-semibold text-blue-700 mb-2">
            <i class="fas fa-project-diagram"></i> 选择爬取策略
          </label>
          <select
            v-model="crawlStrategy"
            class="w-full py-3 px-4 border border-gray-300 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-300 transition"
          >
            <option value="bfs">广度优先（BFS）</option>
            <option value="dfs">深度优先（DFS）</option>
            <option value="best">优先级优先（BestFirst）</option>
          </select>
          <p class="mt-1 text-sm text-gray-400 select-text">
            可选策略包括 BFS、DFS 和智能优先爬取 BestFirst（推荐）
          </p>
        </div>


        <!-- 按钮 -->
        <button
          @click="crawl"
          :disabled="loading"
          class="w-full py-4 bg-gradient-to-r from-blue-600 to-teal-500 hover:from-blue-700 hover:to-teal-600 disabled:from-gray-300 disabled:to-gray-300 disabled:cursor-not-allowed rounded-2xl text-white font-bold shadow-lg transition relative"
        >
          <span v-if="!loading">开始爬取</span>
          <span v-else class="flex items-center justify-center gap-3">
            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
            爬取中...
          </span>
        </button>
      </div>

      <!-- 错误信息 -->
      <div v-if="error" class="mt-8 bg-red-100 border border-red-400 text-red-700 rounded-xl px-5 py-4 flex items-center gap-3 select-text">
        <i class="fas fa-exclamation-circle text-xl"></i>
        <span>❌ {{ error }}</span>
      </div>

      <!-- 下载链接 -->
      <div v-if="filename" class="mt-8 text-center">
        <a
          :href="downloadUrl"
          target="_blank"
          class="inline-block bg-green-500 text-white py-2 px-6 rounded-full hover:bg-green-600 transition font-medium shadow-lg"
          download
        >
          📄 下载提取结果 Markdown 文件
        </a>
      </div>

      <!-- 结果展示 -->
      <div v-if="results.length" class="mt-10 space-y-8">
        <div
          v-for="(item, index) in results"
          :key="index"
          class="bg-white rounded-2xl shadow-md p-8 border border-gray-100 hover:shadow-lg transition"
        >
          <h2 class="text-2xl font-semibold text-blue-700 mb-4 truncate">
            <a :href="item.url" target="_blank" rel="noopener noreferrer" class="hover:underline">
              {{ item.title || '无标题' }}
            </a>
          </h2>
          <div class="prose max-w-full text-gray-800" v-html="renderMarkdown(item.markdown)"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { marked } from 'marked'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const url = ref('')
const keyword = ref('')
const maxDepth = ref(1)
const includeExternal = ref(false)
const crawlStrategy = ref('bfs')
const results = ref([])
const filename = ref('')
const error = ref('')
const loading = ref(false)
const downloadUrl = ref('')

marked.setOptions({
  breaks: true,
  gfm: true,
  headerIds: false,
})

const renderer = new marked.Renderer()
renderer.code = (code, infostring, escaped) => {
  if (infostring === 'math' || infostring === 'latex') {
    try {
      return katex.renderToString(code, {
        throwOnError: false,
        displayMode: true,
      })
    } catch {
      return `<pre>${code}</pre>`
    }
  }
  return `<pre><code>${escaped ? code : escapeHtml(code)}</code></pre>`
}

renderer.codespan = (text) => {
  if (text.startsWith('$') && text.endsWith('$')) {
    const mathText = text.slice(1, -1)
    try {
      return katex.renderToString(mathText, {
        throwOnError: false,
        displayMode: false,
      })
    } catch {
      return text
    }
  }
  return text
}

function escapeHtml(html) {
  return html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

const renderMarkdown = (mdText) => {
  return marked.parse(mdText || '', { renderer })
}

const crawl = async () => {
  if (!url.value || !keyword.value) {
    error.value = '请输入URL和关键词'
    return
  }

  error.value = ''
  results.value = []
  filename.value = ''
  downloadUrl.value = ''
  loading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/crawl-filter/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url: url.value,
        keyword: keyword.value,
        max_depth: maxDepth.value || 1,
        include_external: includeExternal.value,
        strategy: crawlStrategy.value,  // 'bfs' / 'dfs' / 'best'
      }),
    })

    const data = await response.json()
    if (!response.ok) throw new Error(data.error || '请求失败')

    results.value = data.results || []
    filename.value = data.filename || ''
    downloadUrl.value = data.download_url || (filename.value ? `http://localhost:8000/api/download/${filename.value}` : '')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.prose {
  max-width: 100%;
  font-size: 1rem;
  line-height: 1.7;
}

.katex-display {
  margin: 1.2em 0;
  text-align: center;
}

input::placeholder {
  color: #9ca3af;
}

input:focus {
  outline: none;
}

.select-none {
  user-select: none;
}

.select-text {
  user-select: text;
}
</style>
