
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
            <el-date-picker v-model="sourceTime" type="datetime" format="yyyy-MM-dd HH:mm:ss" placeholder="Select date and time" />
          </el-form-item>
          <el-form-item class="video-btn" label="发生地*">
            <el-input v-model="videoLocation" />
          </el-form-item>
          <el-form-item class="video-btn" label="搜集时间*">
            <el-date-picker v-model="collectionTime" type="datetime" format="yyyy-MM-dd HH:mm:ss" placeholder="Select date and time" />
          </el-form-item>
          <el-form-item class="video-btn" label="信息源*">
            <el-select v-model="informationSource" placeholder="请选择" class="center-placeholder">
              <el-option label="抖音" value="douyin" />
              <el-option label="微信群" value="wechat" />
              <el-option label="小红书" value="redbook" />
            </el-select>
          </el-form-item>
          <el-form-item class="video-btn" label="url">
            <el-input v-model="videoUrl" />
          </el-form-item>
          <el-form-item class="video-btn" label="搜集人*">
            <el-input v-model="volunteer_id" />
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
import axios from 'axios'
import { mapGetters } from 'vuex'
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
      volunteer_id: '',
      markerInfo: '', // 标志物信息
      informationSource: '', // 信息源
      depth: '',
      video_id: ''
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  created() {
    this.videoUrl = this.$route.query.videoUrl
    this.video_id = this.$route.query.video_id
    this.volunteer_id = this.name
    this.video_id = this.$route.query.video_id
  },

  methods: {
    toggleSignIn() {
      this.isSignedIn = !this.isSignedIn
    },
    uploadVideo() {
      const data = {
        /* title: this.videoTitle,
        disasterType: this.selectedDisasterType,
        scene: this.selectedScene,
        emergencyLevel: this.selectedEmergencyLevel,
        message: this.videoMessage,
        sourceTime: this.sourceTime,
        location: this.videoLocation,
        collectionTime: this.collectionTime,

        depth: this.depth,*/
        // markerInfo: JSON.stringify(this.markerInfo)
        upload_channel: this.informationSource,
        upload_volunteer_id: this.name,
        upload_video_id: this.video_id
        // video_stored_path: JSON.stringify(this.videoUrl)// 确保发送的是 JSON 字符串
        // potential_landmark: JSON.stringify(this.potentialLandmark) // 添加缺失的字段
      }
      const information = {
        /* title: this.videoTitle,
        disasterType: this.selectedDisasterType,
        scene: this.selectedScene,
        emergencyLevel: this.selectedEmergencyLevel,
        message: this.videoMessage,
        sourceTime: this.sourceTime,
        location: this.videoLocation,
        collectionTime: this.collectionTime,

        depth: this.depth,*/
        // markerInfo: JSON.stringify(this.markerInfo)
        create_time: this.sourceTime,
        video_title: this.videoTitle,
        video_id: this.video_id
        // video_stored_path: JSON.stringify(this.videoUrl)// 确保发送的是 JSON 字符串
        // potential_landmark: JSON.stringify(this.potentialLandmark) // 添加缺失的字段
      }
      axios.post('/uploadTasks/upload', data)
        .then(response => {
          console.log('上传成功:', response.data)
        })
        .catch(error => {
          console.error('上传失败:', error)
          this.$message.error('上传失败')
        })
      axios.post('/videoInformation/upload', information)
        .then(response => {
          console.log('上传成功:', response.data)
          this.$router.push({
            path: '/tasklab/index',
            query: { }
          })
        })
        .catch(error => {
          console.error('上传失败:', error)
          this.$message.error('上传失败')
        })
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
