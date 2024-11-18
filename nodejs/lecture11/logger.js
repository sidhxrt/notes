const EventEmitter = require('events');
const emitter = new EventEmitter();

var url = "https://sampleurl.com/log"

function log(message) {
    // Send an HTTP request
    console.log(message);

    // since, its the logger module that emits or signals an event saying that the message is logged, therefore:
    // Raise an event
    emitter.emit('messageLogged', {id: 1, url: 'https://idklol.com'});
}

module.exports = log;


// now we will create a class called 'logger' that has an additional method called 'log'(same as on line 6)
// when a function is inside a class, we say that it is a method in that class.(we dont say function, we say method)
class Logger {                      // Pascal case convention says that first letter of every word in a class should be uppercase.
    log(message) {                  // inside a class, we dont have to 'function' keyword while declaring a method
        // Send an HTTP request
        console.log(message);

        // Raise an event
        emitter.emit('messageLogged', message);
    }
}

// instead of exporting the log function, we are going to export the Logger class
module.exports = Logger;

// we want this Logger class to have all the capabilities of the EventEmitter(line 1) and we achieve that by using the 'extends' keyword that comes in ES6.
class Logger extends EventEmitter {      // after 'extends', we add the name of parent or base class.               
    log(message) {                  
        // Send an HTTP request
        console.log(message);

        // Raise an event
        // now instead of using the emitter object, we are going to use 'this'
        // so in this class, we can directly emit or raise events
        this.emit('messageLogged', message);
    }
}


// LETS WRITE THE FINAL CLEAN CODE:
const EventEmitter = require('events');

var url = "https://sampleurl.com/log"

class Logger extends EventEmitter {                    
    log(message) {                  
        // Send an HTTP request
        console.log(message);

        // Raise an event
        this.emit('messageLogged', { id: 1, url: 'http://'});
    }
}

module.exports = Logger;