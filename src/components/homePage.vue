<!-- HomePage.vue -->
<script setup>

import { ref } from 'vue';
import { storeToRefs } from 'pinia'
import faceEvaluate from './faceEvaluate.vue'
import faceRanking from './faceRanking.vue'
import { useGlobalStore } from '@/stores/pageStore'


// 获取 store 实例
const globalStore = useGlobalStore()

// 解构保持响应性
const { pageFirstName,pageLastName,userIcon,nickname} = storeToRefs(globalStore)
const { changeFirstName } = useGlobalStore()

const imageStyle = ref({
  width: '100px',
  height: '100px',
  'object-fit': 'cover'
});
</script>

<template>
  <div class="container">
    <div class="left">
        <div class="top-left">
          <div class="tl-img">
           <img :src = "userIcon" alt="Setting" :style="imageStyle">
          </div>
          <div class="tl-text">
            {{ nickname }}
          </div>
        </div>
        <div class="bottom-left">
          <div class="left-side-bar">
            <button class="left-button" @click="changeFirstName()">颜值评分</button>
          </div>
          <div class="left-side-bar">
            <button class="left-button" @click="changeFirstName()">颜值PK</button>
          </div>
          <div class="left-side-bar">
            <button class="left-button" @click="changeFirstName()">社交空间</button>
          </div>
          <div class="left-side-bar">
            <button class="left-button" @click="changeFirstName()">好友列表</button>
          </div>
        </div>
    </div>

    <div class="right">
      <p>FirstName: {{pageFirstName}}  |  LastName: {{pageLastName}}</p>
        <div v-if="pageFirstName === 'faceEvaluate' && pageLastName === 'faceRanking'">
          <face-ranking/>
        </div>
        <div v-if="pageFirstName === 'faceEvaluate' && pageLastName === 'faceEvaluate'">
          <face-evaluate/>
        </div>
    </div>

  </div>

</template>


<style scoped>
.container {
  display: grid;
  grid-template-columns: 1fr 3fr;
  grid-template-rows: auto;
  gap: 4px;
  height: 100vh;
  padding: 16px;
  box-sizing: border-box;
}

.left {
  grid-column: 1;
  grid-row: 1;
  flex: 1;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  justify-content: flex-start; /* 水平方向起始对齐 */

  display: grid;
  grid-template-columns: auto;
  grid-template-rows: 1fr 3fr;
}
.top-left{
  grid-column: 1;
  grid-row: 1;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  justify-content: flex-start;

  display: grid;
  grid-template-columns: 1fr 2fr;
  grid-template-rows: auto;
}

.tl-img {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  width: 100px; /* 容器宽度 */
  height: 100px; /* 容器高度 */
  border-radius: 50%; /* 圆形容器 */
  overflow: hidden; /* 隐藏超出圆形部分 */
}

.tl-img img{
  width: 100%; /* 图片宽度填满容器 */
  height: auto; /* 图片高度自动 */
  border-radius: 50%; /* 图片也设置为圆形 */
}

.tl-text{
  flex: 2; /* 占据三分之二的空间 */
  justify-content: flex-start; /* 水平方向起始对齐 */
  align-content: center;
  font-size: 20px; /* 设置字体大小为 20px */
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

.right {
  grid-column: 2;
  grid-row: 1;
  flex: 2;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;
}



.left-button{
  width: 100%; /* 按钮宽度占满整个格子 */
  height: 100%; /* 按钮高度占满整个格子 */
  border: none; /* 去掉边框 */
  background-color: #03fbb1; /* 设置背景颜色 */
  color: white; /* 设置字体颜色 */
  font-size: 16px; /* 设置字体大小 */
  cursor: pointer; /* 设置鼠标悬停时的光标样式 */
  outline: none; /* 去掉焦点时的轮廓 */
}

.bottom-left {
  grid-row: 2;
  grid-column: 1;

  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #ffffff;

  display: grid;
  grid-template-columns: auto;
  grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
}

.left-side-bar{
  flex: 1; /* 占据三分之二的空间 */
  justify-content: center; /* 水平方向起始对齐 */
  align-content: center;
  font-size: 20px; /* 设置字体大小为 20px */
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #686565;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background-color: #17faa2;
}

</style>