<template>
  <div class="dashboard">
    <el-card class="box-card">
      <h2>智能爬虫任务配置</h2>

      <el-form :model="form" label-width="80px">
        <el-form-item label="URL">
          <el-input v-model="form.url" placeholder="请输入目标网站 URL" />
        </el-form-item>

        <el-form-item label="关键词">
          <el-input v-model="form.keyword" placeholder="请输入关键词（可选）" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="startScraping">Scraping</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const form = ref({
  url: '',
  keyword: ''
})

const startScraping = async () => {
  if (!form.value.url) {
    ElMessage.warning('请输入 URL')
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/api/scrape/', form.value)
    ElMessage.success('爬虫任务已提交！')
    console.log('爬虫返回结果：', response.data)
    // 你也可以在此展示结果、跳转页面等
  } catch (error) {
    console.error(error)
    ElMessage.error('爬虫请求失败，请检查后台是否运行')
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 600px;
  margin: 50px auto;
}

.box-card {
  padding: 20px;
}
</style>
