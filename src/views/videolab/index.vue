<template>
  <div class="video-library">
    <!-- 筛选条件 -->
    <div class="video-library">
      <!-- 筛选条件 -->
      <div class="filters">
        <el-select v-model="selectedLocation" placeholder="选择地点">
          <el-option label="巴黎" value="巴黎" />
          <el-option label="纽约" value="纽约" />
        <!-- 添加其他地点选项 -->
        </el-select>

        <el-select v-model="selectedDisasterType" placeholder="选择灾害类型">
          <el-option label="山洪" value="山洪" />
          <el-option label="内涝" value="内涝" />
        <!-- 添加其他灾害类型选项 -->
        </el-select>

        <el-select v-model="selectedScene" placeholder="选择场景">
          <el-option label="村居" value="村居" />
          <el-option label="街道" value="街道" />
        <!-- 添加其他场景选项 -->
        </el-select>

        <el-select v-model="selectedUrgency" placeholder="选择紧急程度">
          <el-option label="普通" value="普通" />
          <el-option label="紧急" value="紧急" />
        <!-- 添加其他紧急程度选项 -->
        </el-select>

        <el-form-item label-width="120px" label="Publish Time:" class="postInfo-container-item">
          <el-date-picker v-model="displayTime" type="datetime" format="yyyy-MM-dd HH:mm:ss" placeholder="Select date and time" />
        </el-form-item>

      <!-- 添加时间选择组件 -->
      </div>

      <!-- 视频列表 -->
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
  </div></template>

<script>
export default {
  data() {
    return {
      selectedLocation: '', // 用户选择的地点
      // 其他筛选条件的数据
      videos: [
        { id: 1, name: '视频1', time: '2023-05-01', location: '巴黎', type: '洪灾', scene: '城市', urgency: '高' }
        // 其他视频数据
      ]
    }
  },
  computed: {
    filteredVideos() {
      // 根据筛选条件过滤视频数据
      return this.videos.filter(video => {
        return (!this.selectedLocation || video.location === this.selectedLocation)
        // 添加其他筛选条件的逻辑
      })
    }
  }
}
</script>

<style scoped>
.video-library {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
}

.video-list {
  margin-bottom: 20px;
}

.video-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}
</style>
