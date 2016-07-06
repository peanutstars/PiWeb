var zhub = {
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
    , getSensor : function(uid, callback) {
        this.get('/sensor', {uid:uid}, callback) ;
    }
    , setSensorName : function(uid, name, callback) {
        // XXX : In PATCH mode, I don't know how to get data. Anyway I used to append URI.
        this.patch('/sensor/'+uid+'/'+name, {name:name}, callback) ;
    }
    , getNotify : function(uid, callback) {
        this.get('/sensor/notify/'+uid, {}, callback) ;
    }
    , getStringTime : function(strDotTime) {
        if (strDotTime && strDotTime.length > 0) {
            var arr = strDotTime.split('.') ;
            return arr.slice(0,3).join('-') + ' ' + arr.slice(3,6).join(':') ;
        }
        return '-' ;
    }
    , getAttributeValue : function(attribute) {
        if (attribute.precise == 0) {
            return parseInt(attribute.value) ;
        } else if (attribute.precise > 0) {
            return parseInt(attribute.value) * attribute.precise ;
        } else {
            return parseInt(attribute.value) / (10 * attribute.precise * -1) ;
        }
    }
    , getInputFiltering : function(msg) {
        return msg.replace('|', '') ;
    }
} ;

var zutils = {
    isMobile : function() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            return true ;
        }
        return false ;
    }
} ;
