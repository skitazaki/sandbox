var FeedReader = {
    "posts" : 5,
    "chars" : 100,
    read : function(blog_id) {
        var script = document.createElement("script");
        var feed_url = "http://" + blog_id + ".blogspot.com";
        feed_url += "/feeds/posts/default";
        feed_url += "?alt=json-in-script&callback=FeedReader.parse";
        try { console.log("load: " + feed_url); } catch (ignore) {}
        script.src = feed_url;
        document.body.appendChild(script);
        /* this method should be rewritten to check script is executed after safe loading */
        setTimeout(function() { document.body.removeChild(script); }, 5000);
    },
    parse : function(json) {
        if (json == null || json.feed == "undefined") {
            try { console.log("fail to load json data."); } catch (ignore) {}
            return;
        }
        var entries = [];
        for (var i = 0; i < this.posts; i++) {
            var entry = json.feed.entry[i];
            // text element representation includes special dollar symbol.
            var posttitle = entry.title.$t;
            // get the post url
            // check all links for the link with rel = alternate
            var posturl;
            if (i == json.feed.entry.length) break;
            for (var k = 0; k < entry.link.length; k++) {
                if (entry.link[k].rel == 'alternate') {
                    posturl = entry.link[k].href;
                    break;
                }
            }
            // get the postdate, take only the first 10 characters
            var postdate = entry.published.$t.substring(0,10);
            // get the post author
            var postauthor = entry.author[0].name.$t;
            // get the postcontent
            // if the Blogger-feed is set to FULL, then the content is in the content-field
            // if the Blogger-feed is set to SHORT, then the content is in the summary-field
            if ("content" in entry) {
                var postcontent = entry.content.$t;
            } else if ("summary" in entry) {
                var postcontent = entry.summary.$t;
            } else
                var postcontent = "";
            // strip off all html-tags
            var re = /<\S[^>]*>/g;
            postcontent = postcontent.replace(re, "");
            // reduce postcontent to numchar characters
            if (postcontent.length > this.chars) postcontent = postcontent.substring(0, this.chars);
            entries.push({"title":posttitle, "content":postcontent,
                    "date":postdate, "url":posturl});
        }
        this.callback(entries);
    },
    callback : function(entries) {
        /* pass, override me :D */
    }
}

