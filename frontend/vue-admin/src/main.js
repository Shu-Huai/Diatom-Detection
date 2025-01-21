import Vue from 'vue'
import App from './App.vue'
import service from './utils/request';
import VueRouter from 'vue-router'

import router from '@/router'

import Cookies from 'js-cookie';


import dayjs from 'dayjs';

import axios from 'axios';


import VueAnimateNumber from 'vue-animate-number'

import JsonExcel from 'vue-json-excel'


import { VueJsonp } from 'vue-jsonp'



import {Switch,Popconfirm,InputNumber,TabPane,Tabs,TimePicker,Image,MessageBox,DropdownMenu, Avatar, Dropdown, Icon, DropdownItem, Notification, DescriptionsItem, Descriptions, Loading, Col, DatePicker, Radio, RadioGroup, Message, Button, Menu, Submenu, MenuItemGroup, MenuItem,  Dialog, Form, Input, FormItem, Select, Option, Breadcrumb, BreadcrumbItem, Upload, Table, TableColumn, Tag, Pagination, PageHeader } from 'element-ui';

Vue.prototype.$http = service;
Vue.component('el-button', Button)
Vue.component('el-dropdown-menu', DropdownMenu)
Vue.component('el-menu', Menu)
Vue.component('el-submenu', Submenu)
Vue.component('el-menu-item-group', MenuItemGroup)
Vue.component('el-menu-item', MenuItem)
Vue.component('el-dialog', Dialog)
Vue.component('el-form', Form)
Vue.component('el-input', Input)
Vue.component('el-form-item', FormItem)
Vue.component('el-select', Select)
Vue.component('el-option', Option)
Vue.component('el-breadcrumb', Breadcrumb)
Vue.component('el-breadcrumb-item', BreadcrumbItem)
Vue.component('el-upload', Upload)
Vue.component('el-table', Table)
Vue.component('el-table-column', TableColumn)
Vue.component('el-tag', Tag)
Vue.component('el-pagination', Pagination)
Vue.component('el-page-header', PageHeader)
Vue.component('el-radio-group', RadioGroup)
Vue.component('el-radio', Radio)
Vue.component('el-date-picker', DatePicker)
Vue.component('el-col', Col)
Vue.component('el-descriptions', Descriptions)
Vue.component('el-descriptions-item', DescriptionsItem)
Vue.component('el-icon', Icon)
Vue.component('el-dropdown-item', DropdownItem)
Vue.component('el-dropdown', Dropdown)
Vue.component('el-avatar', Avatar)
Vue.component('el-image',Image)
Vue.component('el-time-picker',TimePicker)
Vue.component('el-tabs',Tabs)
Vue.component('el-tab-pane',TabPane)
Vue.component('el-input-number',InputNumber)
Vue.component('el-popconfirm',Popconfirm)
Vue.component('el-switch',Switch);


Vue.config.productionTip = false

//应用插件
Vue.use(VueRouter)
Vue.use(Loading)
Vue.use(VueAnimateNumber)
Vue.use(VueJsonp)




new Vue({
  el: '#app',
  render: h => h(App),
  router,
  //安装全局事件总线
  beforeCreate() {
    Vue.prototype.$bus = this
    Vue.prototype.$message = Message
    Vue.prototype.$mm=MessageBox
    Vue.prototype.$alter = MessageBox.alert
    Vue.prototype.$confirm = MessageBox.confirm
    Vue.prototype.$loading = Loading.service
    Vue.prototype.$dayjs = dayjs
    Vue.prototype.$loading=Loading.service
    Vue.prototype.axios=axios
    Vue.prototype.$notify = Notification
    Vue.prototype.$cookies=Cookies
  }
})
