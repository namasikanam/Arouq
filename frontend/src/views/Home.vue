<template>
  <div>
    <b-container fluid class="container-main">
      <a class="logo" href="."> ArouQ </a>
      <search-input
        class="input"
        v-on:newSearch="newSearch"
        v-on:newSwitch="newSwitch"
        ref="input"
      ></search-input>
      <b-alert
        class="alert justify-content-center"
        show
        variant="danger"
        v-if="!valid && language === 'en'"
      >
        <h4 class="alert-heading;font-size: 18px">Search Error!</h4>
        <p v-if="language == 'en'">
          For English, only english characters and white space are allowed.
        </p>
      </b-alert>
      <b-alert
        class="alert justify-content-center"
        show
        variant="danger"
        v-if="!valid && language === 'cn'"
      >
        <h4 class="alert-heading;font-size: 18px">搜索错误！</h4>
        <p>
          在中文模式下，只允许输入中文字符和空白字符。
        </p>
      </b-alert>
    </b-container>
  </div>
</template>

<script>
import SearchInput from "@/components/SearchInput.vue";
import axios from "axios";

export default {
  name: "home",
  components: { SearchInput },
  data() {
    let language = 'en'
    console.log(`language in route is ${this.$route.params.language}`)
    if (this.$route.params.language !== undefined && this.$route.params.language === 'cn') {
      language = 'cn'
    }
    console.log(`the language is set to ${language}`)
    history.replaceState(
      {
        language
      },
      '',
      `/?#${this.$route.fullPath}`
    )

    return {
      language: language,
      valid: true
    };
  },
  methods: {
    newSearch(query) {
      this.valid = true
      console.log(`language = ${this.language}`)
      if (this.language === 'en') {
        this.valid = /^[a-zA-Z\s]*$/.test(query);
      }
      else {
        this.valid = /^[\u4e00-\u9fa5\s]+$/.test(query)
      }
      if (this.valid) {
        if (query === "") {
          window.location.assign(`/#/home/${this.language}`);
        } else {
          window.location.assign(`/#/search/${query}/1/${this.language}`);
        }
      }
    },
    newSwitch() {
      if (this.language === 'en') {
        window.location.assign(`/#/home/cn`);
      }
      else {
        window.location.assign(`/#/home/en`);
      }
    },
    updateCompletion(query) {
      this.queryBuffer = query
      axios.get(
        '/api/fill/', {
        params: { 'query': query }
      })
        .then((response) => {
          this.candidates = response.data.candidates
        })
    },
    autoCompletion() {
      if (this.query === this.queryBuffer) return
      this.updateCompletion(this.query)
    }
  },
  mounted() {
    this.$refs.input.updateLanguage(this.language);
  }
};
</script>

<style lang="scss" scoped>
.logo {
  display: block;
  text-align: center;
  font-family: Copperplate;
  font-weight: bolder;
  font-size: 100px;
  color: #6b008d;
  margin-top: 150px;
}

.logo:hover {
  text-decoration: none;
  color: #6b008d;
}

.input {
  text-align: center;
}

.alert {
  margin: auto;
  margin-top: 30px;
  width: 1000px;

  .p {
    font-size: 14px;
  }
}
</style>
