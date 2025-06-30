<template>
  <div class="template-container">
    <el-card shadow="hover" class="template-card">
      <div class="card-header">
        <el-icon size="24" color="#409EFF"><Files /></el-icon>
        <span class="card-title">模板列表</span>
        <span class="card-subtitle">网站爬取模板</span>
      </div>

      <div class="card-actions">
        <el-button type="primary" :icon="Refresh" @click="fetchTemplates">刷新数据</el-button>
        <el-button type="success" :icon="Download">导出模板</el-button>
      </div>

      <el-table
        v-if="templates.length"
        :data="templates"
        border
        stripe
        class="template-table"
        style="width: 100%"
        :header-cell-style="{background: '#f5f7fa', color: '#606266'}"
      >
        <el-table-column prop="name" label="网站名称" width="220" sortable>
          <template #default="{row}">
            <div class="website-name">
              <el-icon><Link /></el-icon>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="网站分类" width="180" sortable>
          <template #default="{row}">
            <el-tag :type="getTagType(row.category)">{{ row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="method" label="爬取方法">
          <template #default="{row}">
            <div class="method-content">
              <el-tooltip effect="light" placement="top">
                <template #content>
                  <div style="max-width: 300px">{{ row.method }}</div>
                </template>
                <span class="method-text">{{ truncateMethod(row.method) }}</span>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{row}">
            <el-button type="text" size="small" @click="viewTemplate(row)">查看</el-button>
            <el-button type="text" size="small" @click="useTemplate(row)">使用</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty
        v-else
        description="暂无模板数据"
        :image-size="160"
        image="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
      >
        <el-button type="primary" @click="fetchTemplates">重新加载</el-button>
      </el-empty>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Files, Refresh, Download, Link } from '@element-plus/icons-vue'

const templates = ref([])

const fetchTemplates = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/templates/')
    templates.value = res.data
    ElMessage.success('模板数据加载成功')
  } catch (error) {
    ElMessage.error('获取模板失败，请稍后重试')
  }
}

const getTagType = (category) => {
  const types = ['', 'success', 'info', 'warning', 'danger']
  const hash = [...category].reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return types[hash % types.length]
}

const truncateMethod = (method) => {
  return method.length > 50 ? method.substring(0, 50) + '...' : method
}

const viewTemplate = (row) => {
  ElMessage.info(`查看模板: ${row.name}`)
}

const useTemplate = (row) => {
  ElMessage.success(`已选择模板: ${row.name}`)
}

onMounted(fetchTemplates)
</script>

<style scoped>
.template-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.template-card {
  padding: 20px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.template-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.card-subtitle {
  font-size: 14px;
  color: #909399;
  margin-left: 10px;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
  gap: 12px;
}

.template-table {
  border-radius: 8px;
  overflow: hidden;
  margin-top: 10px;
  font-size: 14px;
}

.template-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa !important;
}

.website-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.method-content {
  display: flex;
  align-items: center;
}

.method-text {
  display: inline-block;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #606266;
}
</style>
