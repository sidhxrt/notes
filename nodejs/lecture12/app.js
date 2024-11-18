// 012
// HTTP Module


// one of the powerful building blocks of node is the HTTP module that we use for creating networking applications.
// for example, we can create a web server that listens for HTTP requests on a given port.
// and with this, we can easily create a backend service for our client applications.(like React/Angular)

// if we go to docs, on http.Server class, we can see that this class inherits from net.Server class(this is another class defined in the net module).
// now if we dive further in docs, we can see that net.Server is an EventEmitter.

const http = require('http');

const server = http.createServer();
// this server is an event emitter, so it has all the capabilities of event emitter that we saw in lecture 11.
// so, server.on, server.addListener, server.emit all are present.

// everytime, there is a new connection(as server is listening on port 3000) or new request, this server raises an event. 
// so we can use the 'on' method to handle that event. 
// so before listening, we will register a listener or a handler.
server.on('connection', (socket) => {   // name of the event is connection which is the first argument and the second argument is the callback function or the actual listener(this listener is a function with one argument that is socket of type Socket class and it returns void)<we got to know this info from tool tip or can get this info from docs>. 
    console.log('New connection...');
});

server.listen(3000)  // server will listen at port 3000

console.log('listening on port 3000...')

// this server object raises different kinds of events that we can respond to.
// now in real world applications, we are not going to respond to the connection event to build an HTTP service. this is very low level.
// so what we commonly do is we pass a callback function to the below 'createServer' method.
const http = require('http');

const server = http.createServer((req, res) => {   // this callback function takes 2 parameters, request and response. 
    // now in this function, instead of working with the socket, we can work with actual request or response objects.
    if (req.url === "/") {
        // if request ka url is this then send something to client in response(which we gonna write below)
        res.write('Hello World');
        res.end();   // we are ending the response here.
    }

    if (req.url === "/api/courses") {
        res.write(JSON.stringify([1,2,3]));  // JSON.stringify() will convert this array into a string using JSON syntax. and then we will write it to the response.
        res.end();
    }
});

server.listen(3000);

console.log('Listening on port 3000....')

// in the real world, we are not going to use this HTTP module to build a backend service for our application.
// because when we add more routes, this code gets more complex, because we add all of them in a linear way inside this callback function.
// so instead, we use a framework called Express which gives our application a clean structure to handle various routes.
// internally, the express framework is built on top of the HTTP module in node.