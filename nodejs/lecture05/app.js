// 005
// MODULE WRAPPER FUNCTION


var url = "https://sampleurl.com/log"

function log(message) { 
    console.log(message);
}

module.exports = log;

// if we make sytantic error in the first line of code, for eg, 'var x=;'
// and run 'node app.js', we can see information about a function, that function is called as module wrapper function

// so basically what happens is that node treats the above module-code as the following:
(function (exports, require, module, __filename, __dirname) {
    var url = "https://sampleurl.com/log"

    function log(message) { 
        console.log(message);
    }

    module.exports = log;

})

// this function is called module wrapper function, obviously, there will be more code to this(for now, this is enough to represent an overview of whats happening behind the scenes)
// the above function is an immediately invoked function expression.
// so the conclusion is that node does not directly executes our code(line 5 to line 11), it always wraps the code inside each module into inside of a function(as seen above) and then runs this function.

// we can write exports.log = log; instead of module.exports.log = log(as exports is passed as argument inside the function); however we cannot write exports = log;

// we can write the following(as __filename and __dirname as passed as arguments inside the module wrapper function):
console.log(__filename);
console.log(__dirname);

var url = "https://sampleurl.com/log"

function log(message) { 
    console.log(message);
}

module.exports = log;