//CustomTest.vue
<template>
  <div class="container">
    <!-- 操作区域：测试次数、测试样本数、启动测试 -->
    <div class="handle-box">
      <el-input
        v-model.number="k"
        placeholder="请输入测试次数(1~10)"
        type="number"
        style="width:200px;"
      />
      <el-input
        v-model.number="x"
        placeholder="请输入样本数(1~1000)"
        type="number"
        style="width:200px; margin-left:10px;"
      />
      <el-button
        type="primary"
        icon="el-icon-search"
        @click="startTest"
        :disabled="disableTestBtn"
        :loading="testLoading"
      >
        启动测试
      </el-button>
    </div>

    <!-- 若完成测试后，展示数据摘要 -->
    <el-card
      class="text-data-card"
      v-if="showSummary"
      style="margin-bottom: 10px;"
    >
      <div slot="header" class="title">数据摘要</div>
      <div class="content">
        <p class="summary">
          一共有
          <span class="highlight">{{ totalSampleNum }}</span>
          个样本，其中训练样本数为
          <span class="highlight">{{ totalTrainSampleNum }}</span>
          ，测试样本数为
          <span class="highlight">{{ totalTestSampleNum }}</span>
          。<br>
          本次定义了
          <span class="highlight">{{ k }}</span>
          次测试，每次随机选取
          <span class="highlight">{{ x }}</span>
          个样本。<br>
          <span v-for="(item, idx) in resultsList" :key="idx">
            第{{ item.round_index }}次测试，正确数：
            <span class="highlight">{{ item.predict_accurate_num }}</span>，
            准确率：
            <span class="highlight">{{ item.accuracy }}%</span>，
            查准率：
            <span class="highlight">{{ item.precision }}%</span>，
            查全率：
            <span class="highlight">{{ item.recall_rate }}%</span>。<br>
          </span>
          平均准确率：
          <span class="highlight">{{ avgAccuracy }}%</span>
          ，平均查准率：
          <span class="highlight">{{ avgPrecision }}%</span>
          ，平均查全率：
          <span class="highlight">{{ avgRecallRate }}%</span>
          ，方差：
          <span class="highlight">{{ variance }}</span>。<br>
          测试耗时：
          {{ testTime }}<br>
          完成时间：
          {{ endTime }}<br>
          以下是每一个测试样本的详细说明：
        </p>
      </div>
    </el-card>

    <!-- 导出Excel按钮（在数据摘要下面） -->
    <el-form style="margin-bottom: 10px;" v-if="showSummary">
      <el-form-item>
        <el-button type="primary" @click="exportExcel" :disabled="!testId">导出Excel</el-button>
      </el-form-item>
    </el-form>

    <!-- 表格：测试明细 -->
    <el-table
      :data="paginatedTableData"
      border
      class="table"
      v-loading="loadingTable"
      style="width: 100%;"
    >
      <el-table-column
        prop="test_no"
        width="60"
        align="center"
        label="序号"
      ></el-table-column>

      <el-table-column
        prop="test_sample_name"
        label="样本名称"
        min-width="120"
      ></el-table-column>

      <el-table-column
        prop="label"
        label="实际标签"
        min-width="100"
      ></el-table-column>

      <el-table-column
        prop="predict"
        label="测试标识"
        min-width="80"
      ></el-table-column>

      <el-table-column
        prop="predict_result"
        label="是否预测正确"
        min-width="120"
      >
        <template v-slot="scope">
          <el-tag v-if="scope.row.predict_result === 1" type="success">正确</el-tag>
          <el-tag v-else type="danger">错误</el-tag>
        </template>
      </el-table-column>
    </el-table> 

    <!-- 如果需要分页可以保留 -->
    <div class="pagination" v-if="showSummary">
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page.sync="page"
        :page-size="limit"
        layout="total, prev, pager, next"
        :total="total"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import service from "@/utils/request"; // 确保路径正确

