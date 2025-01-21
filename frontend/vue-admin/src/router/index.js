//引入路由
import VueRouter from 'vue-router'

import Cookies from 'js-cookie'


import Login from '@/views/Login'
import Home from '@/views/Home'
import Dashboard from '@/views/Dashboard'
import UserAdmin from '@/views/UserAdmin'
import CustomTest from '@/views/CustomTest'
import SvsDisplay from '@/views/SvsDisplay'

const router = new VueRouter({
    routes: [
        { path: '/', redirect: 'login' },
        {
            path: '/login',
            component: Login,
            meta: { is: true, title: '系统后台登录' }
        },
        {
            path: '/',
            component: Home,
            children: [
                {
                    path: "dashboard",
                    component: Dashboard,
                    meta: { title: '系统首页', isAust: true }
                },
                {
                    path: "userAdmin",
                    component: UserAdmin,
                    meta: { title: '用户管理', isAust: true }
                },
                {
                    path: "customTest",
                    component: CustomTest,
                    meta: { title: '自定义样本测试', isAust: true }
                },
                {
                    path: "svsDisplay",
                    component: SvsDisplay,
                    meta: { title: '数字切片展示', isAust: true }
                },
            ],
        }
    ]
})

//全局前置路由守卫----初始化的时候被调用,每次路由切换之前被调用  这个可以限制访问路由组件
router.beforeEach((to, from, next) => {
    const token = Cookies.get("token");
  
    if (to.meta.is) {
      if (token) {
        next("/dashboard");
      } else {
        next();
      }
    } else if (to.meta.isAust) {
      if (token) {
        next();
      } else {
        next("/login");
      }
    } else {
      next();
    }
  });

//全局后置路由守卫---初始化的时候被调用,每次路由切换之后被调用 这个可以用来切换网页的标题
router.afterEach((to, form) => {
    if (to.meta.title) {
        //切换网页标题
        document.title = to.meta.title
    } else {
        document.title = '系统后台'
    }

})
export default router