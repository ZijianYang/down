//request处理
axios.defaults.baseURL = config.baseUrl;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

// http request 拦截器
axios.interceptors.request.use(
    request => {
        // var append = {
        //     clientType: 2,
        //     token: store.state.token,
        //     get timespan() {
        //         if (request.method === "post") {
        //             var dateInt = new Date(parseInt(Date.parse(new Date()) + store.state.diffTime));
        //             return Vue.Timespan(dateInt, 'yyyy-MM-dd h:m:s');
        //         }
        //     },
        // };
        // //不是申请token情况时在token不存在时使用停止调用
        // if (request.url != request.baseURL + "/" + webconfig.apiUrls.tokenApplyAndTime) {
        //     //取消请求令牌,每个请求用单独令牌，防止互相影响
        //     var CancelToken = axios.CancelToken;
        //     var source = CancelToken.source();
        //     request.cancelToken = source.token;
        //     if (append.token == '')//token不存在时处理
        //         source.cancel(webconfig.errorMessage.noTokenChanncelRequest);
        // }
        var append={};
        if (request.method === "get") {
            if (request.params === undefined)
                request.params = {};
            request.params = Object.assign(request.params, append);
        } else if (request.method === "post") {
            if (request.data === undefined)
                request.data = {};
            request.data = Object.assign(request.data, append);
            //重新序列化
            var paramsHandle = new URLSearchParams();
            for (var item in request.data) {
                if (request.data.hasOwnProperty(item))
                    paramsHandle.append(item, request.data[item]);
            }
            request.data = paramsHandle;
        }
        return request;
    },
    err => {
        return Promise.reject(err);
    });


// http response 拦截器
axios.interceptors.response.use(
    response => {
        config.log(response);
        return response;
    },
    error => {
        if (error.response) {
            config.log(response);
            switch (error.response.status) {//处理有响应的错误
                case 401:
                    break;
                default:
                    break;
            }
        }
        else {
            config.log(error);
        }
        return Promise.reject(error)   // 返回接口返回的错误信息
    });

var API={};

API.image={
    gets:function(successfunc,pagenumber,paramesdata){
        axios.get(config.apiurls.images + pagenumber, paramesdata)
        .then((response) => {       
            response.data.score=paramesdata.params.score;
            response.data.tag=paramesdata.params.tag;    
            successfunc(response.data);         
        })
    },
    get:function(successfunc, id){
        axios.get(config.apiurls.image + id)
        .then((response) => {
            successfunc(response.data);
        })
    }
};