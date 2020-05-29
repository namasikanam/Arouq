<template>
  <div class="search-input">
    <b-form @submit.prevent="goSearch">
      <div class="input">
        <b-form-input v-model="query"></b-form-input>
      </div>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "search-input",
  data() {
    return {
      query: ""
    };
  },
  methods: {
    goSearch() {
      this.$emit("newSearch", this.query);
    },
    updateQuery(query) {
      this.query = query
    }
  }
};
</script>

<style lang="scss" scoped>
.search-input {
  form {
    display: flex;
    justify-content: center;

    .input {
      display: flex;
      width: 500px;
      vertical-align: middle;
      border: solid 1px #777;
      height: calc(2.25rem + 7px);
      border-radius: 30px;

      input {
        display: inline-block;
        width: 460px;
        border: none;
        line-height: calc(2.25rem + 7px);
        vertical-align: middle;
        background: none;
        outline: none;
      }

      input.form-control:focus {
        outline: none;
        box-shadow: none;
      }

      .rec {
        display: inline-block;
        width: 24px;
        height: 38px;
        background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAYAAACAa1QyAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAXlJREFUKBW9kr1Kw1AUx5OYVWiRGqqLiPgIios4qg+QobhI7QdYH6CKk4IPUCRNQhFRHPIAnRykIIqre7cMsUMHp0Jt/J2ShiYWxx44/M/53/N17z2qkhLbtgtQl+g62kWvKpXKExiLFlsYzWbzCLgOw7A2HA6XVFU9Ez/i41A9tjAIutA0rVAqld4j/tl13cJoNLrHf5zEJjpBbvq+/zE5FIz8jWkuYXOfMEFETppPd5qV84ebX5Iu82azWd00zR+Zg+fmEdWZd/M8b6Hf7w9kvKDX661Eg3cdx9mK7DFQdBtDPlkhYRUI5J86uq4fgA4d6nR6sCzrOAiCN8MwduDvhAdF9tFX/lJrYNRbrdZiuVz2SDqHs/P5/EBQfOHlXOIkXsVQGMnicI2OZrFY/BZuWiSBtfLo6FPgZLxGmUymxrwNDj65ww3YzuVycleDQof4Ml6bONlFZdxpUpXF3MU+peIeuIx+McELeFutVjvg/5Jeneno+W3ELz3Rmg23qA6NAAAAAElFTkSuQmCC)
          no-repeat center;
      }

      .rec.active {
        background-image: -webkit-image-set(
          url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAASCAMAAAC3taQAAAAAhFBMVEX///8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf8zhf+04UQDAAAAK3RSTlMAAQIDBgwNHR43ODs9PkNEVFZaXGZnlpecqaq31NfZ2t3e3+Dl6On5+/z9BL131wAAAHdJREFUCB0FwYcCgQAUAMBTFGWPaCGb9///5w5s+3e/BdgNy8lq2AH6AsUZ8EuQ/AABAhAgAAECECAgUjGCkH49c9cZZlfTh2ZvcymT8rKxb8xvmXX36day25xjm4GsPSGt7od8nB/uVQoW9Ste9QKAAAABAAL4AzokCI8/h6hiAAAAAElFTkSuQmCC)
            1x,
          url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAkCAMAAACg5NohAAAA8FBMVEUsgf////8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf8sgf+F30pxAAAAT3RSTlMAAAMFBggJCgwNDxARGhscHR4gIyYsLTA3Oj1AQUxNWl1gYWRtb3B+f4KFhoeIio6PlJmbpqeorr6/wMXGyNLT2dve3+bn7e7y9PX2+fv+wE6fLAAAASxJREFUKM/d01dWAkEUBNAqkCBBBETCiKAoSlAElKSgKHGAqf3vxg/oQ9AFeKzPvh/vdPVr0CTy8L5cDsoRbEIYyc0lSZrnDqkgtS/8fqstp7BPEVvF9UlRdmSPHtUyM1qq7ZGUNpTWxwF5DXmlA6Ih/Htayf0bubXCUsckJZcRlwTgSEuMdEZyrJShlMYATjVCV5cka3ox9KwnAFl1UVKdZMzW7VpuZMcA1FVCUpMAyStH7YzPl2nLuQYQmCgJvqpCkvnZem1meQCo6I2gpcU5SZ5UB7Y9qIYBILGQRZANDcPk9l7AyVANEKSvr8/ELiW+1Petiwr1tSgHDQTLC/VDpkNP09G0no263dFsfSo1PTv1Wj1Hmzg962Dn4/edkTTq3MV/fAdun+Nv0TegC0JUU1yQZAAAAABJRU5ErkJggg==)
            2x
        );
      }
    }

    .btn {
      margin-left: 6px;
    }
  }
}
</style>
