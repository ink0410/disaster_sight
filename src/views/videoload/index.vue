<template>
  <div class="app-container video-upload-page">
    <!-- 左半部分：视频播放画布 -->
    <el-row>
      <!-- 左半部分：视频播放画布 -->
      <el-col :span="15">
        <video controls width="100%" height="400px">
          <source v-if="videoUrl" :src="videoUrl" type="video/mp4">
        </video>
        <el-form>
          <el-form-item class="video-btn" :label="'标题: ' + videoTitle" />
          <el-form-item class="video-btn" :label="'源时间: ' + sourceTime" />

        </el-form></el-col>

      <!-- 右半部分：标题、发生地和确认上传按钮 -->
      <el-col :span="9">
        <el-form label-width="100px">
          <el-form-item class="video-btn" label="标题*">
            <el-input v-model="videoTitle" />
          </el-form-item>
          <el-form-item class="video-btn" label="灾害类型">
            <el-select v-model="selectedDisasterType" placeholder="请选择" class="center-placeholder">
              <el-option label="地震" value="earthquake" />
              <el-option label="洪水" value="flood" />
              <el-option label="火灾" value="fire" />
            </el-select>
          </el-form-item>
          <el-form-item label="场景" class="video-btn">
            <el-select v-model="selectedScene" placeholder="请选择" class="center-placeholder">
              <el-option label="城市" value="city" />
              <el-option label="农村" value="village" />
              <el-option label="森林" value="forest" />
            </el-select>
          </el-form-item>
          <el-form-item label="紧急程度" class="video-btn">
            <el-select v-model="selectedEmergencyLevel" placeholder="请选择" class="center-placeholder">
              <el-option label="低" value="low" />
              <el-option label="中" value="medium" />
              <el-option label="高" value="high" />
            </el-select>
          </el-form-item>
          <el-form-item class="video-btn" label="信息内容">
            <el-input v-model="videoMessage" />
          </el-form-item>
          <el-form-item class="video-btn" label="标志物信息">
            <el-input v-model="markerInfo" />
          </el-form-item>
          <el-form-item class="video-btn" label="源时间*">
            <el-input v-model="sourceTime" />
          </el-form-item>
          <el-form-item class="video-btn" label="发生地*">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="搜集时间*">
            <el-input v-model="collectionTime" />
          </el-form-item>
          <el-form-item class="video-btn" label="信息源*">
            <el-input v-model="informationSource" />
          </el-form-item>
          <el-form-item class="video-btn" label="url">
            <el-input v-model="videoUrl" />
          </el-form-item>
          <el-form-item class="video-btn" label="搜集人*">
            <el-input v-model="collector" />
          </el-form-item>
          <el-form-item class="video-btn" label="水位深度">
            <div class="input-group">
              <el-input v-model="depth" />
              <el-button class="small-btn" type="primary" @click="uploadVideo">智能识别</el-button>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button class="video-btn" type="primary" @click="uploadVideo">确认上传</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSignedIn: false,
      workHoursToday: 0,
      contributionToday: {
        uploads: 0,
        reviews: 0
      },
      contributionWeek: {
        uploads: 0,
        reviews: 0
      },
      videoUrl: '',
      selectedDisasterType: '',
      selectedScene: '',
      selectedEmergencyLevel: '',
      videoMessage: '',
      videoTitle: '',
      videoLocation: '',
      sourceTime: '',
      collectionTime: '',
      collector: '',
      markerInfo: '', // 标志物信息
      informationSource: '', // 信息源
      depth: ''
    }
  },
  created() {
    this.videoUrl = this.$route.query.videoUrl
  },
  methods: {
    toggleSignIn() {
      this.isSignedIn = !this.isSignedIn
    },
    uploadVideo() {
      if (!this.videoTitle || !this.selectedDisasterType || !this.videoLocation || !this.sourceTime || !this.collectionTime || !this.collector) {
        this.$message.error('请填写所有必填项')
        return
      }
      // 处理上传逻辑，例如发送数据到后端
      console.log('标题：', this.videoTitle)
      console.log('灾害类型：', this.selectedDisasterType)
      console.log('场景：', this.selectedScene)
      console.log('紧急程度：', this.selectedEmergencyLevel)
      console.log('信息内容：', this.videoMessage)
      console.log('源时间：', this.sourceTime)
      console.log('发生地：', this.videoLocation)
      console.log('搜集时间：', this.collectionTime)
      console.log('搜集人：', this.collector)
      // 在这里添加上传视频的操作
    },
    handleDisasterType() {
      // 处理灾害类型选择逻辑
      console.log(this.selectedDisasterType)
    },
    handleScene() {
      // 处理场景选择逻辑
      console.log(this.selectedScene)
    },
    handleEmergencyLevel() {
      // 处理紧急程度选择逻辑
      console.log(this.selectedEmergencyLevel)
    },
    handleWaterDepth() {
      console.log(this.depth)
    }
  }
}
</script>

<style lang="scss" scoped>
.center-placeholder .el-input__inner {
  text-align: center;
}
.video-upload-page {

  display: flex;
  flex-wrap: wrap;

  .video-btn {
    display: block;
    margin-bottom: 5px;
    font-weight: normal;
    font-family: "华文楷体", sans-serif;
    color: black;
    margin: 0 auto;
    .video-btn-row {
      justify-content: space-between;
      width: 100px;
      height: 40px;
      align-items: center;
    }
  }
  .input-group {
  display: flex;
  align-items: center;
  }

  .small-btn {
  margin-left: 10px; /* 调整按钮与输入框的间距 */
  padding: 5px 10px; /* 调整按钮的大小 */
  }
}

</style>
