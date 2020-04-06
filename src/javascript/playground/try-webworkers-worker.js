onmessage = function(event) {
    const t = event.data["text"],
          repeatCount = event.data["repeat"];
    var ret = "";
    for (var i = 0; i < repeatCount; i++) {
        if (ret !== "") {
            ret += ", ";
        }
        ret += t;
    }
    postMessage(ret);
};
