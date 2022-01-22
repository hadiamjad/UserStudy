var cookieGetter = document.__lookupGetter__("cookie").bind(document);
var cookieSetter = document.__lookupSetter__("cookie").bind(document);

Object.defineProperty(document, 'cookie', {
    get: function() {
        console.log('I am reading the cookie');
    },

    set: function(cookieString) {
        console.log('I am setting the cookie');
    }
});