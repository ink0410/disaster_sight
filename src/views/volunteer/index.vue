<template>
  <div class="volunteer-dashboard">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-button type="primary" @click="signIn">签到</el-button>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card>
          <div>今日在岗时长: {{ todayHours }} 小时</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div>今日贡献值: {{ todayContribution }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div>本周贡献值: {{ weekContribution }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="4">
        <el-tag type="danger" effect="dark">紧急任务</el-tag>
      </el-col>
      <el-col :span="5">
        <video controls :src="emergencyVideo1" />
      </el-col>
      <el-col :span="5">
        <video controls :src="emergencyVideo2" />
      </el-col>
      <el-col :span="5">
        <video controls :src="emergencyVideo3" />
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="6">
        <video controls :src="emergencyVideo21" />
      </el-col>
      <el-col :span="6">
        <video controls :src="emergencyVideo22" />
      </el-col>
      <el-col :span="6">
        <video controls :src="emergencyVideo23" />
      </el-col>
      <el-col :span="6">
        <video controls :src="emergencyVideo24" />
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      todayHours: 0,
      todayContribution: 0,
      weekContribution: 0,
      emergencyVideo1: 'video1.mp4',
      emergencyVideo2: 'video2.mp4',
      emergencyVideo3: 'video3.mp4',
      emergencyVideo21: 'video21.mp4',
      emergencyVideo22: 'video22.mp4',
      emergencyVideo23: 'video23.mp4',
      emergencyVideo24: 'video24.mp4'
    }
  },
  mounted() {
    // 在这里添加获取数据的逻辑
  },
  methods: {
    signIn() {
      // 在这里添加签到逻辑
      console.log('签到成功')
    }
  }
}
</script>

<style scoped>
.volunteer-dashboard {
  padding: 20px;
}
</style>