export default {
  data() {
    return {
      k: null,
      x: null,
      testId: null,
      // 控制按钮 loading
      testLoading: false,
      // 控制摘要和表格是否显示
      showSummary: false,

      // 下面这些属性要与后端 JSON 返回的字段匹配
      resultsList: [],
      avgAccuracy: 0.0,
      avgPrecision: 0.0,
      avgRecallRate: 0.0,
      variance: 0.0,
      testTime: null,
      endtime: null,

      // 表格数据
      tableData: [],
      loadingTable: false,

      // 分页
      page: 1,
      limit: 10,
      total: 0,

      // 统计信息
      totalSampleNum: 0,
      totalTrainSampleNum: 0,
      totalTestSampleNum: 0,
    };
  },
  computed: {
    disableTestBtn(){
      // 如果 k,x 不在合法范围，就禁用
      return !(this.k >= 1 && this.k <= 10 && this.x >= 1 && this.x <= 1000);
    },
    paginatedTableData() {
      const start = (this.page - 1) * this.limit;
      const end = this.page * this.limit;
      return this.tableData.slice(start, end);
    }
  },
  methods: {
    startTest() {
      // 前端校验
      if (!(this.k >= 1 && this.k <= 10)) {
        this.$message.error('测试次数必须在1~10之间');
        return;
      }
      if (!(this.x >= 1 && this.x <= 1000)) {
        this.$message.error('样本数量必须在1~1000之间');
        return;
      }

      // 设置 loading 状态
      this.testLoading = true;
      this.loadingTable = true;
      this.showSummary = false; // 隐藏之前的摘要

      // 向 Django 后端发 POST 请求
      service.post('/customtest/custom-test/', {
        k: this.k,
        x: this.x
      },{ withCredentials: true })
      .then(res => {
        this.testLoading = false;
        this.loadingTable = false;

        if (res.code === 0) {
          // 把后端的字段赋给本地变量
          this.k = res.k;
          this.x = res.x;
          this.testId = res.test_id;  // 保存 test_id
          this.resultsList = res.results_list || [];
          this.avgAccuracy = res.avg_acc || null;
          this.avgPrecision = res.avg_prec || null;
          this.avgRecallRate = res.avg_rec || null;
          this.variance = res.variance || 0.0;
          this.testTime = res.test_time || '';
          this.endTime = res.end_time || '';

          // 表格数据
          this.tableData = res.table_data || [];

          // 统计信息
          this.totalSampleNum = res.total_sample_num || 0;
          this.totalTrainSampleNum = res.total_train_sample_num || 0;
          this.totalTestSampleNum = res.total_test_sample_num || 0;

          // 显示“数据摘要”和明细
          this.showSummary = true; 

          // 重置分页
          this.page = 1;
          this.limit = 10;
          this.total = this.tableData.length;


          // 提示成功消息
          this.$message.success(res.msg || '测试成功');
        } else {
          // 如果 code 不是 0, 可能是后端返回的错误
          this.$message.error(res.msg || '测试失败');
        }
      })
      .catch(err => {
        this.testLoading = false;
        this.loadingTable = false;
        console.error(err);
        // 检查错误响应
        if (err.response) {
          // 后端返回错误响应
          this.$message.error(`请求失败: ${err.response.data.msg || err.message}`);
        } else {
          // 网络错误或其他原因
          this.$message.error('请求出错，请检查网络或后端');
        }
      });
    },
    exportExcel() {
      if (!this.testId) {
        this.$message.error("请先进行测试");
        return;
      }
      // 使用反引号 `` ` `` 来正确插入 testId
      const url = `/customtest/export-excel/?test_id=${this.testId}`;
      console.log(`Export URL: ${url}`);  // 调试输出
      service({
        url: url,
        method: 'get',
        responseType: 'blob', // 确保响应类型为 blob
        withCredentials: true  // 确保携带会话 Cookie
      }).then(res => {
        // 'res' 是 Blob 对象
        const blob = res;
        const contentType = blob.type;
        if (contentType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
          // 成功获取到 Excel 文件
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          link.download = `test_result_${this.testId}.xlsx`;
          link.click();
          this.$message.success("导出成功");
        } else if (contentType === 'application/json') {
          // 后端返回了错误信息（JSON 格式）
          const reader = new FileReader();
          reader.onload = function() {
            try {
              const errorResponse = JSON.parse(reader.result);
              this.$message.error(errorResponse.msg || "导出失败");
            } catch (e) {
              this.$message.error("导出失败");
            }
          }.bind(this);
          reader.readAsText(blob);
        } else {
          this.$message.error("导出失败");
        }
      }).catch(err => {
        console.error('Export error:', err);
        this.$message.error("导出失败");
      });
    },


    handleCurrentChange(val){
      this.page = val;
      // 如需分页可在这里请求新的数据, 进行 slice
    }
  }
};
</script>

<style scoped>
.container {
  padding: 15px;
}
.handle-box {
  margin-bottom: 20px;
}
.table {
  width: 100%;
  font-size: 14px;
}
.text-data-card {
  margin-bottom: 10px;
}
.highlight {
  color: #007bff;
  font-weight: bold;
}
.summary {
  line-height: 1.5;
  letter-spacing: 1px;
}
.pagination {
  margin-top: 10px;
  text-align: right;
}
</style>
