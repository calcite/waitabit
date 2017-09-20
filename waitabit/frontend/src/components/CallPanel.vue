<template>
  <div class="row main-row">
    <div class="disconnect-warning" v-show="appStatus === 'disconnected'">
      <span class="glyphicon glyphicon-ban-circle" aria-hidden="true"></span>
    </div>
    <transition name="fade">
      <div class="screensaver" v-show="screenSaver"></div>
    </transition>
    <div class="col-lg-9 latest-call" v-on:click="fullscreenToggle">
      <p class="big-number" v-bind:key="callList[0]">{{ (callList.length > 0) ? callList[0] : ''}}</p>
    </div>
    <div class="col-lg-3 previous-calls">
      <transition-group name="previous-call-list" tag="ul"
                          class="previous-call-list">
        <li v-for="item in callList.slice(1)" v-bind:key="item"
            v-bind:style="previousCallItemStyle">{{item}}</li>
      </transition-group>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import VueResource from 'vue-resource'
  import fullscreen from 'vue-fullscreen'
  import SockJS from 'sockjs-client'
  import _ from 'lodash'

  Vue.use(fullscreen)
  Vue.use(VueResource)

  export default {
    name: 'call-panel',
    data () {
      return {
        callList: [],
        callListLen: 4,
        fullscreen: false,
        sock: null,
        appStatus: 'disconnected',
        screenSaver: false,
        screenSaverTimeout: 3600000,
        screenSaverAuto: null,
        dingSound: document.getElementById('ding')
      }
    },
    computed: {
      previousCallItemStyle: function () {
        return {
          'font-size': ((100 / this.callListLen) * 0.611) + 'vh',
          'border-bottom': 'gray solid 1px',
          'padding': ((100 / this.callListLen) * 0.0599) + 'vh'
        }
      }
    },
    methods: {
      fullscreenToggle: function () {
        this.$fullscreen.toggle(document.documentElement, {
          wrap: false,
          callback: this.fullscreenChange
        })
      },
      fullscreenChange: function (fullscreen) {
        this.fullscreen = fullscreen
      },
      sockjsSetup: _.throttle(function () {
        // Connect to notifications
        console.log('SockJS connecting')
        this.sock = new SockJS('/api/notifications/')
        var vm = this
        this.sock.onopen = function (e) {
          console.log('Sockjs open')
          vm.updateQueue()
          vm.updateScreenSaver()
          vm.appStatus = 'connected'
        }
        this.sock.onmessage = function (e) {
          vm.processNotification(e.data)
        }
        this.sock.onclose = function (e) {
          console.log('SockJS closed - reconnecting.')
          vm.appStatus = 'disconnected'
          vm.sockjsSetup()
        }
      }, 10000),
      processNotification: function (sockMsg) {
        var msg = sockMsg
        if ((msg.event === 'new_call') || (msg.event === 'delete')) {
          if (msg.event === 'new_call') {
            this.playDing()

            // Reset the screensaver stuff
            this.screenSaver = false
            clearTimeout(this.screenSaverAuto)
            if (this.screenSaverTimeout > 0) {
              this.screenSaverAuto = setTimeout(this.finishSession.bind(this),
                this.screenSaverTimeout)
            }
          }
          this.callList = msg.queue
        } else if (msg.event === 'screensaver') {
          this.screenSaver = msg.status
          clearTimeout(this.screenSaverAuto)
        }
        console.log(JSON.stringify(msg))
      },
      updateQueue: function () {
        var vm = this
        this.$http.get('api/queue').then((response) => {
          vm.callList = response.body.queue
          vm.callListLen = response.body.length
        }, (response) => {
          console.log(response)
        })
      },
      updateScreenSaver: function () {
        var vm = this
        this.$http.get('api/screensaver').then((response) => {
          vm.screenSaverTimeout = response.body.timeout * 1000
          vm.screenSaver = response.body.status

          if ((vm.screenSaverAuto == null) && (vm.screenSaverTimeout > 0)) {
            vm.screenSaverAuto = setTimeout(vm.finishSession.bind(vm),
              vm.screenSaverTimeout)
          }
          // Doesn't solve situation when the screensaver timeout is updated.
          // Then the last timeout will still finish
        }, (response) => {
          console.log(response)
        })
      },
      playDing: function () {
        if (this.dingSound.paused) {
          this.dingSound.play()
        } else {
          this.dingSound.pause()
          this.dingSound.currentTime = 0
          this.dingSound.play()
        }
      },
      finishSession: function () {
        this.screenSaver = true
      }
    },
    mounted: function () {
      this.sockjsSetup()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .latest-call {
    display: inline-block;
    vertical-align: middle;
    height: 100vh;
  }

  .previous-calls {
    height: 100vh;
    border-left: gray solid 1px;
  }

  .previous-call-list {
    list-style-type: none;
    padding: 0px;
  }

  .previous-call-item {
    font-size: 7.6375vh;
    border-bottom: gray solid 1px;
    padding: 0.7487vh;
  }

  .previous-call-list-enter-active, .previous-call-list-leave-active {
    transition: all 1s;
  }

  .previous-call-list-enter {
    opacity: 0;
    transform: translateX(-30px);
  }

  .previous-call-list-leave-to {
    opacity: 0;
    transform: translateX(30px);
  }
  .previous-call-list-move {
    transition: 0.5s;
  }

  .screensaver {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: black;
    z-index: 99;
    opacity: 0.95;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity 5s;
  }

  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
    transition: opacity 0.5s;
  }

  .disconnect-warning {
    position: absolute;
    top: 0;
    left: 0;
    width: 20vw;
    height: 20vh;
    z-index: 100;
    font-size: 10vh;
    margin-top: 5vh;
    color: red;
  }

  @keyframes new-call {
      0% {color: #42b983;}
      70% {color: #42b983;}
      100% {color: #2c3e50;}
  }

  .big-number {
    font-size: 60vh;
    margin-top: 8vh;
    animation-name: new-call;
    animation-duration: 3s;
  }
</style>
