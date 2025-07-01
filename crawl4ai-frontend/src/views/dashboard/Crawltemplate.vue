<template>
  <div class="template-manager">
    <!-- 头部区域 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-title">
          <el-icon class="header-icon"><Files /></el-icon>
          <h1>网站爬取模板</h1>
          <!-- 红色通知徽标 -->
          <el-badge :value="1" type="danger" class="notification-badge">
            <el-icon :size="20"><Bell /></el-icon>
          </el-badge>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="template-content">
      <!-- 搜索和筛选区域 -->
      <div class="filter-section">
        <el-input
          v-model="searchQuery"
          placeholder="搜索模板名称或分类"
          clearable
          class="search-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-select
          v-model="categoryFilter"
          placeholder="按分类筛选"
          clearable
          class="category-select"
        >
          <el-option
            v-for="category in uniqueCategories"
            :key="category"
            :label="category"
            :value="category"
          />
        </el-select>
      </div>

      <!-- 模板表格 -->
      <div class="template-table-container">
        <el-table
          :data="filteredTemplates"
          border
          stripe
          style="width: 100%"
          :header-cell-style="{ background: '#f8fafc', color: '#64748b' }"
          v-loading="loading"
        >
          <el-table-column prop="name" label="网站名称" width="220" sortable>
            <template #default="{ row }">
              <div class="website-cell">
                <el-avatar :size="32" :src="defaultWebsiteIcon" />
                <div class="website-info">
                  <span class="website-name">{{ row.name }}</span>
                  <span class="website-url">{{ formatUrl(row.url) }}</span>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="category" label="分类" width="180" sortable>
            <template #default="{ row }">
              <el-tag :type="getTagType(row.category)">
                {{ row.category }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="method" label="爬取方法">
            <template #default="{ row }">
              <span class="method-text">{{ truncateMethod(row.method) }}</span>
            </template>
          </el-table-column>

          <!-- 操作列（包含查看详情按钮） -->
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button
                  type="primary"
                  size="small"
                  @click="viewTemplate(row)"
                >
                  查看详情
                </el-button>
                <el-button
                  type="success"
                  size="small"
                  @click="useTemplate(row)"
                >
                  使用
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 分页控制 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredTemplates.length"
        />
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`模板详情 - ${selectedTemplate?.name}`"
      width="50%"
    >
      <div v-if="selectedTemplate" class="template-detail">
        <div class="detail-row">
          <span class="detail-label">网站名称：</span>
          <span>{{ selectedTemplate.name }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">目标网址：</span>
          <a :href="selectedTemplate.url" target="_blank">{{ selectedTemplate.url }}</a>
        </div>
        <div class="detail-row">
          <span class="detail-label">爬取方法：</span>
          <pre class="method-content">{{ selectedTemplate.method }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Files, Search, Bell } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const templates = ref([])
const loading = ref(false)
const searchQuery = ref('')
const categoryFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const detailDialogVisible = ref(false)
const selectedTemplate = ref(null)

const defaultWebsiteIcon = 'https://cdn-icons-png.flaticon.com/512/1006/1006771.png'

// 计算属性
const uniqueCategories = computed(() => {
  const categories = new Set()
  templates.value.forEach(t => categories.add(t.category))
  return Array.from(categories)
})

const filteredTemplates = computed(() => {
  return templates.value.filter(t =>
    (!searchQuery.value || t.name.includes(searchQuery.value)) &&
    (!categoryFilter.value || t.category === categoryFilter.value)
  )
})

// 方法
const fetchTemplates = async () => {
  loading.value = true
  try {
    const res = await axios.get('http://localhost:8000/api/templates/')
    templates.value = res.data
  } finally {
    loading.value = false
  }
}

const viewTemplate = (template) => {
  selectedTemplate.value = template
  detailDialogVisible.value = true
}

const useTemplate = (template) => {
  router.push({
    path: '/dashboard/createTask',
    query: {
      url: template.url,
      raw_keyword: template.raw_keyword,
      max_depth: template.max_depth,
      include_external: template.include_external,
      strategy: template.strategy
    }
  })
}

const getTagType = (category) => {
  const types = ['', 'success', 'warning', 'danger', 'info']
  const hash = [...category].reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return types[hash % types.length]
}

const truncateMethod = (method) => {
  return method.length > 50 ? method.substring(0, 50) + '...' : method
}

const formatUrl = (url) => {
  try {
    const { hostname } = new URL(url)
    return hostname.replace('www.', '')
  } catch {
    return url.length > 20 ? url.substring(0, 20) + '...' : url
  }
}

onMounted(fetchTemplates)
</script>

<style scoped>
.template-manager {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.header-title h1 {
  font-size: 24px;
  margin: 0;
}

.notification-badge {
  margin-left: 15px;
  cursor: pointer;
}

.filter-section {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.search-input, .category-select {
  width: 240px;
}

.template-table-container {
  margin-bottom: 24px;
}

.website-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.website-info {
  display: flex;
  flex-direction: column;
}

.website-name {
  font-weight: 500;
}

.website-url {
  font-size: 12px;
  color: #64748b;
}

.method-text {
  display: inline-block;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.pagination-section {
  display: flex;
  justify-content: center;
}

.template-detail {
  padding: 0 20px;
}

.detail-row {
  margin-bottom: 15px;
  display: flex;
}

.detail-label {
  font-weight: bold;
  min-width: 80px;
  display: inline-block;
}

.method-content {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  white-space: pre-wrap;
  font-family: monospace;
  max-height: 300px;
  overflow: auto;
}
</style>