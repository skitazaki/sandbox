function process(item)
{
    return item + item + item;
}

function naiveLoop(count)
{
    for (var i = 0; i < count; i++)
        process(i);
}

function duffsDevice(count)
{
    var i = count % 8;
    while (i)
        process(i--);
    i = count - i;
    while (i) {
        process(i--);
        process(i--);
        process(i--);
        process(i--);
        process(i--);
        process(i--);
        process(i--);
        process(i--);
    }
}

var Loopy = {
    "count": 10000,
    "run": function(loop) {
        var start = +new Date(),
            end;
        loop(this.count);
        end = +new Date();
        return end - start;
    }
};
