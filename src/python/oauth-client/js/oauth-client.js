/**
 * Sample client for OAuth 3-way dance.
 * User agent must support XHR2 and localStorage.
 * Chrome is the best friend of you.
 *
 * This script requires these libraries.
 * - jquery.js
 * - oauth.js
 * - sha1.js
 */
if (typeof OAuth === 'undefined') {
    alert("could not load OAuth library. check your deployment.");
}

/**
 * TODO: write document.
 * TODO: extend 'OAuth' instead of implementing in own namespace.
 */
var OAuthClient = function(consumer, token) {
    this.ck = consumer;
    this.token = token;
};
OAuthClient.prototype = {
    get : function(url, params, callback, errback) {
        var ck = this.ck, t = this.token,
            message = {
                method: 'GET'
              , action: url
              , parameters: [] },
            request = {};
        message.parameters.push(['oauth_consumer_key', ck[0]]);
        message.parameters.push(['oauth_token', t[0]]);
        OAuthClient.signMessage(message, ck, t);
        request['method'] = 'GET';
        request['url'] = url;
        authorization = OAuth.getAuthorizationHeader(
                            message.action, message.parameters);
        request['Authorization'] = authorization;
        request['Content-Type'] = 'application/xml+atom';
        // Use server-side proxy.
        //$.post('/works/oauth-client', request, callback, errback);
        // Use native request via cross-domain-request.
        $.ajax(url, {
            headers: {'Authorization': authorization,
                      'Content-Type': 'application/xml+atom'},
            crossDomain: true,
            success: callback,
            error: errback
        });
    }
  , isInitialized : function() {
        return (this.ck && this.ck.length === 2 &&
                this.token && this.token.length === 2);
    }
  , toString : function() {
        var ck = this.ck, t = this.token,
            dt = [ck[0], ck[1], t[0], t[1]];
        return dt.join('\0');
    }
};

OAuthClient.fromString = function(str) {
    var dt = str.split('\0');
    if (dt.length !== 4) {
        console.error("Invalid input string: " + str);
        throw str;
    }
    return new OAuthClient([dt[0], dt[1]], [dt[2], dt[3]]);
}

OAuthClient.signMessage = function(message, ck, token) {
    var accessor = {'consumerKey': ck[0], 'consumerSecret': ck[1]};
    if (token != null) {
        accessor['token'] = token[0];
        accessor['tokenSecret'] = token[1];
    }
    OAuth.completeRequest(message, accessor);
    OAuth.SignatureMethod.sign(message, accessor);
}

OAuthClient.unpackToken = function(response, callback) {
    var p = OAuth.decodeForm($.trim(response)),
        token, tokenSecret,
        i, k, len;
    for (i = 0, len = p.length; i < len; i++) {
        k = p[i][0];
        if (k == 'oauth_token')
            token = p[i][1];
        else if (k == 'oauth_token_secret')
            tokenSecret = p[i][1];
        else if (k == 'oauth_problem')
            throw ("認証に失敗しました。oauth_problem: " + p[i][1]);
    }
    if (token && tokenSecret) {
        //console.log("token: " + token + ", tokenSecret: " + tokenSecret);
        callback(token, tokenSecret);
    } else {
        console.error("either token or tokenSecret is missing.");
    }
}

OAuthClient.request = function(message, callback, errback) {
    // Server-side MUST implement handling 'Preflighted requests'
    // to accept following headers with OPTIONS.
    // * Access-Control-Request-Method: POST
    // * Access-Control-Request-Headers: Authorization
    // See also:
    // https://developer.mozilla.org/Ja/HTTP_access_control
    // http://stackoverflow.com/questions/1099787/jquery-ajax-post-sending-options-as-request-method-in-firefox
    var xhr = new XMLHttpRequest();
    xhr.open(message.method, message.action);
    xhr.setRequestHeader("Content-Type",
                "application/x-www-form-urlencoded");
    //xhr.setRequestHeader("Authorization",
    //    OAuth.getAuthorizationHeader("localhost", message.parameters));
    xhr.send(OAuth.formEncode(message.parameters));
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200)
                callback(xhr.responseText);
            else if (errback)
                errback(xhr.responseText);
            else if (OAuthClient.onError)
                OAuthClient.onError(xhr.responseText);
            else
                throw xhr;
        }
    };
}

OAuthClient.Dance = function(sp, client) {
    if (sp.steps.length !== 3) {
        alert("Invalid configuration. Given steps is NOT three.");
        return;
    }
    this.sp = sp;
    this.client = client;
};
OAuthClient.Dance.prototype = {
    fetchRequestToken : function(onreadyCallback, onloadCallback, errback) {
        var self = this,
            steps = this.sp.steps,
            message = {method: 'POST', action: steps[0]};
        OAuthClient.signMessage(message, this.client.ck);
        OAuthClient.request(message,
            function(text) {
                //console.log(text);
                if (onloadCallback)
                    onloadCallback(text);
                OAuthClient.unpackToken(text, function(token, tokenSecret) {
                    self.temp = [token, tokenSecret];
                    var link = steps[1] + "?oauth_token=" + token
                                + "&oauth_callback=" + location.href;
                    onreadyCallback(link);
                });
            }, errback
        );
    }
  , fetchAccessToken : function(verifier, onloadCallback, errback) {
        if (verifier == null || verifier == "") {
            alert("Verifier code is Empty!!");
            return false;
        }
        var temp = this.temp,
            params = [["oauth_token", temp[0]],
                      ["oauth_verifier", verifier]],
            message = {
                "method": "POST"
              , "action": this.sp.steps[2]
              , "parameters": params },
            self = this;
        OAuthClient.signMessage(message, this.client.ck, temp);
        OAuthClient.request(message,
            function(text) {
                onloadCallback(text);
                OAuthClient.unpackToken(text,
                    function(token, tokenSecret) {
                        self.temp = null;
                        self.client.token = [token, tokenSecret];
                    });
            }, errback
        );
        return true;
    }
}

OAuthClient.Dance.handleCallback = function(query) {
    var p = OAuth.decodeForm(query),
        i, len, tok, ver;
    if (p) {
        for (i = 0, len = p.length; i < len; i++) {
            if (p[i][0] == 'oauth_token')
                tok = p[i][1];
            else if (p[i][0] == 'oauth_verifier')
                ver = p[i][1];
        }
        if (tok && ver)
            return ver;
    }
    return false;
}
