<script>
import loginUI from "./components/loginUI.vue"
import registerUI from "./components/registerUI.vue"
import HomePage from "./components/homePage.vue";

export default {
  name: 'App',
  data() {
    return {
     pageName: 'login',
   };
  },
  computed: {
  },
  components: {
    loginUI,
    registerUI,
    Home: HomePage,
  },

  methods: {
    updatePageName(newValue) {
      this.pageName = newValue;
    }
  }

}
</script>

<template>
    <div class = "image-container" v-if = "this.pageName !== 'home'">
    <img src="./assets/logo.png" alt="Vue Logo">
    </div>
    <!--<p>Parent Variable: {{ pageName }}</p>-->
    <loginUI @updateLogin = "updatePageName"   v-if =  "this.pageName === 'login'"></loginUI>
    <registerUI @updateRegister = "updatePageName" v-if =  "this.pageName === 'register'"/>
    <Home v-if = "this.pageName === 'home'"/>

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