<template>
  <div>
    <b-container fluid class="container-main">
      <a class="logo" href="."> ArouQ </a>
      <search-input class="input" v-on:newSearch="newSearch"></search-input>
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
    return {};
  },
  methods: {
    newSearch(query) {
      window.location.assign(`/#/search/${query}/1`);
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

.advanced {
  width: 100%;
  text-align: center;
  margin-top: 20px;
  font-size: 16px;

  a:hover {
    text-decoration: none;
  }
}
</style>
