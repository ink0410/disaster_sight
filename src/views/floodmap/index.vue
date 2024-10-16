<template>
  <div class="flood-map-page">
    <el-row>
      <el-col :span="16">
        <!-- 地图部分 -->
        <h2>洪灾地图</h2>
        <div class="map-container">
          <mmap v-if="dataLoaded" :data_position="positions" />

        </div>
      </el-col>
      <el-col :span="8">
        <!-- 洪灾信息部分 -->
        <div class="flood-info">
          <h2>实时新闻</h2>
          <div class="roll-component">
            <roll :data="items" :height="itemHeight">
              <template v-slot:main="{ item }">
                <el-card class="box-card" shadow="hover">
                  <div>
                    <i class="el-icon-message-solid" />
                    <span class="timestamp">{{ item.timestamp }}</span>
                    <el-link :href="item.source" :underline="false" target="_blank" icon="el-icon-bottom-right" style="float: right;font-weight: bold; padding: 2px 0;font-size: 0.6em;">来源</el-link>
                  </div>
                  <div class="content">
                    {{ item.title }}:{{ item.description }}
                  </div>

                </el-card>
              </template>
            </roll>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import mmap from './components/map.vue'
import roll from './components/rroll.vue'
import axios from 'axios'
// import VueAMap from 'vue-amap'
export default {
  name: 'FloodMapPage',
  components: {
    mmap,
    roll
  },
  data() {
    return {
      // 数据状态变量
      dataLoaded: false,
      // 标记点位置
      // positions: [
      // 只能使用position
      // {position: [121.59996, 31.197646]},
      // {position: [121.69996, 31.197646]},
      // {position: [121.79996, 31.197646]},
      // {position: [121.89996, 31.197646]},
      // {position: [121.99996, 31.197646]},
      // ],
      positions: [],
      // 新闻
      items: [
        { id: 1,
          title: '水利部：5省新增12条河流发生超警以上洪水',
          source: 'https://news.cctv.com/2024/09/20/ARTI4dvPnFUGboPsvR1F1V8S240920.shtml',
          timestamp: '2 天前',
          description: '水利部9月20日发布消息，受降雨及上游来水影响，19日8时至20日8时，山东、安徽、甘肃、福建、海南新增12条河流发生超警以上洪水。其中，山东胜利河出现1969年有实测资料以来最高水位，安徽新沱河出现1970年有实测资料以来最大流量。' },
        { id: 2,
          title: '黄河兰州段洪水防御Ⅳ级应急响应启动！甘肃发布地质灾害+山洪灾害双预警',
          source: 'https://finance.sina.com.cn/jjxw/2024-09-04/doc-incmyqsm6124809.shtml',
          timestamp: '18 天前',
          description: '甘肃省水利厅消息，自4日9时起，针对兰州市启动洪水防御Ⅳ级应急响应。9月3日起，甘肃省黄河兰州段以上出现强降雨过程，湟水、大通河、庄浪河等支流发生洪水。' },
        { id: 3,
          title: '黑龙江省发布中小河流洪水、山洪灾害、地质灾害气象风险预警',
          source: 'https://finance.sina.com.cn/wm/2024-08-19/doc-inckcrwq1525673.shtml',
          timestamp: '34 天前',
          description: '黑龙江省人民政府防汛抗旱指挥部办公室、黑龙江省水利厅、黑龙江省气象局8月18日20时联合发布中小河流洪水气象风险预警：预计8月18日20时-20日20时，安达、青冈、大庆、肇源、肇州、杜尔伯特、五常、泰来、龙江、茄子河区、勃利、穆棱、林口、绥芬河、东宁有一定风险发生中小河流洪水（蓝色预警），请上述地区做好中小河流洪水的实时监测、防汛预警、巡查防守、转移避险和抢险救援等防范工作。' },
        { id: 4,
          title: '哈尔滨市气象局连发三道预警！涉及地质灾害、山洪灾害、中小河流洪水风险',
          source: 'https://finance.sina.com.cn/jjxw/2024-08-18/doc-inckaqmf0400404.shtml',
          timestamp: '35 天前',
          description: '哈尔滨市自然资源和规划局、哈尔滨市气象局8月18日20时联合发布地质灾害气象风险蓝色预警：受强降雨影响，预计8月18日20时—20日20时五常有一定风险发生地质灾害，请注意防范强降雨引发的崩塌、滑坡、泥石流等地质灾害，做好监测预警和转移避险等工作。' },
        { id: 5,
          title: '水利部：多条河流可能发生洪水过程 局地山洪灾害风险较高',
          source: 'https://finance.sina.com.cn/jjxw/2024-08-18/doc-inckaqmf0400404.shtml',
          timestamp: '40 天前',
          description: '人民网北京8月13日电 (欧阳易佳)记者从水利部获悉，未来一周，受强降雨影响，海河流域滦河、潮白河，黄河流域渭河，长江流域岷江，珠江流域西江干支流，辽河流域辽河、大凌河，鸭绿江等河流可能发生洪水过程，暴雨区内中小河流洪水和局地山洪灾害风险较高。' }

      ],
      itemHeight: 40 // 每个项目高度，单位像素

    }
  },
  mounted() {
    this.getVideoInfo()
  },
  //   createded() {
  //   this.getVideoInfo()
  // },

  methods: {

    async getVideoInfo() {
      axios.get('/mapView/all')
        .then(response => {
          // 将传来的数据赋值给 positions
          console.log(response)
          // const formattedPositions = response.data.mapViews.map(item => ({
          //   position: [item.location_longitude, item.location_latitude],
          //   video: item.video,
          //   content: item.video_information
          // }))

          // console.log(formattedPositions)
          // this.positions = formattedPositions
          this.positions = response.data.mapViews
          console.log('index的位置信息', this.positions)
          console.log('获取信息成功:', response.data)

          this.dataLoaded = true
        })
        .catch(error => {
          console.error('获取信息失败:', error)
        })
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

    height: 600px;
    border-radius: 8px;
  }

  .flood-info ul {
    list-style-type: none;
    padding: 0;
  }

  .flood-info li {
    margin-bottom: 10px;
  }
  .roll-component {
    position: relative;
    height: 500px; /* 设置一个固定的高度 */
    background-color: #fff; /* 可选：设置背景颜色 */
  }

  .timestamp{
    font-size: 0.8em;
    color: #8b8787;
    padding: 2px 0
  }
  .content{
    font-size: 1em;
    color: #181717;
    padding: 12px 0
  }

  </style>
