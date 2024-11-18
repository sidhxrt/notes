// 009
// EVENTS MODULE

// an event is basically a signal that indicates that something has happened in our application.

const EventEmitter = require('events');
// if the first letter of every word is uppercase, then this is a convention that indicates that this EventEmitter is a class. its not a function, its not a simple value. 
// A class is a container for properties and functions(which we call methods). (a class is a container for a bunch of related methods and properties.)
// so in this EventEmitter class, we have lot of methods(which we can see from docs).

// now, here in order to use this EventEmitter, first we need to create an instance of this class
const emitter = new EventEmitter();
// this emitter is an object of EventEmitter class.

// a class defines the properties and behavior of a concept, but an object is an actual instance of that class.

// we use emit() method to raise an event
emitter.emit('messageLogged'); // the argument passed is the name of the event.
// emit: making a noise or produce something(we are signalling that an event has happened in our application)

// now, if we run app now(with only the above code), nothing is going to happen.
// this is because, even though we have raised an event here, but no where in our application, we have registered a listener that is interested in that event.

// a listener is a function that will be called when that event is raised.
// Registering a Listener
// 'emitter.addListener' is also known as or used as 'emitter.on'  ('on' or 'at', both works)
emitter.on('messageLogged', function(){ console.log('listener called'); }); // this method takes 2 arguments, 'name of the event' and 'the callback function' or the actual listener.



// CLEAN VERSION OF ABOVE CODE---
const EventEmitter = require('events');
const emitter = new EventEmitter();

// Register a Listener
emitter.on('messageLogged', function(){
    console.log('listener called.');
});

// Raise an event
emitter.emit('messageLogged')

// the order is important here, if we register the listener after calling the emit method, nothing would have happened.
// because when we call the emit method, this emitter iterates over all the registered listeners and calls them synchronously.