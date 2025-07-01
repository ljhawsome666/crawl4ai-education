<template>
  <div class="template-detail">
    <div class="detail-section">
      <h3 class="section-title">基本信息</h3>
      <div class="section-content">
        <div class="detail-row">
          <span class="detail-label">模板名称:</span>
          <span class="detail-value">{{ template.name }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">网站分类:</span>
          <el-tag :type="getTagType(template.category)">
            {{ template.category }}
          </el-tag>
        </div>
        <div class="detail-row">
          <span class="detail-label">目标网址:</span>
          <a :href="template.url" target="_blank" class="detail-value link">
            {{ template.url }}
          </a>
        </div>
      </div>
    </div>

    <div class="detail-section">
      <h3 class="section-title">爬取配置</h3>
      <div class="section-content">
        <div class="detail-row">
          <span class="detail-label">爬取策略:</span>
          <span class="detail-value">{{ formatStrategy(template.strategy) }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">最大深度:</span>
          <span class="detail-value">{{ template.max_depth }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">包含外链:</span>
          <span class="detail-value">
            {{ template.include_external ? '是' : '否' }}
          </span>
        </div>
      </div>
    </div>

    <div class="detail-section">
      <h3 class="section-title">爬取方法</h3>
      <div class="section-content code-block">
        <pre>{{ template.method }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  template: {
    type: Object,
    required: true
  }
})

const getTagType = (category) => {
  const types = ['', 'success', 'warning', 'danger', 'info']
  const hash = [...category].reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return types[hash % types.length]
}

const formatStrategy = (strategy) => {
  const map = {
    'bfs': '广度优先 (BFS)',
    'dfs': '深度优先 (DFS)',
    'bestfirst': '智能优先 (BestFirst)'
  }
  return map[strategy] || strategy
}
</script>

<style scoped>
.template-detail {
  padding: 16px;
}

.detail-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.section-content {
  padding: 0 12px;
}

.detail-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.detail-label {
  width: 100px;
  font-weight: 500;
  color: #64748b;
}

.detail-value {
  flex: 1;
  color: #1e293b;
}

.link {
  color: #3b82f6;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.code-block {
  background-color: #f8fafc;
  border-radius: 6px;
  padding: 12px;
  font-family: 'Courier New', Courier, monospace;
  overflow-x: auto;
}

.code-block pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>