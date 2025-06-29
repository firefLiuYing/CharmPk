<script setup>
import {onMounted, ref} from 'vue'
    import axios from 'axios'
    import { storeToRefs } from 'pinia'
    import { useGlobalStore } from '@/stores/pageStore'


    // 获取 store 实例
    const globalStore = useGlobalStore()

    // 解构保持响应性
    const { pageLastName,user_id } = storeToRefs(globalStore)
    const { changeLastName } = globalStore

    const nouse = ref('')
    const points = ref([]);
    const images = ref([]);

    nouse.value = pageLastName

    const loadUserCharmRanking = async () => {
      try {
        const formData = new FormData();
        formData.append('user_id', user_id.value);
        const response = await axios.post('/api/loadUserCharmRanking', formData,{
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Response from backend:', response.data);

        points.value = response.data.points;
        images.value = response.data.images;

      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };

    onMounted(loadUserCharmRanking)
</script>

<template>
    <div class="right-container">
      <div class="top">
          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('faceEvaluate')">颜值评分</button>
          </div>

          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('faceRanking')">颜值排名</button>
          </div>
      </div>
      <div class="content">
       <p style = "font-size: 40px; text-align: center">颜值评分排名</p>
          <div v-if="!points.length" class="empty">
            暂无评分记录
          </div>

          <div v-else class="request-list">
            <div
              v-for="(point, index) in points"
              :key="point"
              class="request-item"
            >
              <div class="requester-info">
                <p> 排名：{{index}} </p>
                <img
                  :src="images[index]"
                  alt="头像"
                  class="avatar"
                />
                <span class="username"> : {{ points[index] }}</span>
              </div>
            </div>
        </div>
      </div>
  </div>

</template>
<style scoped>
.right-container{
  display: grid;
  grid-template-rows: minmax(94.5px, 1fr) 7fr;
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
  background-color: #ff6900;
  font-size: 64px;

  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: auto;
}

.content_1{
  grid-row: 1;

}
</style>

<style scoped>

.request-list {
  margin-top: 20px;
}

.request-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px;
  border-bottom: 2px solid #eee;
}

.requester-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 10%;
  height: 10%;
  object-fit: cover;
}

.username {
  font-weight: 500;
}


</style>