// 003
// CREATING A MODULE

var url = 'https://somerandomwebsitethatreturnsauthmessage.com/log';

function log(message){
    //some https request it will send to the above url and return us a message, which we will load in the console.
    console.log(message)
}

// now the variable url and the function log got its scope limited to this module/file. 
// to make it accessible for other modules or applications to use, we need to export it.
module.exports.log = log; 
module.exports.endpointurl = url; // we can export it with any name(here, we used 'endpointurl'). it need not be the same name as the one we are using internally in this module.

// usually, we dont export every variable or function that are declared inside the module, we only export the ones that needs to be used by other modules/applications
// in the above module, we need not export url variable as it is used for internal implementation.
// whatever we export becomes public.(i.e can be access by anyone)
// so the final version of this module will look like this:
var url = 'https://somerandomwebsitethatreturnsauthmessage.com/log';

function log(message){
    //some https request it will send to the above url and return us a message, which we will load in the console.
    console.log(message)
}

module.exports.log = log; 