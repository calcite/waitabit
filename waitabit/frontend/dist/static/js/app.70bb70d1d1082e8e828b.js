webpackJsonp([1],{0:function(t,s){},"12SR":function(t,s){},"1XP8":function(t,s,n){"use strict";var e=function(){var t=this,s=t.$createElement,n=t._self._c||s;return n("div",{staticClass:"container-fluid"},[n("div",{attrs:{id:"app"}},[n("router-view")],1)])},i=[],a={render:e,staticRenderFns:i};s.a=a},HYcW:function(t,s){},LNOo:function(t,s,n){"use strict";var e=n("mvHQ"),i=n.n(e),a=n("7+uW"),c=n("I0MY"),o=n.n(c),l=n("88le"),u=n.n(l),r=n("ORbq"),d=n("O3w4"),v=n.n(d),p=n("M4fF"),h=n.n(p);a.a.use(o.a,{name:"v-touch"}),a.a.use(u.a),a.a.use(r.a),s.a={name:"call-input",data:function(){return{msg:"Welcome to Your Vue.js App",strBuf:"",callList:[],fullscreen:!1,sock:null,appStatus:"disconnected",screenSaver:!1,clickSound:null}},computed:{sendAvailable:function(){return""===this.strBuf||-1!==this.callList.indexOf(parseInt(this.strBuf))},statusClass:function(){return{"btn-connected":"connected"===this.appStatus,"btn-disconnected":"disconnected"===this.appStatus}}},methods:{numPress:function(t){this.playClick(),this.strBuf+=t},delPress:function(){this.playClick(),this.strBuf=this.strBuf.slice(0,-1)},sendCall:function(){this.playClick();var t=this,s=parseInt(this.strBuf);this.$http.post("api/queue",{call:s}).then(function(s){t.strBuf=""},function(t){console.log(t)})},clearAll:function(){this.playClick(),this.$http.delete("api/queue",{body:{del:"all"}}).then(function(t){},function(t){console.log(t)}),this.callList.splice(0,this.callList.length)},onCallClick:function(t){this.callList.indexOf(t)>-1&&this.$http.delete("api/queue",{body:{del:t}}).then(function(t){},function(t){console.log(t)})},hidePanel:function(){this.playClick(),this.$http.post("api/screensaver").then(function(t){},function(t){console.log(t)})},fullscreenToggle:function(){this.$fullscreen.toggle(document.documentElement,{wrap:!1,callback:this.fullscreenChange})},fullscreenChange:function(t){this.fullscreen=t},pageReload:function(){this.playClick(),console.log("reloading"),location.reload()},sockjsSetup:h.a.throttle(function(){console.log("SockJS connecting"),this.sock=new v.a("/api/notifications/");var t=this;this.sock.onopen=function(s){console.log("Sockjs open"),t.updateQueue(),t.appStatus="connected"},this.sock.onmessage=function(s){t.processNotification(s.data)},this.sock.onclose=function(s){console.log("SockJS closed - reconnecting."),t.appStatus="disconnected",t.sockjsSetup()}},1e4),processNotification:function(t){var s=t;"new_call"===s.event||"delete"===s.event?this.callList=s.queue:"screensaver"===s.event&&(this.screenSaver=s.status),console.log(i()(s))},updateQueue:function(){var t=this;this.$http.get("api/queue").then(function(s){t.callList=s.body.queue},function(t){console.log(t)})},updateScreenSaver:function(){var t=this;this.$http.get("api/screensaver").then(function(s){t.screenSaver=s.body.status},function(t){console.log(t)})},playClick:function(){navigator.vibrate(50),this.clickSound.paused?this.clickSound.play():(this.clickSound.pause(),this.clickSound.currentTime=0,this.clickSound.play())}},mounted:function(){this.clickSound=document.getElementById("click"),this.sockjsSetup()}}},M93x:function(t,s,n){"use strict";function e(t){n("UcJI")}var i=n("xJD8"),a=n("1XP8"),c=n("VU/8"),o=e,l=c(i.a,a.a,o,null,null);s.a=l.exports},NHnr:function(t,s,n){"use strict";Object.defineProperty(s,"__esModule",{value:!0});var e=n("7+uW"),i=n("M93x"),a=n("/ocq"),c=n("gNGx"),o=(n.n(c),n("qb6w")),l=(n.n(o),n("qHMK")),u=n("xKpg"),r=n("NWEg");e.a.config.productionTip=!1,e.a.use(a.a);var d=new a.a({routes:[{path:"/",name:"entry",component:r.a},{path:"/panel",name:"call-panel",component:l.a},{path:"/input",name:"call-input",component:u.a}]});new e.a({el:"#app",router:d,render:function(t){return t(i.a)}})},NWEg:function(t,s,n){"use strict";function e(t){n("HYcW")}var i=n("l/hx"),a=n("S1gE"),c=n("VU/8"),o=e,l=c(i.a,a.a,o,"data-v-334659a3",null);s.a=l.exports},NnUl:function(t,s,n){"use strict";var e=function(){var t=this,s=t.$createElement,n=t._self._c||s;return n("div",{staticClass:"row main-row"},[n("div",{staticClass:"col-xs-9 latest-call"},[n("div",{staticClass:"row"},[n("div",{staticClass:"form-group"},[n("input",{directives:[{name:"model",rawName:"v-model",value:t.strBuf,expression:"strBuf"}],staticClass:"form-control big-input",attrs:{readonly:""},domProps:{value:t.strBuf},on:{click:t.fullscreenToggle,input:function(s){s.target.composing||(t.strBuf=s.target.value)}}})])]),t._v(" "),n("div",{staticClass:"row keypad"},[n("div",{staticClass:"row key-row"},[n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(1)}}},[t._v("1")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(2)}}},[t._v("2")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(3)}}},[t._v("3")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn btn-bcsp",on:{click:t.delPress}},[n("span",{staticClass:"glyphicon glyphicon-step-backward",attrs:{"aria-hidden":"true"}})])])]),t._v(" "),n("div",{staticClass:"row key-row"},[n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(4)}}},[t._v("4")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(5)}}},[t._v("5")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(6)}}},[t._v("6")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("v-touch",{staticClass:"btn big-btn btn-off",attrs:{tag:"button"},on:{press:t.hidePanel}},[n("span",{staticClass:"glyphicon glyphicon-eye-close",attrs:{"aria-hidden":"true"}})])],1)]),t._v(" "),n("div",{staticClass:"row key-row"},[n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(7)}}},[t._v("7")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(8)}}},[t._v("8")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(9)}}},[t._v("9")])]),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("v-touch",{staticClass:"btn big-btn btn-clr",attrs:{tag:"button"},on:{press:t.clearAll}},[n("span",{staticClass:"glyphicon glyphicon-remove",attrs:{"aria-hidden":"true"}})])],1)]),t._v(" "),n("div",{staticClass:"row key-row"},[n("div",{staticClass:"col-xs-3"},[n("v-touch",{class:["btn","big-btn","btn-status",t.statusClass],attrs:{tag:"button"},on:{press:t.pageReload}},[n("span",{staticClass:"glyphicon glyphicon-signal",attrs:{"aria-hidden":"true"}})])],1),t._v(" "),n("div",{staticClass:"col-xs-3"},[n("button",{staticClass:"btn big-btn",on:{click:function(s){t.numPress(0)}}},[t._v("0")])]),t._v(" "),n("div",{staticClass:"col-xs-6"},[n("button",{staticClass:"btn big-btn btn-snd",attrs:{disabled:t.sendAvailable},on:{click:t.sendCall}},[n("span",{staticClass:"glyphicon glyphicon-ok",attrs:{"aria-hidden":"true"}})])])])])]),t._v(" "),n("div",{staticClass:"col-xs-3 previous-calls"},[n("div",{staticClass:"previous-calls-panel"},[n("transition-group",{staticClass:"previous-call-list",attrs:{name:"previous-call-list",tag:"ul"}},t._l(t.callList,function(s){return n("v-touch",{key:s,staticClass:"previous-call-item",attrs:{tag:"li"},on:{swiperight:function(n){t.onCallClick(s)}}},[t._v(t._s(s))])}))],1),t._v(" "),n("transition",{attrs:{name:"fade"}},[n("div",{directives:[{name:"show",rawName:"v-show",value:t.screenSaver,expression:"screenSaver"}],staticClass:"screensaver"})])],1)])},i=[],a={render:e,staticRenderFns:i};s.a=a},Pmlb:function(t,s,n){"use strict";var e=function(){var t=this,s=t.$createElement,n=t._self._c||s;return n("div",{staticClass:"row main-row"},[n("div",{directives:[{name:"show",rawName:"v-show",value:"disconnected"===t.appStatus,expression:"appStatus === 'disconnected'"}],staticClass:"disconnect-warning"},[n("span",{staticClass:"glyphicon glyphicon-ban-circle",attrs:{"aria-hidden":"true"}})]),t._v(" "),n("transition",{attrs:{name:"fade"}},[n("div",{directives:[{name:"show",rawName:"v-show",value:t.screenSaver,expression:"screenSaver"}],staticClass:"screensaver"})]),t._v(" "),n("div",{staticClass:"col-lg-9 latest-call",on:{click:t.fullscreenToggle}},[n("p",{staticClass:"big-number"},[t._v(t._s(t.callList.length>0?t.callList[0]:""))])]),t._v(" "),n("div",{staticClass:"col-lg-3 previous-calls"},[n("transition-group",{staticClass:"previous-call-list",attrs:{name:"previous-call-list",tag:"ul"}},t._l(t.callList.slice(1),function(s){return n("li",{key:s,style:t.previousCallItemStyle},[t._v(t._s(s))])}))],1)],1)},i=[],a={render:e,staticRenderFns:i};s.a=a},S1gE:function(t,s,n){"use strict";var e=function(){var t=this,s=t.$createElement,n=t._self._c||s;return n("div",{staticClass:"hello"},[n("h1",[t._v("Wait-a-Bit order queue management")]),t._v(" "),n("div",{attrs:{clas:"row"}},[n("div",{staticClass:"col-md-6"},[n("router-link",{attrs:{to:"panel"}},[n("div",[n("img",{attrs:{src:"static/panel_screenshot.png"}}),t._v(" "),n("span",{staticClass:"screen-link"},[t._v("Order call display panel")])])])],1),t._v(" "),n("div",{staticClass:"col-md-6"},[n("router-link",{attrs:{to:"input"}},[n("div",[n("img",{attrs:{src:"static/input_screenshot.png"}}),t._v(" "),n("span",{staticClass:"screen-link"},[t._v("Call input/control")])])])],1)])])},i=[],a={render:e,staticRenderFns:i};s.a=a},UcJI:function(t,s){},Yjln:function(t,s,n){"use strict";var e=n("mvHQ"),i=n.n(e),a=n("7+uW"),c=n("ORbq"),o=n("88le"),l=n.n(o),u=n("O3w4"),r=n.n(u),d=n("M4fF"),v=n.n(d);a.a.use(l.a),a.a.use(c.a),s.a={name:"call-panel",data:function(){return{callList:[],callListLen:4,fullscreen:!1,sock:null,appStatus:"disconnected",screenSaver:!1,screenSaverTimeout:36e5,screenSaverAuto:null,dingSound:document.getElementById("ding")}},computed:{previousCallItemStyle:function(){return{"font-size":100/this.callListLen*.611+"vh","border-bottom":"gray solid 1px",padding:100/this.callListLen*.0599+"vh"}}},methods:{fullscreenToggle:function(){this.$fullscreen.toggle(document.documentElement,{wrap:!1,callback:this.fullscreenChange})},fullscreenChange:function(t){this.fullscreen=t},sockjsSetup:v.a.throttle(function(){console.log("SockJS connecting"),this.sock=new r.a("/api/notifications/");var t=this;this.sock.onopen=function(s){console.log("Sockjs open"),t.updateQueue(),t.updateScreenSaver(),t.appStatus="connected"},this.sock.onmessage=function(s){t.processNotification(s.data)},this.sock.onclose=function(s){console.log("SockJS closed - reconnecting."),t.appStatus="disconnected",t.sockjsSetup()}},1e4),processNotification:function(t){var s=t;"new_call"===s.event||"delete"===s.event?("new_call"===s.event&&(this.playDing(),this.screenSaver=!1,clearTimeout(this.screenSaverAuto),this.screenSaverTimeout>0&&(this.screenSaverAuto=setTimeout(this.finishSession.bind(this),this.screenSaverTimeout))),this.callList=s.queue):"screensaver"===s.event&&(this.screenSaver=s.status,clearTimeout(this.screenSaverAuto)),console.log(i()(s))},updateQueue:function(){var t=this;this.$http.get("api/queue").then(function(s){t.callList=s.body.queue,t.callListLen=s.body.length},function(t){console.log(t)})},updateScreenSaver:function(){var t=this;this.$http.get("api/screensaver").then(function(s){t.screenSaverTimeout=1e3*s.body.timeout,t.screenSaver=s.body.status,null==t.screenSaverAuto&&t.screenSaverTimeout>0&&(t.screenSaverAuto=setTimeout(t.finishSession.bind(t),t.screenSaverTimeout))},function(t){console.log(t)})},playDing:function(){this.dingSound.paused?this.dingSound.play():(this.dingSound.pause(),this.dingSound.currentTime=0,this.dingSound.play())},finishSession:function(){this.screenSaver=!0}},mounted:function(){this.sockjsSetup()}}},"l/hx":function(t,s,n){"use strict";s.a={name:"entry",data:function(){return{msg:"Welcome to Your Vue.js App"}}}},pJs1:function(t,s){},qHMK:function(t,s,n){"use strict";function e(t){n("12SR")}var i=n("Yjln"),a=n("Pmlb"),c=n("VU/8"),o=e,l=c(i.a,a.a,o,"data-v-c33d8612",null);s.a=l.exports},qb6w:function(t,s){},xJD8:function(t,s,n){"use strict";s.a={name:"app",components:{}}},xKpg:function(t,s,n){"use strict";function e(t){n("pJs1")}var i=n("LNOo"),a=n("NnUl"),c=n("VU/8"),o=e,l=c(i.a,a.a,o,"data-v-5c7c37bd",null);s.a=l.exports}},["NHnr"]);
//# sourceMappingURL=app.70bb70d1d1082e8e828b.js.map