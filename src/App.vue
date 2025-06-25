<script>
import loginUi from "./components/loginUI.vue"
import registerUi from "./components/registerUI.vue"


export default {
  name: 'App',
  components: {
    loginUi,
    registerUi,
  }
}
</script>

<template>
    <div class = "image-container" v-show = "generalView = register">
    <img src="./assets/logo.png" alt="Vue Logo">
    </div>
    <loginUi></loginUi>
    <registerUi/>

</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

<style>
  .image-container img {
    width: 100px; /* 设置宽度 */
    height: 100px; /* 设置高度 */
    object-fit: cover; /* 保持图片比例 */
  }
</style>