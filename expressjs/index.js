// we will first declare a variable for app which represents the actual api that we are building.
// and its value is an import of the express package which itself is a function so we will add parenthesis after it to initialize it.
const app = require('express')();
const PORT = 8080;

// now at this point, our api hasnt defined any endpoints, but lets go ahead and run it anyways.
// firing up the api!
app.listen(     
    // the way we fireup the api on the server is by calling the app.listen,
    // that tells it to listen on a specific port, which is passed as the first argument. 
    PORT,
    // as an optional second argument to listen, we can fire a callback to let us know when the api is ready.
    () => console.log(`its alive on the http://localhost:${PORT}`)
);

// go to terminal and type: 'node .'

// to access our API, we can use either use curl from the command line or use vscode extention(like 'REST Client') or use a REST client like 'insomnia' or 'postman'

// now lets add an endpoint to the API
// we can do that by changing a http verb to the app instance
app.get(
    '/tshirt',   // this will automatically set up our server with the 'tshirt' endpoint.
    // now we will pass a call back function as the second argument to handle the requests to the endpoint.
    (req, res) => {      // this function itself provides access to 2 different objects, the request object and the response object.
        // the request is the incoming data, while the response is the data that we want to send back to the client.
        // the response can have a status code and then we can send a data payload.
        res.status(200).send({
            tshirt: 'lol',
            size: 'large'     // if we pass a javascript object as the argument, then it will send that data back as json by default.
        })
    }             
); 
// whenever a client or end user requests the url 'http://localhost:8080/tshirt', it will fire the above callback function to handle the request.
// restart the server after making changes to the code.

// when dealing with a POST request, it means that the user is trying to create new data on the server.

app.post('/tshirt/:id', (req, res) => {
    const { id } = req.params;    // we need the id which we can get from the url and its value is made available to us on the request parameters object.
    const { logo } = req.body;    // the request object in express allows us to access information from the request message like url params, body, header, etc.

    // we can store the above info in db if needed
    if (!logo) {
        res.status(418).send({message: 'we need a logo!'})
    }
    res.send({
        tshirt: `this is the id: ${id} and this is the logo: ${logo}`
    })
});

// if we run the above code, we will get 500 internal server error.
// this is because, express does not parse JSON in the body by default.
// not everybody uses express to build a JSON API, so thats not the default behavior.
// what we need to do is setup a middleware. a middleware that tells express to parse json before the actual data hits the function that we are using here to handle the request. 
//  REQ -->    MIDDLEWARE   --> RESPONSE
//         <PARSE JSON HERE>
// think of middleware like a shared code that runs before every endpoint callback that we have defined.
// very common middleware is built into express itself.
// we can refactor our code to make a variable for express and 
// then we can call app.use() to apply middleware.
// in this case, the middleware that we want to apply is the 'express.json' middleware.
const express = require('express');
const app = express();
const PORT = 8080;

app.use(express.json())
// now every request that comes in will first go through this express.json middleware which will convert the body to JSON.
// therefore making it available in our POST callback.
app.post('/tshirt/:id', (req, res) => {
    const { id } = req.params;    
    const { logo } = req.body;    

    // we can store the above info in db if needed
    if (!logo) {
        res.status(418).send({message: 'we need a logo!'})
    }
    res.send({
        tshirt: `this is the id: ${id} and this is the logo: ${logo}`
    })
});
// now if we save code, restart out server, we wont get the error.

// OPENAPI specs
/*
 the OPENAPI specs provides a standard way to describe an API in YAML.
 it originally came about in something called the swagger framework.
 we can go to swaggerhub and download the code boilerplate(of how to write a REST API)
 this is not mandatory, but if we describe our API with OPENAPI spec, we can then upload the configuration to tools like API gateway on AWS or google cloud.
 where it can be secured, monitored and connected to backend infrastructure.
*/