import service from "@/utils/request";



//查看首页数据
export function countData() {
  return service.get('/customtest/data'); // 确保与后端路径一致
}

// 登录API
export const loginTenant = (data, csrfToken) => {
  return service.post('/users/login/', data, {
    headers: {
      "X-CSRFToken": csrfToken, // 附加 CSRF Token
    },
  });
};


/*
  用户管理api
*/

// 搜索用户
export const querySearchUser = (data) => {
  return service.get('/users/', { params: data });
};

// 获取用户列表
export const queryUser = (params) => {
  return service.get('/users/', { params });
};

// 更新用户信息 API
export const upUserInfo = (id, data) => {
  return service.put(`/users/update/${id}/`, data);
};

export const addUser = (data) => {
  return service.post("/users/create/", data);
};

export function deleteUsers(userIds) {
  return service.delete('/users/delete/', { data: { user_ids: userIds } });
};

export function changePassword(userId, data) {
  return service.post(`/users/change_password/${userId}/`, data);
}

