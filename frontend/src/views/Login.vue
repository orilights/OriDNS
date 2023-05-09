<template>
  <div>
    <h2 class="text-2xl font-bold py-2 mb-3">
      用户登录
    </h2>
    <div class="my-2">
      账号：<input
        v-model="username" type="text"
        class="px-2 py-1 border border-gray-400 hover:border-blue-500 rounded-md outline-none"
      >
    </div>
    <div class="my-2">
      密码：<input
        v-model="password" type="password"
        class="px-2 py-1 border border-gray-400 hover:border-blue-500 rounded-md outline-none"
        @keydown.enter="handleLogin"
      >
    </div>
    <button
      class="px-4 py-1 mt-3 mr-2 bg-blue-500 text-white hover:bg-blue-400 border rounded-lg transition-all"
      @click="handleLogin"
    >
      登录
    </button>
  </div>
</template>

<script setup lang="ts">
import { useToast } from 'vue-toastification'
import { useStore } from '@/store'
import { userLogin } from '@/utils/api'

const store = useStore()
const toast = useToast()
const router = useRouter()
const route = useRoute()

const redirect = route.query.redirect
const username = ref('')
const password = ref('')

function handleLogin() {
  if (username.value.trim() === '' || password.value.trim() === '') {
    toast.error('账号或密码不能为空')
    return
  }
  userLogin(username.value, password.value)
    .then(res => res.json())
    .then((data) => {
      if (data.success === true) {
        toast.success('登录成功')
        store.login = true
        store.token = data.data.token
        localStorage.setItem('token', data.data.token)
        if (redirect)
          router.push(redirect as string)
        else
          router.push('/')
      }
      else {
        toast.error(data.msg)
      }
    })
    .catch((err) => {
      toast.error(err.message)
    })
}
</script>
