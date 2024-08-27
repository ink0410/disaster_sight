<template>
  <div id="map" style="width: 100%; height: 500px;" />
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'MapView',
  mounted() {
    this.initMap()
  },
  methods: {
    initMap() {
      // 初始化地图
      const map = L.map('map').setView([51.505, -0.09], 13)

      // 添加一个 tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
      }).addTo(map)

      // 添加一个 marker
      L.marker([51.505, -0.09]).addTo(map)
        .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
        .openPopup()
    }
  }
}
</script>

<style scoped>
#map {
  width: 100%;
  height: 100vh;
}
</style>
