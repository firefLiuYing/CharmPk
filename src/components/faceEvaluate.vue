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

    const imageSrc = ref(null);
    const fileInput = ref(null);
    const formData = ref(null);
    const point = ref(null);
    const showDialog = ref(false);
    const dialogContent = ref('213');

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

      }
    };

    const faceEvaluate = async () => {
      try {
        formData.value.append('user_id', user_id.value);
        const response = await axios.post('/api/faceEvaluate', formData,{
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Response from backend:', response.data);
              point.value = response.data.point;
      } catch (error) {
        console.error('Error uploading image:', error);
      }
    };


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
        <div class="response-block" v-if="!point">{{point}}</div>
        <button class="evaluate-button" @click="faceEvaluate"> 颜值打分 </button>
      </div>
  </div>

  <div>
  <button @click="showDialog=true">显示弹窗</button>
  <div v-if="showDialog" class="dialog-overlay" @click="showDialog = false">
    <div class="dialog" @click.stop>
      <h2>警告</h2>
      <p>{{dialogContent}}</p>
    </div>
  </div>
</div>

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