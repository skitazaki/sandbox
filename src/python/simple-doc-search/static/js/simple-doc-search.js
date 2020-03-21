/**
 * Simple documentation search application.
 * The search server is Solr.
 */
function search(q, start) {
    var params = {
            "wt": "json",
            "q": q,
            "start": start || 0
    };
    return $.ajax({
        "url": "http://s.kitazaki.name/search?" + $.param(params),
        "dataType": "json"
    }).always(function() {
    });
}

(function($){

    /**
     * Model object based on backbone.js.
     */
    var Document = Backbone.Model.extend({});

    var DocumentList = Backbone.Collection.extend({
        model: Document
    });

    /**
     * View object based on backbone.js.
     */
    var DocumentView = Backbone.View.extend({
        template: $("#document_template").html(),

        initialize: function() {
            _.bindAll(this, 'render');
        },
        render: function() {
            var params = {
                    "id": this.model.get("id"),
                    "title": this.model.get("title"),
                    "url": this.model.get("url"),
                    "content": this.model.get("content")
            };
            $(this.el).html(_.template(this.template, params));
            return this;
        }
    });

    var DocumentListView = Backbone.View.extend({
        el: $('#document_container'),
        summary: $("#summary_template").html(),
        pager: $("#pager_template").html(),

        initialize: function() {
            _.bindAll(this, 'render', 'appendItem');
            this.collection = new DocumentList();
            this.collection.bind('add', this.appendItem);
            this.render();
        },
        render: function() {
        },

        appendItem: function(item) {
            var v = new DocumentView({model: item});
            $(this.el).append(v.render().el);
        }
    });

    var rpp = 10;
    function handleResponse(query, response) {
        var numFound = response.numFound,
            start = response.start,
            v = new DocumentListView();
        v.$el.html(_.template(v.summary, {
                    query: query,
                    numFound: numFound,
                    start: start
        }));
        _(response.docs).each(function(item) {
            var doc = new Document(item);
            v.collection.add(doc);
        });
        var params = {
                query: query,
                total: Math.floor((numFound+rpp)/rpp),
                current: Math.floor(((start)/rpp) + 1)
        };
        v.$el.append(_.template(v.pager, params));
    }

    var progress = $("#progress_template").html();
    var AppRouter = Backbone.Router.extend( {
        routes: {
            "search/:query": "query",
            "search/:query/p:page": "query",
            "*actions": "defaultRoute"
        },
        query: function(query, page) {
            var q = decodeURIComponent(query),
                p = Math.max(page, 1);
            $("#document_container").html(progress);
            search(q, (p-1) * rpp).done(function(data) {
                handleResponse(q, data.response);
            }).fail(function() {
                $("#document_container").text("Error.");
            });
        },
        defaultRoute: function(actions) {
        }
    });

    // Initiate the router and history.
    var app = new AppRouter;

    var SearchView = Backbone.View.extend({
        el: $('#search_container'),
        template: $("#search_template").html(),

        events: {
            "submit form": "doSearch"  
        },

        initialize: function() {
            _.bindAll(this, 'render', 'doSearch');
            this.render();
        },
        render: function() {
            $(this.el).html(_.template(this.template, {}));
        },

        doSearch: function(event) {
            event.preventDefault();
            var $q = $("input[name=q]", event.currentTarget),
                q = $q.val();
            if (q) {
                app.navigate("search/" + encodeURIComponent(q), {trigger: true, replace: true});
            } else {
                $q.parent().addClass("error");
                setTimeout(function() {
                    $q.parent().removeClass("error");
                }, 3000);
            }
        }
    });

    new SearchView();

    Backbone.history.start();
})(jQuery);

