function onmessage(event) {
    var t = event.data["text"],
        ret = "";
    for (var i = 0, len = event.data["count"]; i < len; i++) {
        ret += t;
    }
    postMessage(ret);
}
