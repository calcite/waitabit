<template>
  <div class="container-fluid">
    <div id="app">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>

export default {
  name: 'app',
  components: {
  }
}
</script>

<style>

  body {
    overflow: hidden;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

</style>
