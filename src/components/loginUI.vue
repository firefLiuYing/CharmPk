<script setup>
import { ref } from 'vue';
import { defineEmits } from 'vue';
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { useGlobalStore } from '@/stores/pageStore'


// 获取 store 实例
const globalStore = useGlobalStore()

// 解构保持响应性
const { userIcon ,nickname,user_id} = storeToRefs(globalStore)

const username = ref('');
const password = ref('');
const showDialog = ref(false);
const dialogeContent = ref('123');


function handleLogin() {
  // 在这里添加登录逻辑，例如调用 API
  console.log('Logging in with', username.value, password.value);
  // 清空输入
  //在这里之后增加向数据库发送请求和接受返回值
  login()
  username.value = '';
  password.value = '';


}
const emit = defineEmits(['changePage']);

function changePageToRegister() {
  emit('updateLogin','register'); // 发送事件和新值
}

function changePageToHome() {
  emit('updateLogin','home'); // 发送事件和新值
}

const login = async () => {
    try {
      const formData = new FormData();
        formData.append('username', username.value);
        formData.append('password', password.value);

      const response = await axios.post('/api/login', formData,{
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Response from backend:', response.data);

      if(response.data.check_code === 101){
      dialogeContent.value = '用户不存在或密码错误';
      showDialog.value = true;
      }
      else{
        userIcon.value = response.data.user_icon;
        nickname.value = response.data.nickname;
        user_id.value = response.data.user_id;

        console.log(user_id.value);
        console.log(nickname.value);
        changePageToHome()
      }
    } catch (error) {
      console.error('Error uploading image:', error);
    }
};

</script>

<template>
  <div class="loginUI">
    <h2>登录</h2>
    <!--表单提交监听器-->
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" required />
      </div>

      <div class="link">
        <a @click = "changePageToRegister()">没有账号？点此注册</a>
      </div>

      <button type="submit">登录</button>

    </form>
  </div>

<div>
  <button @click="showDialog=true">显示弹窗</button>
  <div v-if="showDialog" class="dialog-overlay" @click="showDialog = false">
    <div class="dialog" @click.stop>
      <h2>警告</h2>
      <p>{{dialogeContent}}</p>
    </div>
  </div>
</div>
</template>

<style scoped>

.loginUI {
  max-width: 300px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.form-group {
  margin-bottom: 15px;
}

.link{
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #369f7e;
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