// 006
// PATH MODULE

// in node, we have a few useful modules that are built into the core of node.
// check out docs of node, to learn more about built-in modules, objects and other stuffs.

const path = require('path');
// when we use require function, it firsts check if the argument passed is a built-in module or not, if it cannot find, then it searches for the module in our directory and then imports it.

var pathObj = path.parse(__filename)  // __filename is one of the arguments of the module wrapper function

console.log(pathObj)

// the output gives us lot of information about the path passed to parse function

// check docs to learn more about path module of nodejs