<script setup>
    // import { ref } from 'vue'
    // import axios from 'axios'
    import { storeToRefs } from 'pinia'
    import { useGlobalStore } from '@/stores/pageStore'

    // 获取 store 实例
    const globalStore = useGlobalStore()

    // 解构保持响应性
    // const { pageLastName,user_id} = storeToRefs(globalStore)
    const { changeLastName } = globalStore
</script>

<template>
    <div class="right-container">
      <div class="top">
          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('addFriends')">添加好友</button>
          </div>
          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('applicationList')">申请列表</button>
          </div>
          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('friendList')">好友列表</button>
          </div>
      </div>
      <div class="content">

      </div>
  </div>
</template>

<style scoped>
.right-container{
  display: grid;
  grid-template-rows: 1fr 7fr;
  grid-template-columns: auto;
  height: 100vh;
  padding: 16px;
  box-sizing: border-box;
}

.top{
  grid-row: 1;
  grid-column: 1;

  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #ffffff;

  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  grid-template-rows: auto;
}

.top-side-bar{
  flex: 1;
  justify-content: center; /* 水平方向起始对齐 */
  align-content: center;
  font-size: 20px; /* 设置字体大小为 20px */
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #686565;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding:4px;
  background-color: #0adcac;
}

.top-button{
  width: 100%; /* 按钮宽度占满整个格子 */
  height: 100%; /* 按钮高度占满整个格子 */
  border: none; /* 去掉边框 */
  background-color: #03fbb1; /* 设置背景颜色 */
  color: white; /* 设置字体颜色 */
  font-size: 16px; /* 设置字体大小 */
  cursor: pointer; /* 设置鼠标悬停时的光标样式 */
  outline: none; /* 去掉焦点时的轮廓 */
}

.content{
  grid-row: 2;
  grid-column: 1;
  text-align: center;
  background-color: coral;
  font-size: 64px;
}
</style>