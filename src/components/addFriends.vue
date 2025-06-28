<script setup>
    import { ref } from 'vue'
    import axios from 'axios'
    import { storeToRefs } from 'pinia'
    import { useGlobalStore } from '@/stores/pageStore'

    // 获取 store 实例
    const globalStore = useGlobalStore()

    // 解构保持响应性
    const { user_id} = storeToRefs(globalStore)
    const { changeLastName } = globalStore
    const user_icon_2 = ref('')
    const user_id_2 = ref(null)
    const nickname_2 = ref(null)
    const searchInput = ref('')
    const searchResult = ref(null)
    const showDialog = ref(false);
    const dialogContent = ref('213');

    let searchTimer = null
    const handleSearchInput = () => {
      clearTimeout(searchTimer)
      searchTimer = setTimeout(() => {
        if (searchInput.value) {
          searchUser(searchInput)
        } else {
          searchResult.value = false
        }
      }, 500)
    }

    const searchUser = async (nickname) => {
      try {
        const formData = new FormData();
        formData.value.append('nickname', nickname.value);
        const response = await axios.post('/api/searchUser', formData,{
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Response from backend:', response.data);
        if(response.data.check_code === 101){
          console.log('全都死光光了')
          dialogContent.value = '用户名已存在，请更换用户名';
          showDialog.value = true;
        }
        else{
          nickname_2.value = nickname.value;
          user_icon_2.value = response.data.user_icon;
          user_id_2.value = response.data.other_user_id;
          searchResult.value = true;
        }


      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };

    const applyForFriends = async () => {
      try {
        const formData = new FormData();
        formData.append('nickname', user_id.value);
        formData.append('nickname', user_id_2.value);
        const response = await axios.post('/api/applyForFriends', formData,{
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Response from backend:', response.data);
        if(response.data.check_code === 105){
          console.log('全都死光光了')
          dialogContent.value = '已经申请过该好友，请勿重复添加';
          showDialog.value = true;
        }

      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };
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
          <div class="user-search-container">
    <!-- 搜索框 -->
    <input
      v-model="searchInput"
      type="text"
      placeholder="输入好友昵称"
      @input="handleSearchInput"
      class="search-input"
    />

    <!-- 搜索结果展示 -->
    <div v-if="searchResult" class="result-card">
      <div class="user-info">
        <img :src="user_icon_2" alt="用户头像" class="avatar" />
        <span class="username">{{ user_id_2 }}</span>
      </div>
      <button @click="applyForFriends" class="add-button">
            添加好友
      </button>
    </div>

  </div>
      </div>
  </div>
</template>

<style scoped>
.user-search-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  margin-bottom: 15px;
}

.result-card {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.username {
  font-weight: bold;
}

.add-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.add-button:hover {
  background-color: #3aa876;
}

.add-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

</style>

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