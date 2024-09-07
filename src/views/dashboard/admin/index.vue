<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <h2>任务盘点</h2>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <el-icon><i class="el-icon-document" /></el-icon>
                <div>待审核: <strong>{{ pendingTasks }}</strong></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <el-icon><i class="el-icon-warning" /></el-icon>
                <div>紧急待处理: <strong>{{ urgentTasks }}</strong></div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <h2>人力盘点</h2>
          <el-row :gutter="20">
            <el-col v-for="(count, type) in manpower" :key="type" :span="8">
              <el-card>
                <el-icon><i class="el-icon-user" /></el-icon>
                <div>{{ type }}: <strong>{{ count }}</strong> 人在线</div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pendingTasks: 10, // 示例数据
      urgentTasks: 5, // 示例数据
      manpower: {
        '类型A': 15, // 示例数据
        '类型B': 8, // 示例数据
        '类型C': 12 // 示例数据
      }
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

h2 {
  margin-bottom: 10px;
  color: #409EFF;
}

.el-card {
  text-align: center;
  padding: 20px;
}

.el-icon {
  font-size: 24px;
  margin-bottom: 10px;
  color: #409EFF;
}
</style>
