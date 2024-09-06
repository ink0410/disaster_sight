<template>
  <div class="dashboard-container">
    <!-- 左侧部分 -->
    <div class="left-section">
      <!-- 签到/签退按钮 -->
      <el-button type="primary" class="sign-button" @click="toggleSignIn">{{ isSignedIn ? '签退' : '签到' }}</el-button>

      <!-- 提示文字 -->
      <div class="footer-text">
        救灾任务紧急，但也别忘记照顾自己哦~
      </div>
    </div>

    <!-- 右侧部分 -->
    <div class="right-section">
      <el-card>
        <p>今日在岗时长: </p>
        <p>{{ todayWorkHours }} 小时</p>
      </el-card>
      <el-card>
        <p>今日贡献值: </p>
        <p>上传: {{ todayUpload }} </p>
        <p>审核: {{ todayReview }}</p>
      </el-card>
      <el-card>
        <p>本周贡献值: </p>
        <p>上传: {{ todayUpload }} </p>
        <p>审核: {{ todayReview }}</p>

      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSignedIn: false, // 签到状态
      todayWorkHours: 8, // 示例数据
      todayUpload: 5,
      todayReview: 3,
      weekUpload: 20,
      weekReview: 15
    }
  },
  methods: {
    toggleSignIn() {
      this.isSignedIn = !this.isSignedIn
      this.$message.success(this.isSignedIn ? '签到成功！' : '签退成功！')
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100vh;
  padding: 20px;
}

.left-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.sign-button {
  margin-bottom: 150px;
  align-items: center;
  margin-left: 150px
}

.footer-text {
  font-size: 14px;
  color: #666;
  margin-left: 100px
}

.right-section {
  width: 300px;
}

.el-card {
  text-align: center;
  margin-bottom: 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.el-card p {
  margin: 10px 0;
  font-size: 16px;
  color: #333;
}
</style>
