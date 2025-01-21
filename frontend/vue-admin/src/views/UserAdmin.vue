<template>
  <div>
    <div class="container">
      <!-- 搜索框 -->
      <div class="handle-box">
        <el-input placeholder="请输入关键字" v-model="searchQuery" style="width:20%; padding-right:10px;"></el-input>
        <el-select v-model="searchField" placeholder="选择筛选条件" style="width:20%; padding-right:10px;">
          <el-option label="账号" value="username"></el-option>
          <el-option label="姓名" value="name"></el-option>
          <el-option label="电话" value="phone"></el-option>
          <el-option label="邮箱" value="email"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch" icon="el-icon-search">搜索</el-button>
        <el-button type="success" @click="addUserDialogVisible = true" :disabled="!isAdmin">新增用户</el-button>
        <el-button type="danger" @click="deleteSelectedUsers" :disabled="!isAdmin || !selectedUsers.length">删除选中</el-button>
      </div>

      <!-- 用户表 -->
      <el-table :data="tableData" border style="width: 100%;" ref="userTable" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" min-width="55"></el-table-column>
        <el-table-column prop="id" label="ID" min-width="80"></el-table-column>
        <el-table-column prop="username" label="账号" min-width="120"></el-table-column>
        <el-table-column prop="name" label="姓名" min-width="120"></el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="180"></el-table-column>
        <el-table-column prop="phone" label="电话" min-width="150"></el-table-column>
        <el-table-column prop="is_admin" label="管理员" min-width="120">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.is_admin" type="success">是</el-tag>
            <el-tag v-else type="info">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="220" fixed="right">
          <template slot-scope="scope">
            <el-button class="same-width-btn" size="mini" type="primary" @click="editUser(scope.row)">修改信息</el-button>
            <br />
            <el-button class="same-width-btn" size="mini" type="warning" @click="handleChangePassword(scope.row)">修改密码</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination @current-change="handlePageChange" :current-page="currentPage" :page-size="pageSize" :total="total" layout="total, prev, pager, next"></el-pagination>
    </div>

    <!-- 修改用户对话框 -->
    <el-dialog title="修改用户" :visible.sync="editUserDialogVisible">
      <el-form :model="currentEditUser" :rules="rules" ref="editForm" label-width="100px">
        <el-form-item label="账号" prop="username">
          <el-input v-model="currentEditUser.username" :disabled="!is_admin"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="currentEditUser.name"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="currentEditUser.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="currentEditUser.email"></el-input>
        </el-form-item>
        <el-form-item label="管理员权限" prop="is_admin">
          <el-switch v-model="currentEditUser.is_admin" :disabled="!isAdmin"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editUserDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUser">保存</el-button>
      </template>
    </el-dialog>


    <!-- 修改密码对话框 -->
    <el-dialog title="修改密码" :visible.sync="changePwdDialogVisible">
      <el-form :rules="rules" ref="changePwdForm" :model="changePwdForm" label-width="100px">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="changePwdForm.old_password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="changePwdForm.new_password" type="password"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="changePwdDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="changePasswordSubmit">确认修改</el-button>
      </div>
    </el-dialog>


    <!-- 新增用户对话框 -->
    <el-dialog title="新增用户" :visible.sync="addUserDialogVisible">
      <el-form :model="newUser" :rules="rules" ref="addForm" label-width="100px">
        <el-form-item label="账号" prop="username">
          <el-input v-model="newUser.username"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="newUser.name"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="newUser.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="newUser.email"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="newUser.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="管理员权限" prop="is_admin">
          <el-switch v-model="newUser.is_admin"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addUserDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addUser">新增</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { queryUser, querySearchUser, upUserInfo, addUser, deleteUsers, changePassword } from "@/api";

