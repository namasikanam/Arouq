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
    }

    .btn {
      margin-left: 6px;
    }
  }
}
</style>
