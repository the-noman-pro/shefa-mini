import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@fontsource-variable/fraunces/full.css'
import '@fontsource-variable/instrument-sans'
import './styles/tokens.css'
import './styles/base.css'
import App from './App.vue'
import router from './router'

createApp(App).use(createPinia()).use(router).mount('#app')
