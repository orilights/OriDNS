import Toast from 'vue-toastification'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'

import '@/assets/tailwind.css'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast)

app.mount('#app')
