import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios';
import * as echarts from 'echarts';

const app = createApp(App)

app.config.globalProperties.$echarts = echarts
app.config.globalProperties.$axios = axios //全局注册，使用方法为:this.$axios
app.config.productionTip = false //阻止vue 在启动时生成生产提示。

app.use(ElementPlus);
app.mount('#app')




// import { createApp } from 'vue'
// import App from './App.vue'

// createApp(App).mount('#app')
