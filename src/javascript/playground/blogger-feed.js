var FeedReader = {
    "posts": 5,
    "chars": 100,
    read: function(blog_id) {
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
    parse: function(json) {
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

    callback: function(entries) {
        /* pass, override me :D */
    }
};

const e = React.createElement;

class NameForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '', error: false };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
    if (this.state.value) {
      this.setState({['error']: false});
    }
  }

  handleSubmit(event) {
    event.preventDefault();
    if (!this.state.value) {
      this.setState({['error']: true});
      return;
    }
    if (this.props.onSubmit) {
      this.props.onSubmit(this.state.value);
    }
  }

  render() {
    var cls = '';
    if (this.state.error) {
      cls = ' alert alert-danger';
    }
    return (
      e('form',
        { onSubmit: this.handleSubmit },
        e('div', {
          className: "input-group" },
          e('div', {
            className: "input-group-prepend" },
            e('span', {
              className: "input-group-text" }, 'http://')),
          e('input', {
            className: "form-control" + cls,
            placeholder: "Blogger ID",
            maxlength: 20,
            onChange: this.handleChange }),
          e('div', {
            className: "input-group-append" },
            e('span', {
              className: "input-group-text" }, '.blogspot.com')),
          e('button', { className: "btn btn-primary", onClick: this.handleSubmit }, 'Read')))
    );
  }
}

class BloggerFeedReader extends React.Component {
  constructor(props) {
    super(props);
    this.state = { blogId: "", entries: null };
    FeedReader.posts = 10;
    FeedReader.chars = 140;
  }

  read(self, blogId) {
    self.setState({["blogId"]: blogId});
    self.setState({["entries"]: []});
    FeedReader.callback = function(entries) {
      self.setState({["entries"]: entries});
    };
    try {
      FeedReader.read(blogId);
    } catch (e) {
      try { console.log(e); } catch (ignore) {}
    }
  }

  renderEntries() {
    const entries = this.state.entries;
    var articles;
    if (entries) {
      articles = entries.map(element => {
        return e("div", { className: "row" },
                 e("h3", {}, element["title"]),
                 e("p", {},
                   element["content"] + " ...",
                   e("a", { href: element["url"] }, "More"),
                   e("span", {}, "(" + element["date"] + ")")));
      });
    }
    return e("div", {}, articles);
  }

  render() {
    return e('div', {},
             e(NameForm, { onSubmit: (blogId) => this.read(this, blogId) }),
             this.renderEntries());
  }
}
