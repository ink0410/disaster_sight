<template>
  <div class="video-upload-page">
    <el-row gutter="20" class="centered-row">
      <el-col :span="12">
        <!-- 视频上传组件 -->
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>视频上传</span>
          </div>
          <div class="video-upload">
            <el-upload
              class="upload-demo"
              action="#"
              :before-upload="beforeUploadVideo"
              :on-change="handleVideoChange"
              :show-file-list="true"
              drag
              multiple
              :accept="'video/*'"
            >
              <el-button size="small" type="primary">
                <i class="el-icon-upload" /> 点击上传视频
              </el-button>
            </el-upload>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <!-- URL 粘贴组件 -->
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>粘贴视频 URL</span>
          </div>
          <div class="url-paste">
            <el-input
              v-model="videoUrl"
              placeholder="粘贴视频 URL"
            />
            <el-button size="small" type="primary" @click="handlePasteUrl">
              <i class="el-icon-link" /> 上传
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      uploadedFiles: [],
      videoUrl: null
    }
  },
  methods: {
    beforeUploadVideo(file) {
      const isVideo = file.type.startsWith('video/')
      const isLt50M = file.size / 1024 / 1024 < 50

      if (!isVideo) {
        this.$message.error('请上传正确的视频格式')
        return false
      }
      if (!isLt50M) {
        this.$message.error('视频大小不能超过50MB')
        return false
      }
      return true
    },
    handleVideoChange(file) {
      // 检查文件是否已经存在
      const fileExists = this.uploadedFiles.some(uploadedFile => {
        // 输出已上传文件的名字
        return uploadedFile.name === file.name && uploadedFile.size === file.size
      })

      if (!fileExists) {
        const videoFile = file.raw
        this.videoUrl = URL.createObjectURL(videoFile)
        this.uploadedFiles.push(file.raw)
        const data = {
          video_stored_path: JSON.stringify(this.videoUrl)// 确保发送的是 JSON 字符串
        }
        axios.post('/videos/', data)
          .then(response => {
            this.video_id = response.data.video.video_id
            this.$router.push({
              path: '/videoload/index',
              query: { videoUrl: this.videoUrl, video_id: this.video_id }
            })
          })
          .catch(error => {
            console.error('上传失败:', error)
            this.$message.error('上传失败')
          })
      } else {
        console.log('文件已存在，不再重复上传')
      }
    },
    handlePasteUrl() {
      // 处理粘贴 URL 后的逻辑
      console.log('粘贴的 URL：', this.videoUrl)
      const data = {
        video_stored_path: JSON.stringify(this.videoUrl)// 确保发送的是 JSON 字符串
      }
      axios.post('/videos/', data)
        .then(response => {
          this.video_id = response.data.video.video_id
          this.$router.push({
            path: '/videoload/index',
            query: { videoUrl: this.videoUrl, video_id: this.video_id }
          })
        })
        .catch(error => {
          console.error('上传失败:', error)
          this.$message.error('上传失败')
        })
    }
  }
}
</script>

<style scoped>
.video-upload-page {
  padding: 20px;
  height: 100vh; /* 使页面高度为视口高度 */
  display: flex;
  align-items: center; /* 垂直居中 */
}

.centered-row {
  width: 100%;
}

.video-upload,
.url-paste {
  margin-bottom: 20px;
}

.box-card {
  margin-bottom: 20px;
}

.el-button {
  margin-top: 10px;
}
</style>
