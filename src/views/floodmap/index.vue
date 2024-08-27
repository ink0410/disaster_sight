<template>
  <div class="flood-map-page">
    <el-row>
      <el-col :span="16">
        <!-- 地图部分 -->
        <h2>洪灾地图</h2>
        <div class="map-container">
          <MapView />
        </div>
      </el-col>
      <el-col :span="8">
        <!-- 洪灾信息部分 -->
        <div class="flood-info">
          <h2>洪灾信息</h2>
          <ul>
            <li v-for="(info, index) in floodInfo" :key="index">
              {{ info }}
            </li>
          </ul>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import MapView from './components/MapView.vue'

export default {
  name: 'FloodMapPage',
  components: {
    MapView
  },
  data() {
    return {
      floodInfo: [
        '洪灾区域1 - 严重程度: 高',
        '洪灾区域2 - 严重程度: 中',
        '洪灾区域3 - 严重程度: 低',
        '洪灾区域4 - 严重程度: 高',
        '洪灾区域5 - 严重程度: 中',
        '洪灾区域6 - 严重程度: 低'
      ]
    }
  }
}

</script>

<style scoped>
.flood-map-page {
  padding: 20px;
}

.map-container {
  height: 500px; /* 设置地图容器高度 */
  margin-bottom: 20px;
}

.flood-info {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.flood-info ul {
  list-style-type: none;
  padding: 0;
}

.flood-info li {
  margin-bottom: 10px;
}
</style>
