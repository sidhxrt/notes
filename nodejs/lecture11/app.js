// 011
// EXTENDING EVENTEMITTER


// referring lecture 10, in the real world, its quite rare that we would work with the EventEmitter object directly(emitter in lecture10).
// instead we will create a class that has all the capabilities of the EventEmitter and then we will use that class in our code.

const EventEmitter = require('events')
const emitter = new EventEmitter();

// Register a listener
emitter.on('messageLogged', (arg) => {   // this listener is only registered with the EventEmitter of this module and not the other module.
    console.log('listener called', arg)
});

// now we need to load the logger module and call the log function
const log = require('./logger')
log('message');


// now if we run 'node app.js' it will only print 'message' on the console, the event listener will not be called.
// this is because, the emitter object of EventEmitter class in app.js and logger.js are 2 different objects.
// so to solve this problem, we will create a class that has all the capabilities of this EventEmitter class and some additional capabilities and then we will use this class in our code.
// go to logger.py for further explanation.


// LETS WRITE THE FINAL CLEAN CODE:
const EventEmitter = require('events')

const Logger = require('./logger');
const logger = new Logger();

// Register a Listener
logger.on('messageLogged', (arg) => {
    console.log('listener called', arg);
});

logger.log('message');

// so now if we run 'node app.js', we will get the following in the output on the console:
// message
// Listener called { id: 1, url: 'http://'}