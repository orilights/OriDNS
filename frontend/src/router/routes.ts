import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [

  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页',
      requireAuth: true,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '登录',
    },
  },
  {
    path: '/domain/:domain',
    name: 'domain',
    component: () => import('@/views/Domain.vue'),
    meta: {
      title: '域名详情',
      requireAuth: true,
    },
  },
]

export default routes
