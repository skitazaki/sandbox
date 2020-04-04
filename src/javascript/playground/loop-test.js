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

var TestPatterns = {
    "naive": naiveLoop,
    "dd":    duffsDevice
};

document.forms[0].onsubmit = function(e) {
    e.preventDefault();
    var elements = this.elements,
        count = parseInt(elements["loopcount"].value),
        loopTypeInput = elements["looptype"],
        testType, result;
    if (isNaN(count)) {
        alert("Enter an interger value.");
        return false;
    }
    Loopy.count = count;
    for (var i = 0, len = loopTypeInput.length; i < len; i++) {
        if (loopTypeInput[i].checked)
            testType = loopTypeInput[i].value;
    }
    if (testType in TestPatterns) {
        result = Loopy.run(TestPatterns[testType]);
        document.getElementById("results").innerHTML += count + " " +
            testType + " " + result + "<br/>";
    } else {
        alert("Invalid loop type.");
    }
    return false;
};
