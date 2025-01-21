<template>
  <div class="header">
    <div class="collapse-btn" @click="collapseChage">
      <el-icon class="el-icon-s-unfold" v-show="tt"></el-icon>
      <el-icon class="el-icon-s-fold" v-show="!tt"></el-icon>
    </div>
    <div class="logo">硅藻检测系统</div>
    <div class="header-right">
      <div class="header-user-con">
        <!-- 用户头像 -->
        <el-avatar class="user-avator" :size="38" :src="imgurl" />
        <!-- 用户名下拉菜单 -->
        <el-dropdown class="user-name" trigger="click" @command="back">
          <span class="el-dropdown-link">
            {{ name }}
            <el-icon class="el-icon-arrow-down el-icon--right">
              <arrow-down />
            </el-icon>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item  divided command="loginOut">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>
<script>
import imgurl from '@/assets/img/tx.jpg';
import { removeToken } from '@/utils/auth';
export default {
  name: "Header",
  data() {
    return {
      imgurl: require("@/assets/img/tx.jpg"),
      name: "",
      tt: false,
    };
  },
  methods: {
    collapseChage() {
      this.tt = !this.tt;
      this.$bus.$emit("tt", this.tt);
    },
    back(comm){
      if(comm=='loginOut'){
        this.$confirm("是否确定退出登陆?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
          })
            .then(() => {
              removeToken();
              this.$router.replace({ path: '/login' });
              this.$message({
                type: "success",
                message: "退出成功",
              });
            })
            .catch(() => {});
      }
      
    }
  },
  created() {
    this.$bus.$emit("tt", this.tt);
    this.name = localStorage.getItem('name') || '超级管理员';
  },
};
</script>
<style scoped>
.header {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  height: 70px;
  font-size: 22px;
  color: #fff;
}
.collapse-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  float: left;
  padding: 0 21px;
  cursor: pointer;
}
.header .logo {
  padding: 0 20px;
  float: left;
  width: 250px;
  line-height: 70px;
}
.header-right {
  float: right;
  padding-right: 50px;
}
.header-user-con {
  display: flex;
  height: 70px;
  align-items: center;
}
.btn-fullscreen {
  transform: rotate(45deg);
  margin-right: 5px;
  font-size: 24px;
}
.btn-bell,
.btn-fullscreen {
  position: relative;
  width: 30px;
  height: 30px;
  text-align: center;
  border-radius: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.btn-bell-badge {
  position: absolute;
  right: 4px;
  top: 0px;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background: #f56c6c;
  color: #fff;
}
.btn-bell .el-icon-lx-notice {
  color: #fff;
}
.user-name {
  margin-left: 10px;
}
.user-avator {
  margin-left: 20px;
}
.el-dropdown-link {
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.el-dropdown-menu__item {
  text-align: center;
}
</style>
