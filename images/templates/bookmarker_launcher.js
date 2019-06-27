//.src = 'https://c836bb8b.ngrok.io/static/js/bookmarklet.js?r=' +

(function () {
    if (window.myBookmarklet !== undefined) {
        myBookmarklet();
    } else {
        document.body.appendChild(document.createElement('script'))
            .src = 'https://nenu1985.herokuapp/static/js/bookmarklet.js?r=' +
            Math.floor(Math.random() * 99999999999999999999);
    }
})();