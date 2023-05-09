import { createRouter, createWebHashHistory } from 'vue-router'
import { useToast } from 'vue-toastification'
import routes from './routes'
import { useStore } from '@/store'
import { getTokenExpTime } from '@/utils/token'
import { tokenRefresh, tokenVerify } from '@/utils/api'

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach(async (to, from) => {
  const store = useStore()
  if (!store.login) {
    const token = localStorage.getItem('token')
    if (token) {
      const expTime = getTokenExpTime(token)
      if (expTime <= 0) {
        localStorage.removeItem('token')
        useToast().warning('登录过期，请重新登录')
      }
      else {
        try {
          const res = await tokenVerify(token)
          const data = await res.json()
          if (data.success) {
            store.login = true
            store.token = token
            if (expTime < 604800) {
              tokenRefresh(token)
                .then(res => res.json())
                .then((data) => {
                  if (data.success) {
                    store.token = data.token
                    localStorage.setItem('token', data.token)
                  }
                  else {
                    useToast().warning('服务器或网络错误')
                  }
                })
                .catch(() => {
                  useToast().warning('服务器或网络错误')
                })
            }
          }
          else {
            localStorage.removeItem('token')
            useToast().warning('登录过期，请重新登录')
          }
        }
        catch (err) {
          useToast().warning('服务器或网络错误')
        }
      }
    }
  }
  if (to.meta.title)
    document.title = `${to.meta.title} - OriDNS`

  if (to.name === 'login' && store.login) {
    return {
      path: '/',
    }
  }
  if (to.meta.requireAuth && !store.login) {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath,
      },
    }
  }
})

export default router
