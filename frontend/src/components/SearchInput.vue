<template>
  <div class="search-input">
    <b-form @submit.prevent="goSearch">
      <div class="input">
        <b-form-input
          v-model="query"
          v-on:input="autoCompletion"
          list="auto-completion-list"
        >
        </b-form-input>
        <datalist id="auto-completion-list" autocomplete="on">
          <option v-for="candidate in candidates" v-bind:key="candidate">
            {{ candidate }}
          </option>
        </datalist>

        <!-- failed to copy the glass search logo from Google, perhaps try again later -->
        <!-- <button class="Tg7LZd" jsname="Tg7LZd" aria-label="Google Search" type="submit" data-ved="0ahUKEwj8pfaUheLpAhV0yosBHTJuBAYQ4dUDCAw"> <div class="FAuhyb"> <span class="z1asCe MZy1Rb"><svg focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path></svg></span> </div> </button> -->
        <!-- <div type="submit" class="glass">
          <svg
            focusable="false"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
          >
            <path
              d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
            ></path>
          </svg>
        </div> -->
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
      query: "",
      queryBuffer: '',
      candidates: [],
      lastUpdateTime: 0,
    };
  },
  methods: {
    goSearch() {
      this.$emit("newSearch", this.query);
    },
    doComplete(t) {
      if (this.lastUpdateTime == t) {
        axios.get(
          '/api/fill/', {
          params: { 'query': this.queryBuffer }
        })
          .then((response) => {
            this.candidates = response.data.candidates
            console.log('candidates = ')
            console.log(this.candidates)
          })
      }
    },
    updateCompletion(query) {
      this.queryBuffer = query
      this.lastUpdateTime = Date.now()
      // 1s delay
      window.setTimeout(this.doComplete, 1000, this.lastUpdateTime);
    },
    autoCompletion() {
      if (this.query === this.queryBuffer) return
      this.updateCompletion(this.query)
    },
    updateQuery(query) {
      this.query = query
      this.updateCompletion(query)
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
      width: 1000px;
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

  .glass {
    display: inline-block;
    fill: currentColor;
    height: 24px;
    line-height: 24px;
    position: relative;
    width: 24px;
    background: none;
    color: #4285f4;
    margin: auto;
    background: transparent;
  }
}
</style>
