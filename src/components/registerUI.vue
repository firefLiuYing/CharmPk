<template>
  <div class="loginUI">
    <h2>注册</h2>
    <!--表单提交监听器-->
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" required />
      </div>

      <div class="link" @click="changePageToLogin">
        <a href = "">已有账号？点此登录</a>
      </div>

      <button type="submit">注册</button>

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

<script setup>
import { ref } from 'vue';
import { defineEmits } from 'vue';
import axios from 'axios'
import response from "core-js/internals/is-forced";

const username = ref('');
const password = ref('');
const showDialog = ref(false);
const dialogeContent = ref('123');
const emit = defineEmits(['changePage']);

const register = async () => {
      try {
        const response = await axios.post('http://localhost:5000/upload', username.value,password.value,{
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Response from backend:', response.data);
      } catch (error) {
        console.error('Error uploading image:', error);
      }

      if(response.data.check_code === 102){
        showDialog.value = true;
        dialogeContent.value = '用户名已存在，请更换用户名';
      }
    };

function changePageToLogin() {
  emit('updateRegister','login'); // 发送事件和新值
}

function handleRegister() {
  // 在这里添加登录逻辑，例如调用 API
  console.log('Logging in with', username.value, password.value);

  register();
  // 清空输入
  username.value = '';
  password.value = '';
}
</script>

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