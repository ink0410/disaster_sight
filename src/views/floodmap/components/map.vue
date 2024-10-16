<template>
  <div class="amap-page-container">
    <el-amap
      vid="amapDemo"
      :center="center"
      :zoom="zoom"
      :events="events"
      :amap-manager="amapManager"
      :plugin="plugin"
      pitch-enable="false"
      class="amap-demo"
    >
      <!-- 遍历显示 -->
      <el-amap-marker
        v-for="(marker,index) in markers"
        :key="index"
        :position="marker.position"
        :events="marker.events"
      />
      <el-amap-info-window
        v-if="window"
        :position="window.position"
        :visible="window.visible"
        :content="window.content"
        :offset="window.offset"
        :close-when-click-map="true"
        :is-custom="true"
      >
        <div id="info-window">
          <!--    <p>{{ window.address }}</p>-->
          <div class="window_content">
            <p>源时间： {{ window.content.create_time }}</p>
            <p>视频内容： {{ window.content.video_title }}</p>
            <p>发生地： {{ window.content.video_location }}</p>
          </div>

          <div class="detail" @click="() => checkDetail(window.content.video.video_stored_path)">查看详情</div>
        </div>
      </el-amap-info-window>
    </el-amap>

    <div style="text-align: right;">
      <!-- 图例 -->

      <p class="mapLegend" style="background-color:#F56C6C" />
      <span style="color:#F56C6C">紧急</span>

      <p class="mapLegend" style="background-color:#1a73e8" />
      <span style="color:#1a73e8">不紧急</span>

      <!-- position: [{{ lng }}, {{ lat }}] address: {{ address }}
        <button type="button" name="button" v-on:click="addMarker">
          add markers
        </button>
        <button type="button" name="button" v-on:click="removeMarker">
          remove markers
        </button>-->
    </div>
  </div>
</template>

  <style>
  .amap-page-container {
    width: 100%;
    height: 500px;
  }
  .mapLegend{
    margin:8px 0 8px 10px;
    display:inline-block;
    vertical-align:middle;
    height:12px;
    width:12px;
    border-radius:6px
  }
  #info-window{
          width: 211px;
          height: 200px;
          margin-left: 30px;
          background:rgba(255,255,255,0.9);
          border-radius: 4px;
          position: relative;
          overflow: hidden;
          .detail{
            width: 100%;
            height: 24px;
            color: #fff;
            background-color: #1a73e8;
            position: absolute;
            bottom: 0;
            font-size: 12px;
            line-height: 24px;
            text-align: center;
            cursor: pointer;
          }
          .window_content{
            width: 100%;
           /*  height: 24px;
            color: #fff;
            background-color: #1a73e8;
            position: absolute;
            bottom: 0;
            font-size: 12px;
            line-height: 24px;
            text-align: center;
            cursor: pointer; */
          }
  }

  </style>

<script>
// NPM 方式
// import { AMapManager } from 'vue-amap'
// import VueAMap from 'vue-amap'
// import AMap from 'AMap'

// const amapManager = new VueAMap.AMapManager()

export default {
  name: 'Mmap',
  props: {
    data_position: {
      type: Array,
      default: () => []
    }
  },
  data: function() {
    // const self = this

    return {
      //* ******************地图和组件初始化设置**********************//

      // amapManager,
      zoom: 12,
      center: [121.59996, 31.197646],
      windows: [],
      window: '',

      address: '',
      markers: [],
      events: {
        init(o) {
          o.getCity((result) => {
            // result 为地图初始化时所在位置的行政区域信息
            console.log(result)
          })
        }

      }

    }
  },

  //* ******************在地图上添加点**********************//
  mounted() {
    this.point()
  },
  methods: {

    // 显示弹窗//
    point() {
      const markers = []
      const windows = []
      const that = this

      console.log('接收到index信息', this.data_position)
      this.data_position.forEach((item, index) => {
        markers.push({
          position: [item.location_longitude, item.location_latitude],

          // icon:item.url, //不设置默认蓝色水滴
          events: {
            mouseover() {
              // 方法：鼠标移动到点标记上，显示相应窗体
              that.windows.forEach(window => {
                window.visible = false // 关闭窗体
              })
              that.window = that.windows[index]
              that.$nextTick(() => {
                that.window.visible = true
              })
            }
          }

        })
        windows.push({
          position: [item.location_longitude, item.location_latitude],
          isCustom: true,
          offset: [115, 55], // 窗体偏移
          showShadow: false,
          visible: false, // 初始是否显示
          // address: item.address,
          content: { 'create_time': item.create_time, 'video_title': item.video_title, 'video_location': item.video_location }
        })
      })
      //  加点
      this.markers = markers
      // 加弹窗
      this.windows = windows

      // 调试
      console.log('markers: ', this.markers)
      console.log('windows: ', this.windows)
    },
    checkDetail(video_path) {
      // alert('点击了查看详情')
      this.$router.push({ path: '/videoload/index',
        query: { file: video_path }})
    }

  }
}
</script>
