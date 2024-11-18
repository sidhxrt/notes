// 007
// OS MODULE

// this module gets us information about the current operating system
// check docs for more detail about os module in nodejs

// the freemem method returns the amount of free memory on our machine.
// the totalmem method returns the amount of total memory on our machine.
// we can get information about the current user using userInfo method
// we can get uptime of our machine using uptime method 

const os = require('os');

var freeMemory = os.freemem();
var totalMemory = os.totalmem();

console.log("free memory: " + freeMemory);
// we can simplify this expression by using a template string which is available in more recent versions of javascript that we refer to as ES6 or ES2015; ECMAScript 6.
// template string was introduced in ES6 that helps us build a string without concatenations.

// instead of single/double quotes, we use backtick character(`)
console.log(`total memory: ${totalMemory}`);

// before node, we could not get this kind of information using javascript, js used to run only inside of a browser and we could only work with the window or document objects.