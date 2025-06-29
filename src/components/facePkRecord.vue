<script setup>
import {onMounted, ref} from 'vue'
    import axios from 'axios'
    import { storeToRefs } from 'pinia'
    import { useGlobalStore } from '@/stores/pageStore'

    // 获取 store 实例
    const globalStore = useGlobalStore()
    const { user_id} = storeToRefs(globalStore)
    const { changeLastName } = globalStore

    const points_1 = ref([]);
    const images_1 = ref([]);
    const points_2 = ref([]);
    const images_2 = ref([]);
    const nickname_1 = ref([]);
    const nickname_2 = ref([]);



    const loadPkRanking = async () => {
      try {
        const formData = new FormData();
        formData.append('user_id', user_id.value);
        const response = await axios.post('/api/loadPkRanking', formData,{
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Response from backend:', response.data);

        points_1.value = response.data.points_1;
        images_1.value = response.data.images_1;
        points_2.value = response.data.points_2;
        images_2.value = response.data.images_2;
        nickname_1.value = response.data.nickname_1;
        nickname_2.value = response.data.nickname_2;

      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };
        onMounted(loadPkRanking())
</script>

<template>
  <div class="right-container">
      <div class="top">
          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('facePk')">颜值PK</button>
          </div>

          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('facePkRecords')">PK记录</button>
          </div>

          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('facePkApplication')">PK邀请</button>
          </div>
      </div>

      <div class="content">
        <h2>颜值PK申请列表</h2>
          <div v-if="!points_1.length" class="empty">
            暂无PK申请
          </div>

          <div v-else class="request-list">
            <div
              v-for="(id, index) in points_1"
              :key="id"
              class="request-item"
            >
            <div class="requester-info">
              <img
                :src="images_1[index]"
                alt="头像"
                class="avatar"
              />
              <span class="username">{{ nickname_1[index] }} : {{points_1[index]}}  VS</span>

              <img
                :src="images_1[index]"
                alt="头像"
                class="avatar"
              />
              <span class="username">{{ nickname_2[index] }} : {{points_2[index]}}</span>
            </div>
        </div>
      </div>
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
  padding: 60px;

  display:grid;
  grid-template-columns: 1fr;
  grid-template-rows: 2fr 2fr 1fr;
  background-color: coral;
  justify-items: center;
}

</style>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>

<style>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 80%;
  max-width: 400px;
}
</style>