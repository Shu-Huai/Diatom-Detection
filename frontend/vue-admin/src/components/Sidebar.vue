<template>
  <div class="sidebar">
    <el-menu
      :default-active="n"
      class="sidebar-el-menu"
      background-color="#324157"
      text-color="#bfcbd9"
      active-text-color="#20a0ff"
      @select="handleSelect"
      :collapse="isCollapse"
    >
      <el-menu-item index="1">
        <i class="el-icon-menu"></i>
        <span>系统首页</span>
      </el-menu-item>
      <el-menu-item index="2">
        <i class="el-icon-user"></i>
        <span>用户管理</span>
      </el-menu-item>
      <el-menu-item index="3">
        <i class="el-icon-monitor"></i>
        <span>自定义样本测试</span>
      </el-menu-item>
      <el-menu-item index="4">
        <i class="el-icon-picture"></i>
        <span>数字切片展示</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>
 
<script>
export default {
  name: "Sidebar",
  data() {
    return {
      n: JSON.parse(localStorage.getItem("n")) || "1",
      isCollapse: false,
    };
  },
  methods: {
    handleSelect(key) {
      localStorage.setItem("n", JSON.stringify(key));
      this.n = key; // 动态更新高亮项
      if (key == "1") {
        this.$router.push("/dashboard").catch((err) => {});
      } else if (key == "2") {
        this.$router.push("/userAdmin").catch((err) => {});
      } else if (key == "3") {
        this.$router.push("/customTest").catch((err) => {});
      } else if (key == "4") {
        this.$router.push("/svsDisplay").catch((err) => {});
      }
    },
  },
  created() {
    const currentPath = this.$route.path;
    let defaultKey = "1"; // 默认值

    if (currentPath === "/dashboard") {
      defaultKey = "1";
    } else if (currentPath === "/userAdmin") {
      defaultKey = "2";
    } else if (currentPath === "/customTest") {
      defaultKey = "3";
    } else if (currentPath === "/svsDisplay") {
      defaultKey = "4";
    }

    this.n = defaultKey; // 设置高亮项
    localStorage.setItem("n", JSON.stringify(defaultKey)); // 同步 sessionStorage
    this.$bus.$on("tt", (data) => {
      this.isCollapse = data;
    });
  },
};
</script>

<style scoped>
.sidebar {
  display: block;
  position: absolute;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: scroll;
}
.sidebar::-webkit-scrollbar {
  width: 0;
}
.sidebar-el-menu:not(.el-menu--collapse) {
  width: 250px;
}
.sidebar > ul {
  height: 100%;
}

.iconfont{
  margin-right: 10px;
  font-size: 18px;
}
</style>
