var alexa = require('alexa-app');
var app = new alexa.app();

app.launch(function(request, response){
 response.say("Hello there, I am a bot created to help you find what to eat for lunch.");
 response.shouldEndSession(false);
})

app.intent('GetLunchSuggestions',
 {
  "slots": {},
  "utterances": [
   "what's for lunch",
   "where should {I|we} go for lunch"
  ]
 },

 function (request, response) {
  generate_suggestions(response);
  return; 
 }
);

function generate_suggestions(response){
 var food = ["Thai",
  "Sushi",
  "Chik-fil-a",
  "Smash Burgers",
  "Uncle Julio's"
 ];

var rand = food[Math.floor(Math.random() * food.length)];
response.say("How about some " + rand + " today?");
 response.send();
return ;
}

// Connect to lambda

exports.handler = app.lambda();

if ((process.argv.length === 3) && (process.argv[2] === 'schema'))
{
    console.log (app.schema ());
    console.log (app.utterances ());
}
