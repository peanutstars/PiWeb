var psutil = {
    get : function(url, params, callback) {
        var opts = {
            dataType : 'json' ,
            type : 'GET' ,
            async : true ,
            url : url ,
            data : params ,
        } ;
        this.doAjax(opts, callback) ;
    }
    , post : function(url, params, callback) {
        var opts = {
            dataType : 'json' ,
            type : 'POST' ,
            async : true ,
            url : url ,
            data : params ,
        } ;
        this.doAjax(opts, callback) ;
    }
    , patch : function(url, params, callback) {
        var opts = {
            dataType : 'json' ,
            type : 'PATCH' ,
            async : true ,
            url : url ,
            data : params ,
        } ;
        this.doAjax(opts, callback) ;
    }
    , doAjax : function(opts, callback) {
        opts.success = function(response) {
            if (callback) {
                callback(response) ;
            }
        } ,
        opts.error = function(response) {
            console.log('Fail\n' + response) ;
        }
        $.ajax(opts) ;
    }
    , getBookmark : function(callback) {
        this.get('/bookmark', {}, callback) ;
    }
} ;
