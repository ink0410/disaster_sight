<template>
  <div id="scroll-wrap">
    <div
      v-for="item in data"
      :key="item.id"
      class="scroll-content"
      :style="{ top }"
      @mouseenter="Stop"
      @mouseleave="Up"
    >
      <slot name="main" :item="item" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Roll',
  props: {
    data: {
      type: Array,
      default: () => [] // 使用函数返回一个空数组作为默认值
    },
    height: {
      type: Number,
      default: 300 // 设置默认高度为 300
    }
  },
  data() {
    return {
      activeIndex: 0,
      time: null
    }
  },
  computed: {
    top() {
      return `${-this.activeIndex * this.height}px`
      // 单个轮播项的高度 + （上或下）边距 = 滚动高度
    }
  },
  mounted() {
    this.scrollUp()
  },
  methods: {
    scrollUp() {
      if (this.time) this.Stop()
      this.time = setInterval(() => {
        if (this.activeIndex < this.data.length) {
          this.activeIndex += 1
        } else {
          this.activeIndex = 0
        }
      }, 1500)
    },

    Stop() {
      clearInterval(this.time)
    },

    Up() {
      this.scrollUp()
    }
  }
}
</script>

  <style lang="scss" scoped>
  #scroll-wrap {
    height: 100%;
    overflow: hidden;
    .scroll-content {
      position: relative;
      transition: top 0.5s;
    }
  }
  </style>
