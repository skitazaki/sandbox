/**
 * Simple bookmarklet which posts the page title and URL to Twitter.
 * @see `javascript: escape(), encodeURI(), encodeURIComponent() 比較
 *  <http://groundwalker.com/blog/2007/02/javascript_escape_encodeuri_encodeuricomponent_.html>`_
 */
javascript:(function(w, t, h){
    w.open("http://twitter.com/?status=" + encodeURIComponent(" / " + t + " - " + h));
}(window, document.title, location.href))

