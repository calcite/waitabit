<template>
  <div class="hello">
    <h1>Wait-a-Bit order queue management</h1>
    <div class="row">
      <div class="link-panel flex-panel">
        <router-link to="panel">
        <div>
        <img src="static/panel_screenshot.png" class="img-responsive">
        <span class="screen-link">Order call display panel</span>
        </div>
        </router-link>
      </div>
      <div class="link-panel flex-panel">
        <router-link to="input">
          <div>
            <img src="static/input_screenshot.png" class="img-responsive">
            <span class="screen-link">Call input/control</span>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'entry',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  h1 {
    margin-bottom: 8vh;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    margin: 0 10px;
    font-size: large;
  }

  a {
    color: #42b983;
  }

  .link-panel {
    display: block;
    margin: 0 auto;
  }

  @media (orientation:landscape) {
    .flex-panel {
      float:left;
      width: 50%;
    }
  }

  @media (orientation:portrait) {
    .flex-panel {
      float:none;
      width: 80%;
    }
  }
  .screen-link {
    display: block;
    font-size: large;
    margin-bottom: 5vh;
    margin-top: 1vh;
  }
</style>
