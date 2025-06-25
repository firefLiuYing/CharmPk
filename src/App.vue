<script>
import loginUI from "./components/loginUI.vue"
import registerUI from "./components/registerUI.vue"

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
  },

  methods: {
    updatePageName(newValue) {
      this.pageName = newValue;
    }
  }

}
</script>

<template>
    <div class = "image-container">
    <img src="./assets/logo.png" alt="Vue Logo">
    </div>
    <p>Parent Variable: {{ pageName }}</p>
    <loginUI @updateParent = "updatePageName" v-if =  "this.pageName === 'login'"></loginUI>
    <registerUI v-if =  "this.pageName === 'register'"/>

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