<template>
  <div class="row main-row">
    <div class="col-xs-9 latest-call">
      <div class="row">
        <div class="form-group">
          <input  class="form-control big-input" readonly v-model="strBuf"
                  v-on:click="fullscreenToggle">
        </div>
      </div>
      <div class="row keypad">
        <div class="row key-row">
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(1)">1</button>
          </div>
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(2)">2</button>
          </div>
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(3)">3</button>
          </div>
          <div class="col-xs-3">
            <button class="btn big-btn btn-bcsp" v-on:click="delPress">
              <span class="glyphicon glyphicon-step-backward"
                    aria-hidden="true"></span>
            </button>
          </div>
        </div>
        <div class="row key-row">
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(4)">4</button>
          </div>
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(5)">5</button>
          </div>
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(6)">6</button>
          </div>
          <div class="col-xs-3">
            <v-touch tag="button" v-on:press="hidePanel"
                     class="btn big-btn btn-off">
              <span class="glyphicon glyphicon-eye-close"
                    aria-hidden="true"></span>
            </v-touch>
          </div>
        </div>
        <div class="row key-row">
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(7)">7</button>
          </div>
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(8)">8</button>
          </div>
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(9)">9</button>
          </div>
          <div class="col-xs-3">
            <v-touch tag="button" v-on:press="clearAll"
                     class="btn big-btn btn-clr">
              <span class="glyphicon glyphicon-remove"
                    aria-hidden="true"></span>
            </v-touch>
          </div>
        </div>
        <div class="row key-row">
          <div class="col-xs-3">
            <v-touch tag="button" v-on:press="pageReload"
                     v-bind:class="['btn', 'big-btn', 'btn-status', statusClass]">
              <span class="glyphicon glyphicon-signal"
                    aria-hidden="true"></span>
            </v-touch>
          </div>
          <div class="col-xs-3">
            <button class="btn big-btn" v-on:click="numPress(0)">0</button>
          </div>
          <div class="col-xs-6">
            <button class="btn big-btn btn-snd"
                    v-on:click="sendCall" :disabled="sendAvailable">
              <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="col-xs-3 previous-calls">
      <div class="previous-calls-panel">
        <transition-group name="previous-call-list" tag="ul"
                          class="previous-call-list">
          <v-touch tag="li" class="previous-call-item"
              v-for="item in callList" v-bind:key="item"
                   v-on:swiperight="onCallClick(item)">{{item}}</v-touch>
        </transition-group>
      </div>
      <transition name="fade">
        <div class="screensaver" v-show="screenSaver"></div>
      </transition>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import VueTouch from 'vue-touch'
  import fullscreen from 'vue-fullscreen'
  import VueResource from 'vue-resource'
  import SockJS from 'sockjs-client'
  import _ from 'lodash'

  Vue.use(VueTouch, {name: 'v-touch'})
  Vue.use(fullscreen)
  Vue.use(VueResource)

  export default {
    name: 'call-input',
    data () {
      return {
        strBuf: '',
        callList: [],
        fullscreen: false,
        sock: null,
        appStatus: 'disconnected',
        screenSaver: false,
        clickSound: null,
        heartBeatInterval: 3000,
        heartBeatTimer: null,
        maxDigits: 3
      }
    },
    computed: {
      sendAvailable: function () {
        if (!(this.strBuf === '') &&
          (this.callList.indexOf(parseInt(this.strBuf)) === -1)) {
          return false
        } else {
          return true
        }
      },
      statusClass: function () {
        return {
          'btn-connected': this.appStatus === 'connected',
          'btn-disconnected': this.appStatus === 'disconnected'
        }
      }
    },
    methods: {
      numPress: function (value) {
        this.playClick()
        if (this.strBuf.length < this.maxDigits) {
          this.strBuf += value
        }
      },
      delPress: function () {
        this.playClick()
        this.strBuf = this.strBuf.slice(0, -1)
      },
      sendCall: function () {
        this.playClick()
        var vm = this
        var call = parseInt(this.strBuf)
        this.$http.post('api/queue', {'call': call}).then((response) => {
          // Pass for now
          vm.strBuf = ''
        }, (response) => {
          console.log(response)
        })
      },
      clearAll: function () {
        this.playClick()
        this.$http.delete('api/queue', {'body': {'del': 'all'}}).then(
          (response) => {
            // Pass for now
          }, (response) => {
          console.log(response)
        })
        this.callList.splice(0, this.callList.length)
      },
      onCallClick: function (callId) {
        var index = this.callList.indexOf(callId)

        if (index > -1) {
          this.$http.delete('api/queue', {'body': {'del': callId}}).then(
            (response) => {
              // Pass for now
            }, (response) => {
            console.log(response)
          })
//          this.callList.splice(index, 1)
        }
      },
      hidePanel: function () {
        this.playClick()
        this.$http.post('api/screensaver').then((response) => {
          // Pass for now
        }, (response) => {
          console.log(response)
        })
      },
      fullscreenToggle: function () {
        this.$fullscreen.toggle(document.documentElement, {
          wrap: false,
          callback: this.fullscreenChange
        })
      },
      fullscreenChange: function (fullscreen) {
        this.fullscreen = fullscreen
      },
      pageReload: function () {
        this.playClick()
        console.log('reloading')
        location.reload()
      },
      sockjsSetup: _.throttle(function () {
        // Connect to notifications
        console.log('SockJS connecting')
        this.sock = new SockJS('/api/notifications/')
        var vm = this
        this.sock.onopen = function (e) {
          console.log('Sockjs open')
          vm.updateQueue()
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

        // In any case reset the heartbeat timeout
        clearTimeout(this.heartBeatTimer)
        this.heartBeatTimer = setTimeout(this.restartConnection.bind(this),
          this.heartBeatInterval * 3)

        if ((msg.event === 'new_call') || (msg.event === 'delete')) {
          this.callList = msg.queue
        } else if (msg.event === 'screensaver') {
          this.screenSaver = msg.status
        }
        console.log(JSON.stringify(msg))
      },
      updateQueue: function () {
        var vm = this
        this.$http.get('api/queue').then((response) => {
          vm.callList = response.body.queue
          vm.heartBeatInterval = response.body.heartbeat_interval * 1000
          vm.maxDigits = response.body.max_digits
        }, (response) => {
          console.log(response)
        })
      },
      updateScreenSaver: function () {
        var vm = this
        this.$http.get('api/screensaver').then((response) => {
          vm.screenSaver = response.body.status
        }, (response) => {
          console.log(response)
        })
      },
      playClick: function () {
        navigator.vibrate(50)
        if (this.clickSound.paused) {
          this.clickSound.play()
        } else {
          this.clickSound.pause()
          this.clickSound.currentTime = 0
          this.clickSound.play()
        }
      },
      restartConnection: function () {
        console.log('No heart beat detected, restarting connection.')
        this.appStatus = 'disconnected'
        this.sockjsSetup()
      }
    },
    mounted: function () {
      this.clickSound = document.getElementById('click')
      this.sockjsSetup()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .big-input {
    font-size: 10vh;
    height: 18vh;
    width: 70vw;
    margin: 3vh 2vw 0 2.5vw;
    direction: rtl;
  }

  .big-btn {
    height: 16vh;
    width: 100%;
    font-size: 10vh;
    font-weight: 600;
    margin: 1vh 1vw 1vh 1vw;
    background-color: #b6d4ff;
    border-radius: 10px;
  }

  .btn-snd {
    background-color: limegreen;
    color: white;
  }

  .btn-clr {
    background-color: crimson;
    color: white;
  }

  .btn-bcsp {
    background-color: orangered;
    color: white;
  }

  .btn-off {
    background-color: lightgray;
  }

  .btn-status {
    font-size: 8vh;
    font-weight: 300;
    padding-bottom: 0;
    border-radius: 50px;
  }

  .btn-connected {
    background-color: #33e207;
  }

  .btn-disconnected {
    background-color: red;
  }

  .btn-snd-extra {
    background-color: limegreen;
    padding-bottom: -10px;
  }

  .keypad {
    margin: 0vh 2vw 0 0;
  }
  .latest-call {
    display: inline-block;
    vertical-align: middle;
    height: 100vh;
  }


  .previous-calls {
    height: 100vh;
    border-left: gray solid 1px;
  }

  .previous-calls-panel {
    height: 100vh;
    overflow-y: scroll;
  }

  .previous-call-list {
    list-style-type: none;
    padding: 0px;
    margin-top: 3vh;
  }

  .previous-call-item {
    font-size: 8vh;
    border:  solid 1px;
    padding: 5px;
    margin: 10px;
    border-radius: 10px;
    background: white;

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
    position: relative;
    margin-top: -100vh;
    margin-right: -15px;
    margin-left: -15px;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: black;
    z-index: 99;
    opacity: 0.5;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity 5s;
  }

  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
    transition: opacity 0.5s;
  }
</style>
