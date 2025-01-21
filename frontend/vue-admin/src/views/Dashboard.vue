<template>
  <div class="dsh">
    <div class="grid-content grid-con-1">
      <el-icon class="grid-con-icon el-icon-user"></el-icon>
      <div class="grid-cont-right">
        <div class="grid-num">
          <animate-number from="0" :to="userCount" :key="userCount" duration="500"></animate-number>
        </div>
        <div>用户量</div>
      </div>
    </div>
    <div class="grid-content grid-con-2">
      <el-icon class="grid-con-icon el-icon-s-claim"></el-icon>
      <div class="grid-cont-right">
        <div class="grid-num">
          <animate-number from="0" :to="total_sample_num" :key="total_sample_num"></animate-number>
        </div>
        <div>样本量</div>
      </div>
    </div>
  </div>
</template>

<script>
import { countData } from '@/api';
export default {
  name: "Dashboard",
  data() {
    return {
      userCount:0,
      total_sample_num:0,
    };
  },
  created() {
    countData()
      .then((res) => {
        this.userCount = res.userCount; // 确保与后端返回的键名一致
        this.total_sample_num = res.total_sample_num; // 确保与后端返回的键名一致
      })
      .catch((err) => {
        console.error(err);
        this.$message({
          showClose: true,
          message: "服务器错误",
          type: "error",
        });
      });
  },
};
</script>

<style >
.dsh {
  display: flex;
  justify-content: space-around;
  /* border: 1px solid #000; */
}

.grid-content {
  width: 20%;
  display: flex;
  align-items: center;
  height: 100px;
  border: 1px solid #dddfe2;
}

.grid-cont-right {
  flex: 1;
  text-align: center;
  font-size: 14px;
  color: #999;
}

.grid-num {
  font-size: 30px;
  font-weight: bold;
}

.grid-con-icon {
  font-size: 50px;
  width: 100px;
  height: 100px;
  color: #fff;
}

.grid-con-1 .grid-con-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
  color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
  color: rgb(100, 213, 114);
}
</style>