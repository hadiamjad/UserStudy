var cookieGetter = document.__lookupGetter__("cookie").bind(document);
var cookieSetter = document.__lookupSetter__("cookie").bind(document);

Object.defineProperty(document, 'cookie', {
    get: function() {
        var storedCookieStr = cookieGetter();
        console.log(storedCookieStr);
        console.trace();
    },

    set: function(cookieString) {
        // console.log(cookieString);
    }
});