<template>
  <div class="hello">
    <h1>Wait-a-Bit order queue management</h1>
    <ul>
      <li>
        <router-link to="panel">Order call display panel</router-link>
      </li>
      <li>
        <router-link to="input">Call input/control</router-link>
      </li>
    </ul>
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
h1, h2 {
  font-size: 10vh;
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 0 10px;
  font-size: 5vh;
}

a {
  color: #42b983;
}
</style>
