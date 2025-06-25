<!-- HomePage.vue -->
<template>
  <div class="container">
    <div class="top-left">
        <div class="tl-img">
         <img src = "@/assets/setting.png" alt="Setting" :style="imageStyle">
        </div>
        <div class="tl-text">
          粉色默剧
        </div>
    </div>

    <div class="top-right">
      1231321
    </div>

    <div class="bottom-left">
      1231321
    </div>

    <div class="bottom-right">
      1231321
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
  grid-template-rows: 1fr 4fr;
  gap: 4px;
  height: 100vh;
  padding: 16px;
  box-sizing: border-box;
}

.top-left {
  grid-column: 1;
  grid-row: 1;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  align-items: center;
  justify-content: flex-start; /* 水平方向起始对齐 */
  padding-left: 10px; /* 图片和文字之间的间距 */
}

.tl-img{
  margin: 5px;

}

.tl-text{
  flex-grow: 1;
}

.top-right {
  grid-column: 2;
  grid-row: 1;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;
}

.bottom-left {
  grid-column: 1;
  grid-row: 2;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;
}

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

.side-bar{

}

</style>