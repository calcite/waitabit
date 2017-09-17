// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import CallPanel from './components/CallPanel'
import CallInput from './components/CallInput'
import Entry from './components/Entry'

Vue.config.productionTip = false
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {path: '/', name: 'entry', component: Entry},
    {path: '/panel', name: 'call-panel', component: CallPanel},
    {path: '/input', name: 'call-input', component: CallInput}
  ]
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  // template: '<App/>',
  router,
  render: h => h(App)
  // components: { App }
})
