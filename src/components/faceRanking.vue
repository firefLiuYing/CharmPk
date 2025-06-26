<script setup>
    import { storeToRefs } from 'pinia'
    import { useGlobalStore } from '@/stores/pageStore'

    // 获取 store 实例
    const globalStore = useGlobalStore()

    // 解构保持响应性
    const { pageLastName } = storeToRefs(globalStore)
    const { changeLastName } = globalStore
</script>

<template>
    <button @click ="changeLastName('faceEvaluate')">

    </button>
    <p>
      {{ pageLastName }}
    </p>
</template>
<style scoped>

</style>