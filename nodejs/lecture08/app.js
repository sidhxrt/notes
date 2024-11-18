// 008
// FILE SYSTEM MODULE

// here, we will learn how to work with files in node.
// check node docs for more information on file system module of nodejs

const fs = require('fs');
// when we do fs. we can see bunch of methods(sync and async), we use async ones in real world applications. sync is present just for simplicity.

// the thing is, a node process has a single thread, if we are using node to build the backend for our application, 
// we might have several hundreds or thousands of clients connecting to that backend.
// if we keep that single thread busy, we wont be able to serve many clients. so always use asynchronous methods.

// lets first see fs.readdir(), we will first see the synchronous form as that is easier to understand.
const files = fs.readdirSync('./');   // this will return all the files and folders in the current folder
// so, files will be a string-array
console.log(files)

// now, lets take a look at the asynchronous form of this method.
// just like before, the first argument is the path
fs.readdir('./', function(err, files){      // so, here we need to check if we have an error or the result, only one of these arguments will have a value and the other will be a null.
    if (err) console.log('error: ', err);
    else console.log('result', files);
})
// all these asynchronous methods take a function as their last argument. node will call that function when the asynchronous operation completes.
// we call this function, 'callback'.
// this callback function takes 2 arguments, an error and result(which in this case, is a string array).
// we can call this string-array 'files'(as we did in synchronous form)
// the above will give us proper output.

// now if we want to simulate an error:
fs.readdir('some_random_value', function(err, files){ 
    if (err) console.log('error: ', err);
    else console.log('result', files);
})
// the output will be error.