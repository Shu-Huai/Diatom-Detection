// src/utils/auth.js
import Cookies from 'js-cookie';
export const getToken = () => {
  return localStorage.getItem('token');
};

export const setToken = (token) => {
  localStorage.setItem('token', token);
};

export const removeToken = () => {
  Cookies.remove('token');
};
