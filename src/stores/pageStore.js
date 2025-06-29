// stores/useUserStore.js
import { defineStore } from 'pinia'
import {ref} from 'vue'

export const useGlobalStore = defineStore('global', () => {

  const pageFirstName = ref('faceEvaluate')
  const pageLastName = ref('faceEvaluate')
  const nickname = ref('nickname')
  const userIcon = ref(null)
  const user_id = ref(null)
  const other_user_id = ref(null)

  function changeFirstName (name) {
    pageFirstName.value = name
  }

  function changeLastName (name) {
    pageLastName.value = name
  }

   return {
     pageFirstName,
     pageLastName,
     nickname,
     userIcon,
     user_id,
     other_user_id,

     changeFirstName,
     changeLastName
  }

  // // 状态 (相当于 data)
  // const count = ref(0)
  // const user = ref(null)
  // const loading = ref(false)
  //
  // // 计算属性 (相当于 computed)
  // const isAuthenticated = computed(() => user.value !== null)
  // const userName = computed(() => user.value?.name || 'Guest')
  //
  // // 操作方法 (相当于 methods)
  // async function login(credentials) {
  //   loading.value = true
  //   try {
  //     user.value = await api.login(credentials)
  //   } finally {
  //     loading.value = false
  //   }
  // }
  //
  // function increment() {
  //   count.value++
  // }
  //
  // function logout() {
  //   user.value = null
  //   count.value = 0
  // }

  // 返回所有需要暴露的状态和方法

})
