// NODE MODULE SYSTEM

console.log()
// we have used the console.log function to log something on the console.
// this console object is a global object, so its part of the global scope; which means we can access it anywhere, in any files.

// there are a bunch of other objects and functions that are also globally available in node, for example:
setTimeout()  // we use this to call a function after a delay(like time.sleep() in python)
clearTimeout()

setInterval() // we use this to repeatedly call a function after a given delay.
clearInterval() // we use this to stop that function from being called repeatedly.

/* 
window : in browser, we have this window object that represents our global scope.
so all the functions and variables that are defined globally, we can access them via this window object.
so we can call:
window.console.log() 
or simply console.log(), coz the javascript engine will prefix this statement with window(i.e console.log() -> window.console.log()) because thats where this object is defined.

similarly, all the other functions that we defined above(setTimeout etc) as global ones belong to window object.
so we can call:
window.setTimeout() or window.setInterval()

now similar to above, when we declare a variable like:
var message = '';
this variable is also available via the window object(i.e window.message)

NOW,
in node, we dont have this window object, instead we have another object called 'global'.
so, we can use global the in node the same way we use window in pure js.
for eg,
global.console.log()

but, unlike window object, in node, when we declare variable, unless we mention explicitly, it will not have global scope.
i.e the variable's scope will be limited to the file where it is declared
i.e
var message = '';
console.log(global.message);
this will return as 'undefined'; this is because of node's modular system.
*/

// the following code is valid in pure js, 
var sayhello = function() {

}

window.sayhello();
// but the problem is if any variable or function declared is given global scope then it will get overwritten if we declare another variable or function with same name.
// in complex projects, we will use variables with same name in other files(if not in same file), so if global scope is given then it will get overwritten.
// thats why in node, we follow a modular system. it means that any variabe or function declared has its scope limited to the module/file where it is declared.(they are encapsulated inside of that module)
// in the language of oops, we say that these variables are private(that is their scope is limited to the container/module where they are defined), they are not available outside that container.
// now if we want to use a variable or function defined in a module outside that module, we need to explicitly export it and make it public.

// every node application has atleast one file or one module which we call the main module.

// we can run the following code to learn more about our current module. the module is not global, so we cannot use global.module.
console.log(module)

// in node, every file is a module and the variables and functions defined in that file are scoped to that module. they are not available outside of that module.