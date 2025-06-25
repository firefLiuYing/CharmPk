<script setup lang = ts>
    import { createApp } from 'vue'
    import {ref} from "vue";

    const app = createApp({})

    app.component(
      // 注册的名字
      'globalComponent',
      // 组件的实现
      {

      }
    )
</script>


<style scoped>

</style>