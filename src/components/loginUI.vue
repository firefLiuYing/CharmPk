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
        <a @click = "changePage()">没有账号？点此注册</a>
      </div>

      <button type="submit">登录</button>

    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { defineEmits } from 'vue';

const username = ref('');
const password = ref('');

function handleLogin() {
  // 在这里添加登录逻辑，例如调用 API
  console.log('Logging in with', username.value, password.value);
  // 清空输入
  //在这里之后增加向数据库发送请求和接受返回值
  username.value = '';
  password.value = '';
  changePage()
}
const emit = defineEmits(['changePage']);

function changePage() {
  emit('updateParent','register'); // 发送事件和新值
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