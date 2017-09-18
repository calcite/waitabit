<template>
  <div class="hello">
    <h1>Wait-a-Bit order queue management</h1>
    <div clas="row">
      <div class="col-md-6">
        <router-link to="panel">
        <div>
        <img src="static/panel_screenshot.png">
        <span class="screen-link">Order call display panel</span>
        </div>
        </router-link>
      </div>
      <div class="col-md-6">
        <router-link to="input">
          <div>
            <img src="static/input_screenshot.png">
            <span class="screen-link">Call input/control</span>
          </div>
        </router-link>
      </div>
    </div>

    <!--<ul>-->
      <!--<li>-->
        <!--<router-link to="panel">-->
          <!--<div class="screen-link">-->
            <!--<img src="static/panel_screenshot.png">-->
            <!--<span>Order call display panel</span>-->
          <!--</div>-->
        <!--</router-link>-->
      <!--</li>-->
      <!--<li>-->
        <!--<router-link to="input">-->
          <!--<div class="screen-link">-->
            <!--<img src="static/input_screenshot.png">-->
            <!--<span>Call input/control</span>-->
          <!--</div>-->
        <!--</router-link>-->
      <!--</li>-->
    <!--</ul>-->
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
/*h1, h2 {*/
  /*font-size: x-large;*/
  /*font-weight: normal;*/
  /*margin-bottom: 10vh;*/
/*}*/

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

  /*.screen-link {*/
    /*width: 50%;*/
    /*float: left;*/
  /*}*/

  /*.screen-link > img {*/
    /*width: 50%;*/
  /*}*/

  .screen-link {
    display: block;
    font-size: large;
    margin-bottom: 5vh;
    margin-top: 1vh;
  }
</style>
