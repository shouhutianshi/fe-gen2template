<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <div class="min-h-screen flex items-center justify-center">
    <el-card class="w-96 text-center">
      <h1 class="text-2xl font-bold mb-4">__PROJECT_NAME__</h1>
      <p class="text-gray-500 mb-4">Vue 3 + Vite + TypeScript + Element Plus</p>
      <el-button type="primary" @click="count++">点击了 {{ count }} 次</el-button>
    </el-card>
  </div>
</template>