export default {
  data() {
    return {
      tableData: [],
      is_admin: false,
      searchQuery: "",
      searchField: "username",
      currentPage: 1,
      pageSize: 10,
      total: 0,
      currentEditUser: {
        id: null, // 确保 id 存在
        name: "",
        email: "",
        phone: "",
        is_admin: false,
      },
      newUser: { is_admin: false },
      editUserDialogVisible: false,
      addUserDialogVisible: false,
      selectedUsers: [],
      changePwdDialogVisible: false,
      changePwdForm: {
        user_id: null,
        old_password: '',
        new_password: ''
      },
      msg: "",
      loading: false, // 确保loading已定义
      rules: {
        username: [{ required: true, message: "账号不能为空", trigger: "blur" }],
        name: [{ required: true, message: "姓名不能为空", trigger: "blur" }],

        email: [
          { required: true, message: "邮箱不能为空", trigger: "blur" },
          { type: "email", message: "邮箱格式不正确", trigger: "blur" },
        ],
        phone: [
          { required: true, message: "电话不能为空", trigger: "blur" },
          {
            pattern: /^((13[0-9])|(14[0|5|6|7|9])|(15[0|1|2|3|5|6|7|8|9])|(16[2|5|6|7])|(17[0|1|2|3|5|6|7|8])|(18[0-9])|(19[0|1|2|3|5|6|7|8|9]))\d{8}$/,
            message: "电话格式不正确", trigger: "blur"
          },
        ],
        password: [{ required: true, message: "密码不能为空", trigger: "blur" }],
        old_password: [{ required: true, message: "密码不能为空", trigger: "blur" }],
        new_password: [{ required: true, message: "密码不能为空", trigger: "blur" }],
      },
    };
  },
  computed: {
    isAdmin() {
      // 判断当前用户是否为管理员
      return localStorage.getItem('is_admin') === '1';
    },
  },
  methods: {
    async handleSearch() {
      const res = await querySearchUser({
        query: this.searchQuery,
        field: this.searchField,
        page: this.currentPage,
        pageSize: this.pageSize,
      });
      this.tableData = res.data;
      this.total = res.total;
    },
    async handlePageChange(page) {
      this.currentPage = page;
      await this.getUserList();
    },
    async getUserList() {
      try {
        this.loading = true; // 开始加载
        const res = await queryUser({ page: this.currentPage, pageSize: this.pageSize });
        if (res && res.data) {
          this.tableData = res.data;
          this.total = res.total || 0;
        } else {
          this.tableData = [];
          this.total = 0;
        }
      } catch (error) {
        console.error("获取用户列表失败:", error);
        this.$message.error("无法加载用户数据");
      } finally {
        this.loading = false; // 结束加载
      }
    },
    editUser(user) {
      const currentUsername = localStorage.getItem('username');
      const isAdmin = localStorage.getItem('is_admin') === '1';

      // 如果不是管理员 并且 要修改的账号 != 自己的账号 -> 禁止操作
      if (!isAdmin && user.username !== currentUsername) {
        this.$message.warning("你没有权限修改其他账号信息");
        return;
      }

      // 允许修改
      this.currentEditUser = { ...user };
      this.editUserDialogVisible = true;
    },
    async saveUser() {
      // 1. validate 校验表单
      this.$refs.editForm.validate(async (valid) => {
        if (!valid) {
          this.$message.error("请完善表单信息后再提交");
          return;
        }
        // 2. 若校验通过，再进行后续逻辑
        if (!this.currentEditUser.id) {
          this.$message.error("用户 ID 缺失，无法更新！");
          return;
        }

        try {
          const res = await upUserInfo(this.currentEditUser.id, this.currentEditUser);
          if (res.code === 0) {
            this.$message.success("用户信息更新成功！");
            this.editUserDialogVisible = false;
            this.getUserList(); // 刷新用户列表
          } else {
            this.$message.error(res.msg || "更新失败！");
          }
        } catch (error) {
          console.error("更新用户信息失败:", error);
          this.$message.error("服务器错误，请稍后重试！");
        }
      });
    },
    handleChangePassword(user) {
      const currentUsername = localStorage.getItem('username');
      const isAdmin = localStorage.getItem('is_admin') === '1';

      // 如果非管理员，且要改别人密码
      if (!isAdmin && user.username !== currentUsername) {
        this.$message.warning("你没有权限修改其他账号的密码");
        return;
      }

      // 打开对话框
      this.changePwdForm.user_id = user.id;
      this.changePwdForm.old_password = '';
      this.changePwdForm.new_password = '';
      this.changePwdDialogVisible = true;
    },
    async changePasswordSubmit() {
      // 调用后端 change_password/<user_id>/ 接口
      this.$refs.changePwdForm.validate(async (valid) => {
        if (!valid) {
          // 如果校验不通过，则终止新增逻辑
          this.$message.error("请完善表单信息后再提交");
          return;
        }
        try {
          const { user_id, old_password, new_password } = this.changePwdForm;
          const res = await changePassword(user_id, { old_password, new_password });
          if (res.code === 0) {
            this.$message.success("密码修改成功！");
            this.changePwdDialogVisible = false;
          } else {
            this.$message.error(res.msg || "修改密码失败");
          }
        } catch (e) {
          console.error(e);
          this.$message.error("服务器错误，请稍后重试");
        }
      })
    },
    async addUser() {
      // 1. 调用 validate 校验
      this.$refs.addForm.validate(async (valid) => {
        if (!valid) {
          // 如果校验不通过，则终止新增逻辑
          this.$message.error("请完善表单信息后再提交");
          return;
        }
        try {
          const res = await addUser(this.newUser);
          console.log("dddddddddddddddddddddddddd")
          console.log(res)
          if (res.code === 0) {
            this.$message.success("用户创建成功！");
            this.addUserDialogVisible = false;
            this.getUserList();
          } else {
            this.$message.error(res.msg || "用户创建失败！");
          }
        } catch (error) {
          console.error("创建用户失败:", error);
          if (error.response) {
            // 如果后端返回了错误信息，显示错误信息
            this.$message.error(error.response.data.msg || "服务器错误，请稍后重试！");
          } else {
            // 否则，显示通用的错误信息
            this.$message.error("服务器错误，请稍后重试！");
          }
        }
      });
    },
    async deleteSelectedUsers() {
      if (this.selectedUsers.length === 0) {
        this.$message.warning('请选择要删除的用户！');
        return;
      }
      if (this.selectedUsers.some(user => user.username === localStorage.getItem('username'))) {
        this.$message.warning('不能删除当前登录用户！');
        return;
      }
      try {
        // 等待用户在对话框中选择：“确定” or “取消”
        await this.$confirm('确定要删除选中的用户吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        });

        // 如果执行到这里，表示点击了“确定”
        const userIds = this.selectedUsers.map(user => user.id);
        // 如果此处 deleteUsers 出现错误，也会抛到下方的 catch
        await deleteUsers(userIds);
        this.$message.success('用户删除成功！');
        this.getUserList(); // 刷新用户列表

      } catch (err) {
        // 如果是对话框点击“取消”或关闭，Element 会默认抛出一个 'cancel' 或类似的错误信息
        if (err === 'cancel' || err === 'close') {
          this.$message.info('已取消删除操作');
        } else {
          // 其他错误，比如后端返回 4xx / 5xx
          console.error('删除用户失败:', err);
          this.$message.error('删除用户失败，请检查网络或联系管理员');
        }
      }
    },
    async getUserPage() {
      try {
        this.loading = true;
        let pageNum = this.page;
        let pageSize = this.size;
        const res = await queryUser({ pageNum, pageSize });
        const { code, data } = res;
        if (code === 0) {
          this.tableData = data.list;
          this.total = data.total;
        } else {
          this.$message.error('获取用户列表失败');
        }
      } catch (error) {
        console.error('加载用户列表失败:', error);
        this.$message.error('加载用户列表失败，请检查网络');
      } finally {
        this.loading = false;
      }
    },
    handleSelectionChange(val) {
      this.selectedUsers = val;
    },
  },
  created() {
    this.getUserList();
  },
};
</script>

<style>
.container {
  width: 100%;
  box-sizing: border-box;
  /* 确保包括 padding 和 border */
}

.el-table {
  width: 100%;
  table-layout: fixed;
}

.handle-box {
  margin-bottom: 20px;
}

.button-column {
  display: flex;
  flex-direction: column;
  /* 纵向排列 */
  gap: 8px;
  /* 两按钮间距（可按需调整） */
}

.same-width-btn {
  min-width: 80px;
  /* 或者一个更适合的宽度，比如 100px */
}
</style>
