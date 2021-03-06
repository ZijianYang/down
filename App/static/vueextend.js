var VueExtend = {
    install: function (Vue, options) {
        // 获取Url参数
        Vue.GetUrlParam = function (name) {
            var paramStr = window.location.search.substr(1);
            var searchParams = new URLSearchParams(paramStr);
            return searchParams.get(name)
        },
            Vue.Timespan = function (dateIn, format) {
                var date = {
                    "M+": dateIn.getMonth() + 1,
                    "d+": dateIn.getDate(),
                    "h+": dateIn.getHours(),
                    "m+": dateIn.getMinutes(),
                    "s+": dateIn.getSeconds(),
                    "q+": Math.floor((dateIn.getMonth() + 3) / 3),
                    "S+": dateIn.getMilliseconds()
                };
                if (/(y+)/i.test(format)) {
                    format = format.replace(RegExp.$1, (dateIn.getFullYear() + '').substr(4 - RegExp.$1.length));
                }
                for (var k in date) {
                    if (new RegExp("(" + k + ")").test(format)) {
                        format = format.replace(RegExp.$1, RegExp.$1.length === 1
                            ? date[k] : ("00" + date[k]).substr(("" + date[k]).length));
                    }
                }
                return format;
            },
            //整理时间格式
            Vue.TimeFormat = function (dataTimeStr) {
                var date = dataTimeStr.split("T")[0].split("-");
                var time = dataTimeStr.split("T")[1].split(":");
                var year = parseInt(date[0]);
                var month = parseInt(date[1]) - 1;
                var day = parseInt(date[2]);
                var hour = parseInt(time[0]);
                var minute = parseInt(time[1]);
                var second = parseInt(time[2]);
                return new Date(year, month, day, hour, minute, second);
            },
            Vue.TimeDiff = function (starDate, endDate) {
                //计算出相差天数
                var dateFiff = endDate - starDate;
                //计算年数
                var years = Math.floor(dateFiff / (12 * 30 * 24 * 3600 * 1000))
                //计算月数
                var leave0 = dateFiff % (12 * 30 * 24 * 3600 * 1000)    //计算年数后剩余的毫秒数    
                var months = Math.floor(leave0 / (30 * 24 * 3600 * 1000))
                //计算天数
                var leave1 = dateFiff % (30 * 24 * 3600 * 1000)    //计算年数后剩余的毫秒数    
                var days = Math.floor(leave1 / (24 * 3600 * 1000))
                //计算出小时数
                var leave2 = dateFiff % (24 * 3600 * 1000)    //计算天数后剩余的毫秒数
                var hours = Math.floor(leave2 / (3600 * 1000))
                //计算相差分钟数
                var leave3 = dateFiff % (3600 * 1000)        //计算小时数后剩余的毫秒数
                var minutes = Math.floor(leave3 / (60 * 1000))
                //计算相差秒数
                var leave4 = dateFiff % (60 * 1000)      //计算分钟数后剩余的毫秒数
                var seconds = Math.round(leave4 / 1000)
                return { year: years, month: months, day: days, hour: hours, minute: minutes, second: seconds };
            },
            Vue.showBase64 = function (value) {
                var array = [];
                array.push('data:image/gif;base64');
                array.push(value);
                var result = array.join();
                return result;
            },
            //整理金额数字格式
            Vue.MoneyFormat = function (str, n) {  //1.字符串，2.小数位数
                if (n === undefined)
                    n = 2;
                n = n >= 0 && n <= 20 ? n : 2;
                str = parseFloat((str + "").replace(/[^\d\.-]/g, "")).toFixed(n) + "";
                var l = str.split(".")[0].split("").reverse(), r = str.split(".")[1];
                t = "";
                for (i = 0; i < l.length; i++) {
                    t += l[i] + ((i + 1) % 3 === 0 && (i + 1) !== l.length ? "," : "");
                }
                if (n === 0 || r === undefined)
                    return t.split("").reverse().join("");
                else
                    return t.split("").reverse().join("") + "." + r
            }
        Vue.Debounce = function (func, threshold, execAsap) {//debounce 接受 3 个参数，后两个可选；第一个是要 debounce 的函数， 第二个代表 debouce 的时间间隔，第三个在时间段的开始还是结束执行函数;
            var timeout;
            return function debounced() {
                var obj = this, args = arguments;
                function delayed() {
                    if (!execAsap)
                        func.apply(obj, args);
                    timeout = null;
                };
                if (timeout)
                    clearTimeout(timeout);
                else if (execAsap)
                    func.apply(obj, args);
                timeout = setTimeout(delayed, threshold || 100);
            };
        },
        /////////////////例子///////////////////////
        // var test = new Vue({
        //     el: "test",
        //     data: {
        //         number: 0,
        //     },
        //     methods: {
        //         show() {
        //             this.number = this.number + 1;
        //             console.log(this.number);
        //         },
        //     },
        //     mounted: function () {
        //         self = this;
        //         $(window).scroll( Vue.Debounce(function () {
        //             self.show()
        //         }, 1000, true));
        //         window.onresize = Vue.Debounce(function () {
        //             self.show()
        //         }, 2000)
               
        //     },
        // });
        Vue.Throttle = function (func, duration) {
            // duration 以秒计
            let last
            return function () {
                let now = Date.now()
                if (last && (now - last) < duration * 1e3)
                    return false;
                last = now;
                func.apply(this, arguments)
            }
        }
    }
}

Vue.use(VueExtend)
Vue.use(Vuex)



// 提示组件
Vue.component('my-prompt', {
    template:
        '<div class="prompt_box"  style="background-color:bisque">' +
            '<span v-if="Total!=0" v-text="Total"></span>' +  
            '<ul>' +    
                '<li v-for="(item,index) in myItems">'+
                    '<span v-text="item" v-on:click="Selected(item)"></span>'+
                '</li>'+
            '</ul>' +          
        '</div>',
    props: {
        myItems: {
            type: Object,
            default: function () {
              return []
            }
        },
    },
    computed: {            
        Total: function () {
            var data = this.myItems.length;
            return data;
        }
    },
    methods: {
        Selected: function (content) {
            this.$emit('selected', content);
        },
    },
});


// 图片显示组件（带遮罩提示）
Vue.component('my-imgshow', {
    template:
        '<div style="float:left;position:relative;cursor:pointer;">'+
            '<img v-bind:src="mySrc"/>'+
            // '<span v-text="mySrc"/>'+
            '<div style="width:100%;height:100%;position:absolute;left:0;top:0;">' +
                '<slot name="tip"></slot>' + 
            '</div>' + 
        '</div>',
    props: {
        mySrc: {
            type: String,
            required: true
        },
    },
});