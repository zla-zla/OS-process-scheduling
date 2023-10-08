为了实现前后端分离的开发理念，开发前端 SPA（single page web application） 项目，实现数据绑定，路由配置，项目编译打包等一系列工作的技术框架。



## npm指令

```
vue create 【项目名】		//创建项目
npm run serve					//启动项目
npm install qs.js --save　　//它的作用是能把json格式的直接转成data所需的格式
```

## 解析代码段

```
new Vue({
    render: h => h(App),
}).$mount('#app')
```

$mount(’#app’) ：手动[挂载](https://so.csdn.net/so/search?q=挂载&spm=1001.2101.3001.7020)到id为app的dom中的意思。这里创建的vue实例没有el属性，而是在实例后面添加了一个$mount(’#app’)方法。当Vue实例没有el属性时，则该实例尚没有挂载到某个dom中；假如需要延迟挂载，可以在之后手动调用vm.$mount()方法来挂载需要注意的是：该方法是直接挂载到入口文件index.html 的 id=app 的dom 元素上的

render函数是vue通过js渲染dom结构的函数createElement，约定可以简写为h.这个函数的作用就是生成一个 VNode节点，
render 函数得到这个 VNode 节点之后，返回给 Vue.js 的 mount 函数，渲染成真实 DOM 节点，并挂载到根节点上。

## 项目目录结构

```
node_modules（npm 加载的项目依赖模块）
public（公共资源）
src（开发目录）
    assets（图片等文件）
    components（组件）
    router（路由）
    store（vuex）
    views（页面）
    App.vue（核心页）
    main.js（核心文件）
browserslistrc（这个配置能够分享目标浏览器和nodejs版本在不同的前端工具。这些工具能根据目标浏览器自动来进行配置）
eslintrc.js（ESlint配置文件）
gitignore（git配置文件）
babel.config.js（babel配置文件）
package-lock.json（依赖版本锁定）
package.json（项目信息及依赖信息）
README.md（项目介绍）
```

## Vue.prototype

在main.js中添加一个变量到 Vue.prototype

```javascript
Vue.prototype.$appName = 'My App'
```

这样 $appName 就在所有的 Vue 实例中可用了，甚至在实例被创建之前就可以。

每个组件都是一个vue实例，Vue.prototype加一个变量，只是给每个组件加了一个属性，这个属性的值并不具有全局性。

**如果要实现全局变量的功能，需要把属性变为引用类型**

```javascript
Vue.prototype.$appName = { name: 'main' }
```

**后面使用 this.$appName.name 改变和引用相应的值**



## 属性

### 数据

每个 Vue 应用都是通过用 `Vue` 函数创建一个新的 **Vue 实例**开始的：

```
var vm = new Vue({
  // 选项
})
```

所有的 Vue 组件都是 Vue 实例，并且接受相同的选项对象 (一些根实例特有的选项除外)。

当一个 Vue 实例被创建时，它将 `data` 对象中的所有的 property 加入到 Vue 的**响应式系统**中。当这些 property 的值发生改变时，视图将会产生“响应”，即匹配更新为新的值。

当这些数据改变时，视图会进行重渲染。值得注意的是只有当实例被创建时就已经存在于 `data` 中的 property 才是**响应式**的。也就是说如果你添加一个新的 property，比如：

```
vm.b = 'hi'
```

那么对 `b` 的改动将不会触发任何视图的更新。如果你知道你会在晚些时候需要一个 property，但是一开始它为空或不存在，那么你仅需要设置一些初始值。比如：

```
data: {
  newTodoText: '',
  visitCount: 0,
  hideCompletedTodos: false,
  todos: [],
  error: null
}
```

除了数据 property，Vue 实例还暴露了一些有用的实例 property 与方法。它们都有前缀 `$`，以便与用户定义的 property 区分开来。



### 方法属性

我们用 `methods` 选项向组件实例添加方法，它应该是一个包含所需方法的对象：

```js
const app = Vue.createApp({
  data() {
    return { count: 4 }
  },
  methods: {
    increment() {
      // `this` 指向该组件实例
      this.count++
    }
  }
})
const vm = app.mount('#app')
console.log(vm.count) // => 4
vm.increment()
console.log(vm.count) // => 5
```

这些 `methods` 和组件实例的其它所有 property 一样可以在组件的模板中被访问。在模板中，它们通常被当做事件监听使用。你可以在模板支持 JavaScript 表达式的任何地方调用方法。





### 计算属性

模板内的表达式非常便利，但是设计它们的初衷是用于简单运算的。在模板中放入太多的逻辑会让模板过重且难以维护。所以，对于任何包含响应式数据的复杂逻辑，你都应该使用**计算属性**。

```
<div id="example">
  <p>Original message: "{{ message }}"</p>
  <p>Computed reversed message: "{{ reversedMessage }}"</p>
</div>
```

```
var vm = new Vue({
  el: '#example',
  data: {
    message: 'Hello'
  },
  computed: {
    // 计算属性的 getter
    reversedMessage: function () {
      // `this` 指向 vm 实例
      return this.message.split('').reverse().join('')
    }
  }
})
```

我们可以将同一函数定义为一个方法而不是一个计算属性。两种方式的最终结果确实是完全相同的。然而，不同的是**计算属性是基于它们的响应式依赖进行缓存的**。只在相关响应式依赖发生改变时它们才会重新求值。这就意味着只要 `message` 还没有发生改变，多次访问 `reversedMessage` 计算属性会立即返回之前的计算结果，而不必再次执行函数。

计算属性默认只有 getter，不过在需要时你也可以提供一个 setter：

```
// ...
computed: {
  fullName: {
    // getter
    get: function () {
      return this.firstName + ' ' + this.lastName
    },
    // setter
    set: function (newValue) {
      var names = newValue.split(' ')
      this.firstName = names[0]
      this.lastName = names[names.length - 1]
    }
  }
}
// ...
```

### 侦听属性

这就是为什么 Vue 通过 `watch` 选项提供了一个更通用的方法，来响应数据的变化。当需要在数据变化时执行异步或开销较大的操作时，这个方式是最有用的。







## axios

基于`promise`用于浏览器和`node.js`的http客户端，因此可以使用Promise API	

在vue项目的`main.js`文件中引入`axios`

```typescript
import axios from 'axios'
Vue.prototype.$axios = axios
```

在组件中使用axios

```html
<script>
	export default {
		mounted(){
			this.$axios.get('/goods.json').then(res=>{
				console.log(res.data);
			})
		}
	}
</script>
```

axios实例常用配置

```
baseURL 请求的域名，基本地址，类型：String
timeout 请求超时时长，单位ms，类型：Number
url 请求路径，类型：String
method 请求方法，类型：String
headers 设置请求头，类型：Object
params 请求参数，将参数拼接在URL上，类型：Object
data 请求参数，将参数放到请求体中，类型：Object
```

```
//全局配置
this.$axios.defaults.timeout = 2000;//配置全局的超时时长
this.$axios.defaults.baseURL = 'http://localhost:8080';//配置全局的基本URL
//实例配置
let instance = this.$axios.create();
instance.defaults.timeout = 3000;
```

## element

```
<el-container>：外层容器。当子元素中包含 <el-header> 或 <el-footer> 时，全部子元素会垂直上下排列，否则会水平左右排列
<el-header>：顶栏容器
<el-aside>：侧边栏容器
<el-main>：主要区域容器
<el-footer>：底栏容器
```









运行别人的vue：https://www.php.cn/website-design-ask-481967.html