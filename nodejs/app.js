// FIRST NODE PROGRAM
function sayhello(name){
    console.log("hello " + name)
}

sayhello('sid')


console.log(window)
// this wont work, nodejs is just a cpp program that includes chromes v8 js engine.
// in node, we dont have the window or document objects(these are part of runtime environment that we get with browsers)
// in node, we have other objects to work with files, os, network and so on.


// NODE MODULE SYSTEM