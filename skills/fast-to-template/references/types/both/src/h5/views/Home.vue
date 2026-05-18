<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4">
    <h1 class="text-2xl font-bold mb-4">__PROJECT_NAME__</h1>
    <p class="text-gray-500 mb-4">Vue 3 + Vite + TypeScript + Vant 4</p>
    <van-button type="primary" @click="count++">点击了 {{ count }} 次</van-button>
  </div>
</template>
