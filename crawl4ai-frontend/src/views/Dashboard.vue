<template>
  <div class="layout">
    <aside class="sidebar">
      <ul>
        <li v-for="item in menuItems" :key="item.name">
          <router-link
            :to="item.route"
            class="nav-link"
            active-class="active"
          >
            {{ item.name }}
          </router-link>
        </li>
      </ul>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
const menuItems = [
  { name: '用户', route: '/dashboard/user' },
  { name: '首页', route: '/dashboard/home' },
  { name: '新建', route: '/dashboard/crawlFilter' },
  { name: '任务', route: '/dashboard/task' },
  { name: '数据广场', route: '/dashboard/dataShowcase' }
]
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f0f0f0;
  padding: 20px;
}

.nav-link {
  display: block;
  padding: 10px;
  margin-bottom: 8px;
  color: #333;
  text-decoration: none;
  border-radius: 4px;
}

.nav-link:hover {
  background-color: #ddd;
}

.active {
  background-color: #bbb;
  font-weight: bold;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
