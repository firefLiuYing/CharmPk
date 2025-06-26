<!-- HomePage.vue -->
<template>
  <div class="container">
    <div class="left">
        <div class="top-left">
          <div class="tl-img">
           <img src = "@/assets/setting.png" alt="Setting" :style="imageStyle">
          </div>
          <div class="tl-text">
            粉色默剧
          </div>
        </div>
        <div class="bottom-left">
          <div class="left-side-bar">
            颜值评分
          </div>
          <div class="left-side-bar">
            颜值PK
          </div>
          <div class="left-side-bar">
              社交空间
          </div>
          <div class="left-side-bar">
              好友列表
          </div>
        </div>
    </div>

    <div class="right">
        12213
    </div>


  </div>

</template>

<script setup>
import { ref } from 'vue';

const imageStyle = ref({
  width: '100px',
  height: '100px',
  'object-fit': 'cover'
});
</script>

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

/*
.top-side-bar{
  flex: 1;
  justify-content: center;
  align-content: center;
  font-size: 20px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #787676;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 30px;
  background-color: #17faa2;
}
*/


.bottom-left {
  grid-column: 1;
  grid-row: 2;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;

  display: grid;
  grid-template-columns: auto; /* 定义两列 */
  grid-template-rows: 1fr 1fr 1fr 1fr 1fr; /* 定义五行 */
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


/*
.bottom-right {
  grid-column: 2;
  grid-row: 2;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
*/

</style>