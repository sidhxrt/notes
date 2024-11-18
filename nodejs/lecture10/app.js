// 010
// EVENT ARGUMENTS


// quite often, when we want to raise an event, we also want to send some data about that event. we do that by adding additional arguements which we refer to as 'event arguments' to emit function.

const EventEmitter = require('events');
const emitter = new EventEmitter();

// Register a Listener
emitter.on('messageLogged', function(){
    console.log('listener called.');
});

// Raise an event
emitter.emit('messageLogged', id, url);  // adding 'event arguments'

// if we want to send multiple values about an event, its a better practice to encapsulate those values inside an object. so:
emitter.emit('messageLogged', {id: 1, url: 'http://someurl.com'});
// we are referring to this object: {id: 1, url: 'http://someurl.com'} as 'event argument'

// now lets update the listener
emitter.on('messageLogged', function(arg){  // we can name the argument variable anything, but general convention is to use arg, e or eventArg.
    console.log('listener called.', arg);
});


// to make the code little bit simpler, in ES6, we have this feature called 'arrow function'.
// in arrow function, we remove the 'function' keyword, separate the argument and function-body with '=>' (arrow); thats why we call this as 'arrow function'.
// final clean structure of code:
const EventEmitter = require('events');
const emitter = new EventEmitter();

// Register a Listener
emitter.on('messageLogged', (arg) => {
    console.log('listener called.', arg);
});

// Raise an event
emitter.emit('messageLogged', {id: 1, url: 'http://sampleurl.com'});  