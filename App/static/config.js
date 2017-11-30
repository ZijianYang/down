//保存集中配置
var config = {
    isTest: true,//是否是测试
    pageSize: 10,//默认页面数据量
    baseUrl: 'http://127.0.0.1:5000/api',//接口地址
    apiurls: {
        images: '/images/',//
        image: '/image/',//
        tag: '/tag/',//
    },
    urls: {
        images: '/',//首页地址
        image:'/detail',//详情地址
    },
    errorMessage: {
        error: "error",
    },
    url: function (url) {
        return this.baseUrl + url;
    },
    log: function (message,isobject=true) {//测试条件下打印信息
        if (this.isTest) {
            if (typeof message=="string"||isobject)
                console.log(message);
            else
                console.log(JSON.stringify(message));
        }
    },
}