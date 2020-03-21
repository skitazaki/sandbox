/**
 * Sample User Interface to use OAuthClient.
 * Screens are composed from 6 stages.
 * 1. register information about service provider and consumer token.
 * 2. initiate OAuth dance to POST signed request.
 * 3. indicate move to authorization page on target service.
 * 4. handle callback to get verifier code and prepare final request.
 * 5. get the access token and save them on browser 'localStorage'.
 * 6. try to access authorized resource using tokens.
 *
 * We can inspect access token to use developer tools.
 *
 * This script requires these libraries.
 * - jquery.js
 * - jquery.history.js
 * - oauth-client.js
 */

if (typeof OAuthClient === 'undefined') {
    alert("could not load OAuthClient. check your deployment.");
}

var STORAGE_KEY = 'oauth-client';

/**
 * User Interfaces separeted by forms.
 * Each stage is consists of `menu` and `form`.
 * `menu` is a clickable item to change stage back and forth, and `form`
 * is a block to show the correspondant form.
 */
var STAGES = {
    register:  { form:null, menu:null }
  , initiate:  { form:null, menu:null }
  , authorize: { form:null, menu:null }
  , access:    { form:null, menu:null }
  , save:      { form:null, menu:null }
  , get:       { form:null, menu:null }
  , current:   null
  , Forward: function(next) {
      if (next) {
          if (this.current) {
              if (this.current.form)
                  $(this.current.form).hide();
              if (this.current.menu)
                  $(this.current.menu).removeClass("active");
          }
          this.current = next;
          if (this.current.form)
              $(this.current.form).show("slow");
          if (this.current.menu)
              $(this.current.menu).addClass("active");
      }
    }
  , Install: function(stage, callback) {
      var self = this[stage].form;
      $(self).submit(function(){
          try {
              callback(this);
          } catch (e) {
              console.error(e);
              $('div.warning').hide();
              var message = $("<div/>", {"class":"warning"}).text(e.toString());
              $(message).prependTo(self);
              setTimeout(function() {
                  $(message).remove();
              }, 10000);
          }
          return false;
      });
    }
};

var Util = {
    hasEmpty: function(form) {
        var r = false;
        $(form).find('input').each(function() {
            var $e = $(this);
            if ($e.val() == "") {
                $e.addClass("warning");
                setTimeout(function() {
                    $e.removeClass("warning");
                }, 1000);
                r = true;
            }
        });
        return r;
    }
};

/**
 * Initialization code goes from here.
 */

// handle verifier code when getting back from service provider to
// callback URL, which is this same file on another tab.
(function(query, parent) {
    if (query) {
        var verifier = OAuthClient.Dance.handleCallback(query),
            field = 'oauth_verifier';
        if (verifier) {
            if (parent &&
                parent.document.getElementById(field)) {
                parent.document.getElementById(field).value = verifier;
                window.close();
            } else
                alert("Verifier code: " + verifier);
        } else {
            alert("Invalid access. close this window.");
            window.close();
        }
    }
})(location.search.substring(1), window.opener)

$(function() {
    // set forms on each stage.
    for (var i = 0, forms = document.forms, len = forms.length; i < len; i++) {
        var action = $(forms[i]).attr('action').substring(1); // remove "#" character
        if (action in STAGES)
            STAGES[action].form = forms[i];
    }
    // set menus on each stage.
    $("#oauth-client-steps li").each(function(index) {
        var stage = this.firstChild.hash.substring(1);
        if (stage in STAGES)
            STAGES[stage].menu = this;
    });

    var client = null, dancer = null;
    (function(s) {
        if (STORAGE_KEY in s) {
            client = OAuthClient.fromString(s[STORAGE_KEY]);
        }
    }(localStorage));

    // show appropriate stage by detecting accessor status and history-hash.
    $.History.bind(function(state) {
        // TODO: think again.
        if (state in STAGES) {
            if (!client && !dancer) {
                STAGES.Forward(STAGES.register);
            } else if (state === 'get' &&
                (!client || !client.isInitialized())) {
                STAGES.Forward(STAGES.initiate);
            } else {
                STAGES.Forward(STAGES[state]);
            }
        }
    });
    if (location.hash.length < 2)
        STAGES.Forward(STAGES.register);

    // Install `onsubmit` handler on each stage.
    STAGES.Install("register", function(form) {
        if (Util.hasEmpty(form))
            throw "空のフィールドがあります。";
        var el = form.elements, steps = [];

        steps.push($(el['step1']).val());
        steps.push($(el['step2']).val());
        steps.push($(el['step3']).val());
        client = new OAuthClient(
                        [$(el['key']).val(), $(el['secret']).val()]);
        dancer = new OAuthClient.Dance({steps: steps}, client);
        STAGES.Forward(STAGES.initiate);
    });
    STAGES.Install("initiate", function(form) {
        if (!dancer) {
            STAGES.Forward(STAGES.register);
        }
        var el = STAGES.authorize.form.elements;
        dancer.fetchRequestToken(
            function(link) {
                $(el.link).val(link); STAGES.Forward(STAGES.authorize);
            }
          , function(text) { $(el.response).val(text); }
        );
    });
    STAGES.Install("authorize", function(form) {
        window.open(form.elements.link.value, 'authorize');
        STAGES.Forward(STAGES.access);
    });
    STAGES.Install("access", function(form) {
        if (Util.hasEmpty(form))
            throw "確認コードを入力してください。";
        var verifier = $(form.elements['verifier']).val();

        dancer.fetchAccessToken(verifier, function(text) {
            $(STAGES.save.form.elements.response).val(text);
            STAGES.Forward(STAGES.save);
        });
    });
    STAGES.Install("save", function(form) {
        localStorage[STORAGE_KEY] = dancer.client.toString();
        STAGES.Forward(STAGES.get);
        $.History.go('get');
    });
    STAGES.Install("get", function(form) {
        if (Util.hasEmpty(form))
            throw "リソースの URL を入力してください。";
        var url = $(form.elements['url']).val(),
            params = {};

        client.get(url, params, function(doc) {
            $("#resources").empty();
            // TODO: ensure the content type is text/plain.
            $("<pre></pre>").text(doc).appendTo("#resources");
        });
    });

    // install some handlers.
    OAuthClient.onError = function(e) {
        var message = $("<div/>", {"class":"warning"});
        message.append($("<p/>").text("通信に失敗しました。"));
        if (e.status && e.responseText)
            $("<pre/>").text("Status: " + e.status +
                        ", Response: " + e.responseText).appendTo(message);
        $(message).prependTo(STAGES.current.form);
        setTimeout(function() {
            $(message).remove();
        }, 5000);
    }

    // install history handler with jquery.history.
    var export_space = $("#service_provider_display");
    export_space.hide();
    $.History.bind("export", function(state) {
        if (!client) {
            return;
        }
        export_space.text(JSON.stringify(client));
        export_space.show("slow");
        setTimeout(function() {
            export_space.text("");
            export_space.hide();
            $.History.go("initiate");
        }, 20000);
    });
    $.History.bind("clear", function(state) {
        localStorage.removeItem(STORAGE_KEY);
        $.History.go("initiate");
    });
});
