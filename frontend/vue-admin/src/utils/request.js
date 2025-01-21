import axios from "axios";
import {Message} from 'element-ui';
import { getToken } from "@/utils/auth";
import Cookies from "js-cookie";

const service = axios.create({
  baseURL: "http://58.199.165.140:10102",
  timeout: 1000000, // request timeout
  headers: {
    'Content-Type': 'application/json', // 确保发送和接收 JSON 格式
},
});

// 请求拦截器，添加token


service.interceptors.request.use((config) => {
  const csrfToken = Cookies.get("csrftoken"); // 从 Cookies 获取 CSRF Token
  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }
  return config;
});

// 响应拦截器
service.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response && error.response.status === 401) {
      Message.error("身份验证失败，请重新登录");
      Cookies.remove("token"); // 清除 token
      window.location.href = "/login"; // 重定向到登录页面
    }
    return Promise.reject(error);
  }
);

export default service;
