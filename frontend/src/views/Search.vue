<template>
  <div>
    <header-navbar></header-navbar>
    <b-navbar fixed="top" sticky class="head bg-white shadow-sm">
      <a class="logo" href=".">ArouQ</a>
      <search-input
        class="search-input"
        v-on:newSearch="newSearch"
        ref="input"
        style="padding-left: 30px"
      ></search-input>
    </b-navbar>
    <b-container fluid class="container-main">
      <div class="search-output">
        <div class="total" v-if="total > 0">
          {{ total.toLocaleString() }} results found.
        </div>
        <div class="no-result" v-if="total === 0 && !init">
          <!-- Maybe something wrong happens. -->
          No matched document.
        </div>
        <b-card class="answer" v-bind:name="answer" v-if="answer !== ''">
        </b-card>
        <div class="document" v-for="item in documents" :key="item.index">
          <div class="url">{{ item.url }}</div>
          <a
            class="name"
            v-html="item.name"
            v-bind:href="item.url"
            target="_blank"
          ></a>
          <div class="article" v-html="item.article"></div>
        </div>
        <div class="pagination" v-if="total > 0">
          <b-pagination
            size="md"
            :total-rows="total"
            v-model="page"
            v-on:change="changePage"
            :per-page="10"
            v-bind:limit="10"
            hide-ellipsis
            hide-goto-end-buttons
          >
          </b-pagination>
        </div>
      </div>
    </b-container>
  </div>
</template>

<script>
import HeaderNavbar from "@/components/HeaderNavbar.vue";
import SearchInput from "@/components/SearchInput.vue";
import axios from "axios";
import randomstring from "randomstring";

export default {
  name: "search",
  components: { HeaderNavbar, SearchInput },
  data() {
    let query = ''
    if (this.$route.params.query !== undefined) {
      query = this.$route.params.query
    }
    let page = 1
    if (this.$route.params.page !== undefined) {
      page = parseInt(this.$route.params.page)
    }
    history.replaceState(
      {
        query,
        page
      },
      '',
      `/?#${this.$route.fullPath}`
    )
    return {
      query: query,
      page: page,
      total: 0,
      documents: [],
      answer: "",
      init: false
    };
  },
  methods: {
    async getResults() {
      let response;
      this.$refs.input.updateQuery(this.query);
      response = await axios.get("/api/", {
        params: { query: this.query, page: this.page }
      });

      // The following is just for test
      //   let random_documents = [];
      //   let random_total = Math.floor(Math.random() * 100);
      //   for (let i = 0; i < Math.min(random_total, 10); ++i) {
      //     let random_content = [];
      //     for (let j = Math.floor(Math.random() * 10) + 10; j--;)
      //       random_content.push(randomstring.generate(10) + ' ');
      //     let random_doc = {
      //       name: randomstring.generate(10),
      //       article: random_content,
      //       url: randomstring.generate(3) + "." + randomstring.generate(5) + "." + randomstring.generate(3)
      //     }
      //     random_documents.push(random_doc);
      //   }
      //   response = {
      //     data: {
      //       total: random_total,
      //       documents: random_documents,
      //       answer: randomstring.generate()
      //     }
      //   };

      if (response.data === null) {
        response.data = {
          total: 0,
          documents: [],
          answer: ''
        };
      }
      console.log(response);

      let documents = [];
      this.total = response.data.total;
      this.answer = response.data.answer;
      for (let i = 0; i < response.data.documents.length; ++i) {
        let doc = response.data.documents[i]
        if (doc.name !== "") {
          documents.push(doc);
        }
        else {
          console.log("ERROR: receive a document without name!");
        }
      }
      this.documents = documents;
      this.init = false;
      window.scrollTo(0, 0);
    },
    newSearch(query) {
      if (query === "") {
        window.location.assign("/#/");
      } else {
        window.location.assign(`/#/search/${query}/1`);
      }
    },
    changePage(page) {
      window.location.assign(
        `/#/search/${this.query}/${page}`
      );
    }
  },
  mounted() {
    this.getResults();
  },
  beforeRouteUpdate(to, from, next) {
    this.query = to.params.query;
    this.page = parseInt(to.params.page);
    this.getResults();
    next();
  }
};
</script>

<style lang="scss">
.search-output {
  width: 800px;

  .total,
  .conditions {
    font-size: 14px;
    margin-top: 10px;
    color: #777;
    max-width: 800px;
  }

  .no-result {
    margin-top: 10px;
  }

  .correct {
    margin-top: 5px;

    span,
    a {
      font-weight: bold;
    }
  }

  .suggestion {
    a {
      font-weight: bold;
    }
  }

  .answer {
    margin-top: 20px;
  }

  .document {
    margin-top: 20px;

    .name {
      font-size: 18px;

      .highlight {
        color: #c00;
      }
    }

    .url {
      max-width: 100%;
      font-size: 12px;
    }

    .article {
      font-size: 14px;
      max-width: 800px;
      overflow-wrap: break-word;

      .highlight {
        font-weight: bold;
        color: #c00;
      }
    }
  }

  .pagination {
    margin-top: 25px;
    width: 100%;

    .b-pagination {
      width: auto;
      margin: 0 auto;
    }
  }
}
</style>
