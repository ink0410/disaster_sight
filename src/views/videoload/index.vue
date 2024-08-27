<template>
  <div class="app-container video-upload-page">
    <!-- 左半部分：视频播放画布 -->
    <el-row>
      <!-- 左半部分：视频播放画布 -->
      <el-col :span="15">
        <video controls width="100%" height="400px">
          <source src="your_video_url.mp4" type="video/mp4">
        </video>
        <el-form>
          <el-form-item class="video-btn" label="标题" />
          <el-form-item class="video-btn" label="源时间" />
        </el-form></el-col>

      <!-- 右半部分：标题、发生地和确认上传按钮 -->
      <el-col :span="9">
        <el-form label-width="100px">
          <el-form-item class="video-btn" label="标题">
            <el-input v-model="videoTitle" />
          </el-form-item>
          <el-form-item class="video-btn" width="230">
            <el-button class="video-btn video-btn-row" type="primary" @click="handleDisasterType">灾害类型</el-button>
            <el-button class="video-btn video-btn-row" type="primary" @click="handleScene">场景</el-button>
            <el-button class="video-btn video-btn-row" type="primary" @click="handleEmergencyLevel">紧急程度</el-button>
          </el-form-item>
          <el-form-item class="video-btn" label="信息内容">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="标志物信息">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="源时间">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="发生地">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="搜集时间">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="搜集时间">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="url">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="搜集人">
            <el-input v-model="videoLocation" />
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
      videoTitle: '',
      videoLocation: ''
    }
  },
  methods: {
    uploadVideo() {
      // 处理上传逻辑，例如发送数据到后端
      console.log('标题：', this.videoTitle)
      console.log('发生地：', this.videoLocation)
      // 在这里添加上传视频的操作
    }
  }
}
</script>

<style lang="scss" scoped>
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
}

</style>
