<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center">
    <h1 class="text-2xl font-bold mb-4">__PROJECT_NAME__</h1>
    <p class="text-gray-500 mb-4">Vue 3 + Vite + TypeScript + Element Plus + Vant</p>
    <div class="flex gap-4">
      <el-button type="primary" @click="count++">PC: 点击了 {{ count }} 次</el-button>
      <van-button type="primary" @click="count++">H5: 点击了 {{ count }} 次</van-button>
    </div>
  </div>
</template>
