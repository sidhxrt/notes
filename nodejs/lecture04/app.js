// 004
// LOADING A MODULE

// to load a module, we will use the 'require()' function. this is one of the functions that we have in node but not in browsers.
require('./logger'); // this function takes one argument and thats the name or path of the target module that we want to load
// './' indicates current folder
// now if this logger was in subfoler, we will make the path as: require('./subfolder/logger')
// if it was in the parent folder, we can use require('../subfolder/logger') or require('../logger')
// we need not add logger.js as node will automatically assume that the file passed as argument in require() will be a js file and automatically adds the .js extention

// this require function returns the object that is exported from the mentioned target module(we can check this exports manually by typing: console.log(module))
var logger = require('./logger');

console.log(logger);

// when we run the 'node app.js' we get the following as output:
// { log: [Function: log]}
// now, we can call this function/method in app.js
logger.log('message');
// output will be 'message' after we run 'node app.js'


// in the recent versions of javascript, we have the ability to define constants, 
// so as a best practice, when loading a module using the require function, its better to store the result in a constant
const logger = require('./logger');


// sometimes, instead of exporting an object from a module, we may want to export only a single function
// for example, in our logger module, we dont necessarily need an object because we have a single method.
// an object would be useful if we had multiple methods or properties here.
// in this case(current logger), instead of exporting an object, we can export a single function. so lets modify the code a lil
// logger.js - 
var url = 'https://sampleurl.com/log';
function logg(message){
    console.log(message);
}

module.exports = logg;

// app.js
const log = require('./logger');
log('message');

// running 'node app.js' will give us the same output
// so in our modules, we can export a single function or an object.