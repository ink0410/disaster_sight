<template>
  <div class="video-library">
    <!-- 分类栏 -->
    <h2 class="category-title">分类栏</h2>

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

      <el-date-picker
        v-model="saleTime"
        type="daterange"
        value-format="yyyy-MM-dd HH:mm:ss"
        format="yyyy-MM-dd"
        :default-time="['00:00:00', '23:59:59']"
        range-separator="-"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        size="mini"
        :picker-options="pickerOptions"
        @change="dateChangePicker"
      />

      <el-button type="primary" @click="filterVideos">筛选</el-button>
    </div>

    <!-- 视频列表 -->
    <div v-for="(videos, yearMonth) in groupedVideos" :key="yearMonth">
      <h3>{{ yearMonth }}</h3>
      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col v-for="video in videos" :key="video.id" :span="6" class="video-item">
          <video controls :src="video.src" />
        </el-col>
      </el-row>
    </div>

    <!-- 分页 -->
    <el-pagination
      background
      layout="prev, pager, next"
      :total="filteredVideos.length"
      :page-size="8"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedLocation: '', // 用户选择的地点
      selectedDisasterType: '', // 用户选择的灾害类型
      selectedScene: '', // 用户选择的场景
      selectedUrgency: '', // 用户选择的紧急程度
      selectedYearMonth: '', // 用户选择的年月
      videos: [
        { id: 1, name: '视频1', time: '2023-05-01', location: '巴黎', type: '洪灾', scene: '城市', urgency: '高', src: 'emergencyVideo21' },
        { id: 2, name: '视频2', time: '2023-06-01', location: '纽约', type: '内涝', scene: '村居', urgency: '低', src: 'emergencyVideo22' }
        // 其他视频数据
      ],
      currentPage: 1,
      pageSize: 8
    }
  },
  computed: {
    filteredVideos() {
      // 根据筛选条件过滤视频数据
      return this.videos.filter(video => {
        return (!this.selectedLocation || video.location === this.selectedLocation) &&
               (!this.selectedDisasterType || video.type === this.selectedDisasterType) &&
               (!this.selectedScene || video.scene === this.selectedScene) &&
               (!this.selectedUrgency || video.urgency === this.selectedUrgency) &&
               (!this.selectedYearMonth || video.time.startsWith(this.selectedYearMonth))
      })
    },
    paginatedVideos() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredVideos.slice(start, end)
    },
    groupedVideos() {
      const grouped = {}
      this.paginatedVideos.forEach(video => {
        const yearMonth = video.time.slice(0, 7) // 提取年月
        if (!grouped[yearMonth]) {
          grouped[yearMonth] = []
        }
        grouped[yearMonth].push(video)
      })
      return grouped
    }
  },
  methods: {
    handlePageChange(page) {
      this.currentPage = page
    },
    filterVideos() {
      this.currentPage = 1 // 重置分页
    }
  }
}
</script>

<style scoped>
.video-library {
  padding: 20px;
}

.category-title {
  text-align: center;
}

.filters {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.video-item {
  margin-bottom: 20px;
}

.video-item video {
  width: 100%;
}
</style>
