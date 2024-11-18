// 004
// LOADING A MODULE

var url = 'https://somerandomwebsitethatreturnsauthmessage.com/log';

function log(message){
    //some https request it will send to the above url and return us a message, which we will load in the console.
    console.log(message)
}

module.exports.log = log; 