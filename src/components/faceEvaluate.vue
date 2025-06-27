<script setup>
    import { storeToRefs } from 'pinia'
    import { useGlobalStore } from '@/stores/pageStore'
    import { ref } from 'vue'
    import axios from 'axios'


    // 获取 store 实例
    const globalStore = useGlobalStore()

    // 解构保持响应性
    const { pageLastName } = storeToRefs(globalStore)
    const { changeLastName } = globalStore

    const imageSrc = ref(null);
    const fileInput = ref(null);
    const formData = ref(null);
    const points = ref('0');

    const triggerInput = () =>{
      fileInput.value.click();
    }

    const handleFileUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        formData.value = new FormData();
        formData.value.append('image', file);

        const reader = new FileReader();
        reader.onload = (e) => {
          imageSrc.value = e.target.result;
        };
        reader.readAsDataURL(file);

        uploadImage();
      }
    };

    const uploadImage = async () => {
      try {
        const response = await axios.post('http://localhost:5000/login', formData.value, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Response from backend:', response.data);
      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };

    const Evaluate = () => {
        points.value = '100'
    }

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
        <div class="upload-container" @click="triggerInput">
          <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" />
          <div v-if="!imageSrc">Click to upload an image</div>
          <img :src="imageSrc" alt="Uploaded Image" v-else style="width: 100%; height: 100%; object-fit: contain;" />
        </div>
        <div class="response-block" v-if="points === '100'">{{points}}</div>
        <button class="evaluate-button" @click="Evaluate"> 颜值打分 </button>
      </div>
  </div>

  <p>
    {{ pageLastName }}
  </p>
</template>

<style>
.upload-container {
  grid-column: 1;
  grid-row: 1;

  width: 400px;
  height: 200px;
  border: 2px dashed #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  object-fit: cover;
}
.upload-container:hover {
  border-color: #007bff;
}

.response-block{
  grid-row:2;
  grid-column: 1;

  width: 100%;
  height: 100%;
  background-color: darkmagenta;
}

.evaluate-button{
  grid-column: 1;
  grid-row: 3;

  width: 10%; /* 按钮宽度占满整个格子 */
  height: 40%; /* 按钮高度占满整个格子 */
  text-align: center;
  border: none; /* 去掉边框 */
  background-color: #03fbb1; /* 设置背景颜色 */
  color: white; /* 设置字体颜色 */
  font-size: 16px; /* 设置字体大小 */
  cursor: pointer; /* 设置鼠标悬停时的光标样式 */
  outline: none; /* 去掉焦点时的轮廓 */
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