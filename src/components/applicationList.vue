<script setup>
    import { storeToRefs } from 'pinia'
    import { useGlobalStore } from '@/stores/pageStore'
    import {onMounted, ref} from "vue";
    import axios from "axios";

    // 获取 store 实例
    const globalStore = useGlobalStore()

    // 解构保持响应性
    const { user_id} = storeToRefs(globalStore)
    const { changeLastName } = globalStore
    const user_icons = ref([])
    const nicknames = ref([])
    const user_ids = ref([])
    const showApplication = ref(false)

    const loadApplication = async () => {
      try {
        const formData = new FormData();
        formData.append('user_id', user_id.value);
        const response = await axios.post('/api/loadApplication', formData,{
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Response from backend:', response.data);
        if(response.data.nickname.length === 0){
          showApplication.value = false
        }
        else{
          showApplication.value = true
          user_ids.value = response.data.user_icon;
          nicknames.value = response.data.nickname;
          user_icons.value = response.data.user_icon;
        }

      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };

    const acceptApplication = async (user_id_2) => {
      try {
        const formData = new FormData();
        formData.append('user_id_1', user_id.value);
        formData.append('user_id_2_', user_id_2.value);
        const response = await axios.post('/api/acceptApplication', formData,{
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Response from backend:', response.data);
        loadApplication();

      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };

    const refuseApplication = async (user_id_2) => {
      try {
        const formData = new FormData();
        formData.append('user_id_1', user_id.value);
        formData.append('user_id_2_', user_id_2.value);
        const response = await axios.post('/api/refuseApplication', formData,{
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Response from backend:', response.data);
        loadApplication();

      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };

    onMounted(loadApplication);
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
          <h2>好友申请列表</h2>
          <div v-if="!user_ids.length" class="empty">
            暂无好友申请
          </div>

          <div v-else class="request-list">
            <div
              v-for="(id, index) in user_ids"
              :key="id"
              class="request-item"
            >
              <div class="requester-info">
                <img
                  :src="user_icons[index] || defaultAvatar"
                  alt="头像"
                  class="avatar"
                />
                <span class="username">{{ nicknames[index] }}</span>
              </div>

          <div class="action-buttons">
            <button
              @click="acceptApplication(id)"
              class="accept-btn"
            >
              <span>同意</span>
            </button>

            <button
              @click="refuseApplication(id)"
              class="reject-btn"
            >
              <span>拒绝</span>
            </button>
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
  background-color: coral;
  font-size: 64px;
}
</style>

<style scoped>
.friend-requests-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .empty {
  text-align: center;
  padding: 20px;
  color: #666;
}

.request-list {
  margin-top: 20px;
}

.request-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.requester-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.username {
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.3s;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.accept-btn {
  background-color: #42b983;
  color: white;
}

.reject-btn {
  background-color: #f56c6c;
  color: white;
}
</style>