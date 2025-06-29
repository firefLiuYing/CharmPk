<script setup>
    // import { ref } from 'vue'
    // import axios from 'axios'
    // import { storeToRefs } from 'pinia'
    import { useGlobalStore } from '@/stores/pageStore'
    import {ref} from "vue";
    import axios from "axios";
    import {storeToRefs} from "pinia";

    // 获取 store 实例
    const globalStore = useGlobalStore()
    const {user_id,other_user_id} = storeToRefs(globalStore)
    const { changeLastName } = globalStore

    const imageSrc_1 = ref(null);
    const imageSrc_2 = ref(null);
    const fileInput = ref(null);
    const formData_1 = ref(null);
    const formData_2 = ref(null);
    const point_1 = ref(null);
    const point_2 = ref(null);
    const text_1 = ref(null);
    const text_2 = ref(null);
    const isresponsed = ref(false)

    const triggerInput_1 = () =>{
      fileInput.value.click();
    }

    const triggerInput_2 = () =>{
      if(!other_user_id){
        changeLastName('facePkApplication')
      }
      else  fileInput.value.click();
    }

    const handleFileUpload_1 = (event) => {
      const file = event.target.files[0];
      if (file) {
        formData_1.value = new FormData();
        formData_1.value.append('image_1', file);

        const reader = new FileReader();
        reader.onload = (e) => {
          imageSrc_1.value = e.target.result;
        };
        reader.readAsDataURL(file);
        uploadImageToPkRecords_1(user_id)
      }
    };

    const handleFileUpload_2 = (event) => {
      const file = event.target.files[0];
      if (file) {
        formData_2.value = new FormData();
        formData_2.value.append('image_2', file);

        const reader = new FileReader();
        reader.onload = (e) => {
          imageSrc_2.value = e.target.result;
        };
        reader.readAsDataURL(file);
        uploadImageToPkRecords_2(other_user_id)
      }
    }

    const uploadImageToPkRecords_1 = async (user_id) =>{
      try {
        formData_1.value.append('user_id', user_id.value);
        const response = await axios.post('/api/facePk', formData_1.value, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Response from backend:', response.data);
      } catch (error) {
        console.error('Error uploading image:', error);
      }
    }

    const uploadImageToPkRecords_2 = async (user_id) =>{
      try {
        formData_2.value.append('user_id', user_id.value);
        const response = await axios.post('/api/facePk', formData_2.value, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Response from backend:', response.data);
      } catch (error) {
        console.error('Error uploading image:', error);
      }
    }

    const facePk = async () => {
      try {
        const formData = new FormData();
        formData.append('user_id_1', user_id.value);
        formData.append('user_id_2', other_user_id.value);
        const response = await axios.post('/api/facePk', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Response from backend:', response.data);

        point_1.value = response.data.point_1;
        point_2.value = response.data.point_2;
        if (point_1.value > point_2.value) {
          text_1.value = '胜'
          text_2.value = '负'
        } else {
          text_1.value = '负'
          text_2.value = '胜'
        }
        isresponsed.value = true;
      } catch (error) {
        console.error('Error uploading image:', error);
      }
  }

</script>

<template>
  <div class="right-container">
      <div class="top">
          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('facePk')">颜值PK</button>
          </div>

          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('facePkRecords')">PK记录</button>
          </div>

          <div class="top-side-bar">
              <button class="top-button" @click ="changeLastName('facePkApplication'),other_user_id = null">PK邀请</button>
          </div>
      </div>

      <div class="content">
        <div class="upload-container_1" @click="triggerInput_1">
          <p> 请你上传图片至此处 </p>
          <input type="file" ref="fileInput" @change="handleFileUpload_1" style="display: none;" />
          <div v-if="!imageSrc_1">Click to upload an image
          </div>
          <img :src="imageSrc_1" alt="Uploaded Image" v-else style="width: 100%; height: 100%; object-fit: contain;" />
        </div>

        <div class="vs-text">
            VS
        </div>

        <div class="upload-container_2" @click="triggerInput_2">
          <p v-if="!other_user_id"> 请选择好友上传 </p>
          <p v-if="other_user_id"> 等待对方上传 </p>
          <input type="file" ref="fileInput" @change="handleFileUpload_2" style="display: none;" />
          <div v-if="!imageSrc_2">Click to upload an image
          </div>
          <img :src="imageSrc_2" alt="Uploaded Image" v-else style="width: 100%; height: 100%; object-fit: contain;" />
        </div>

        <div v-if = "isresponsed" class="result-test-1">
          {{text_1}}:{{point_1}}
        </div>

        <div v-if = "isresponsed" class="result-test-2">
          {{text_2}}:{{point_2}}
        </div>

        <div>
          <button class="pk-button" @click="facePk"> 颜值打分 </button>
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
  padding: 60px;

  display:grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 2fr 2fr 1fr;
  background-color: coral;
  justify-items: center;
}

.upload-container_1 {
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

.vs-text{
  grid-column: 2;
  grid-row: 1;

  justify-content: center; /* 水平方向起始对齐 */
  align-content: center;
  font-size: 60px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

.result-test-1{
  grid-column: 1;
  grid-row: 2;

  justify-content: center; /* 水平方向起始对齐 */
  align-content: center;
  font-size: 40px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

.result-test-2{
  grid-column: 3;
  grid-row: 2;

  justify-content: center; /* 水平方向起始对齐 */
  align-content: center;
  font-size: 40px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

.upload-container_2 {
  grid-column: 3;
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

.pk-button{
  grid-column: 2;
  grid-row: 3;

  width: 80%; /* 按钮宽度占满整个格子 */
  height: 60%; /* 按钮高度占满整个格子 */
  text-align: center;
  border: none; /* 去掉边框 */
  background-color: #03fbb1; /* 设置背景颜色 */
  color: white; /* 设置字体颜色 */
  font-size: 16px; /* 设置字体大小 */
  cursor: pointer; /* 设置鼠标悬停时的光标样式 */
  outline: none; /* 去掉焦点时的轮廓 */
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