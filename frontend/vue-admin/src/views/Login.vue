<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">溺水死亡鉴识系统登录</div>
      <el-form :model="param" :rules="rules" ref="param" label-width="0px" class="ms-content">
        <el-form-item prop="account">
          <el-input v-model="param.account" placeholder="请输入账号" prefix-icon="el-icon-user">
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" placeholder="请输入密码" v-model="param.password" prefix-icon="el-icon-lock">
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="submitForm('param')">登录</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { loginTenant } from '@/api';
import { setToken } from '@/utils/auth';
import Cookies from "js-cookie";
export default {
  name: "Login",
  data() {
    return {
      param: {
        account: "",
        password: "",
      },
      rules: {
        account: [
          {
            required: true,
            message: "请输入账号",
            trigger: "blur",
          },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
    };
  },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            const csrfToken = Cookies.get("csrftoken"); // 从 Cookies 获取 CSRF Token

            loginTenant(this.param, csrfToken)
              .then((res) => {
                const { code, msg, token } = res;
                localStorage.setItem('username', res.username);
                localStorage.setItem('name', res.name);
                // 后端返回 userInfo.is_admin 为 true/false
                localStorage.setItem('is_admin', res.is_admin ? "1" : "0");
                if (code !== 0) {
                  this.$message({
                    showClose: true,
                    message: msg,
                    type: "error",
                  });
                } else {
                  this.$message({
                    showClose: true,
                    message: "登录成功",
                    type: "success",
                  });
                  Cookies.set("token", token);
                  localStorage.setItem("n", JSON.stringify("1"));
                  this.$router.push("/dashboard");
                }
              })
              .catch((err) => {
                console.error(err);
                this.$message({
                  showClose: true,
                  message: "服务器错误",
                  type: "error",
                });
              });
          } else {
            return false;
          }
        });
    },
  },
  
}
</script>

<style scoped>
.login-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url(../assets/img/login-bg.jpg);
  background-size: 100%;
}

.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: #fff;
  border-bottom: 1px solid #ddd;
}

.ms-login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}

.ms-content {
  padding: 30px 30px;
}

.login-btn {
  text-align: center;
}

.login-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}

.login-tips {
  font-size: 12px;
  line-height: 30px;
  color: #fff;
}
</style>