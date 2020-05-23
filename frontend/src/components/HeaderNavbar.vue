<template>
  <header class="header-nav"></header>
</template>

<script>
export default {
  name: 'header-navbar'
}
</script>

<style lang="scss">
.head {
  .logo {
    font-family: Copperplate;
    font-size: 24px;
    vertical-align: middle;
    font-weight: bolder;
    color: #6b008d;
    margin-right: 10px;
  }

  .search-input {
    display: inline-block;
  }

  .logo:hover {
    text-decoration: none;
  }
}

.container-main {
  padding: 20px 50px;
  margin-bottom: 20px;
}

a {
  color: #0075f2;
}

body {
  min-width: 780px;
}
</style>
