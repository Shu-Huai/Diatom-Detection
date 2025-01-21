//Svsdisplay.vue
<template>
    <div class="svs-container">
      <h2>硅藻数字切片缩略图</h2>
  
      <div class="image-row">
        <button @click="prev('slice')" class="arrow-btn">◀</button>
        <div class="image-display" v-for="(image, index) in currentSlices" :key="index">
            <img :src="getImageUrl(image.image)" :alt="image.description" />

        </div>
        <button @click="next('slice')" class="arrow-btn">▶</button>
      </div>
  
      <h2>硅藻patch示意图</h2>
  
      <div class="image-row">
        <button @click="prev('patch')" class="arrow-btn">◀</button>
        <div class="image-display" v-for="(image, index) in currentPatches" :key="index">
            <img :src="getImageUrl(image.image)" :alt="image.description" />

        </div>
        <button @click="next('patch')" class="arrow-btn">▶</button>
      </div>
    </div>
  </template>
  
  <script>
  import service from "@/utils/request";
  
  export default {
    data() {
      return {
        diatom_slices: [],
        diatom_patches: [],
        currentSliceIndex: 0,
        currentPatchIndex: 0,
      };
    },
    computed: {
      currentSlices() {
        return this.diatom_slices.slice(this.currentSliceIndex, this.currentSliceIndex + 3);
      },
      currentPatches() {
        return this.diatom_patches.slice(this.currentPatchIndex, this.currentPatchIndex + 3);
      },
    },
    methods: {
        async fetchImages() {
        try {
          console.log("Requesting /svsdisplay/images/...");
          const res = await service.get('/svsdisplay/images/');
          console.log("Images loaded successfully:", res); // 不需要使用 res.data
          this.diatom_slices = res.diatom_slices;
          this.diatom_patches = res.diatom_patches;
        } catch (error) {
          console.error("Error fetching images:", error);
          this.$message.error("服务器错误，请稍后重试");
        }
      },
      next(type) {
        if (type === 'slice') {
          if (this.currentSliceIndex + 3 < this.diatom_slices.length) {
            this.currentSliceIndex += 3;
          } else {
            this.$message.warning("已经是最后一组了");
          }
        } else if (type === 'patch') {
          if (this.currentPatchIndex + 3 < this.diatom_patches.length) {
            this.currentPatchIndex += 3;
          } else {
            this.$message.warning("已经是最后一组了");
          }
        }
      },
      prev(type) {
        if (type === "slice") {
          if (this.currentSliceIndex > 0) {
            this.currentSliceIndex -= 3;
          } else {
            this.$message.warning("已经是第一组了");
          }
        } else if (type === "patch") {
          if (this.currentPatchIndex > 0) {
            this.currentPatchIndex -= 3;
          } else {
            this.$message.warning("已经是第一组了");
          }
        }
      },
      // 动态获取完整图片 URL
      getImageUrl(imagePath) {
        return `${this.$http.defaults.baseURL}${imagePath}`;
      },
    },
    created() {
      console.log("Created lifecycle hook triggered");
      this.fetchImages();
    },
  };
  </script>
  
  <style>
  .svs-container {
    text-align: center;
    padding: 20px;
  }
  .image-row {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
  }
  .image-display {
    margin: 0 10px;
  }
  .arrow-btn {
    font-size: 20px;
    cursor: pointer;
  }
  img {
    max-width: 200px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  </style>
  