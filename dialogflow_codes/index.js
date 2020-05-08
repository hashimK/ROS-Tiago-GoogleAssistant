// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
var https = require ('https');
const {
  dialogflow,
  BasicCard,
  Permission,
  Suggestions,
  Carousel,
  Image,
} = require('actions-on-google');

// Import the firebase-functions package for deployment.
const functions = require('firebase-functions');

// Import firebase-admin for firestore
const admin = require('firebase-admin');

// Instantiate Firestore
admin.initializeApp(functions.config().firebase);
const db = admin.firestore();

// Instantiate the Dialogflow client.
const agent = dialogflow({debug: true});
process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

function welcome(conv,params) {
	conv.ask(`Hi! Im Tiago. You can ask me to move in any direction or give me a goal location to reach.`);
}

function fallback(conv,params) {
	conv.ask(`I didn't understand`);
	conv.ask(`I'm sorry, can you try again?`);
}

function moveTiagoIntentHandler(conv,params) {
	console.log("Function moveTiagoIntentHandler Run");
	// const codeContext=conv.contexts.get("traceiotcontext");
	const parameters = params;
	console.log("Check Started");
	// console.log("codeContext",codeContext);
	console.log("parameters",parameters);

	// Get parameter from Dialogflow with the string to add to the database
    var current_direction = parameters["movement_direction"];

    // Get the database collection 'dialogflow' and document 'agent' and store
    // the document  {entry: "<value of database entry>"} in the 'agent' document
    const dialogflowAgentRef = db.collection('robots').doc('diff-drive');
    return db.runTransaction(t => {
      t.update(dialogflowAgentRef, {joystick_direction : current_direction});
      return Promise.resolve('Update complete');
    }).then(doc => {
	//   conv.ask(`Wrote "${current_direction}" to the Firestore database.`);
	if (current_direction==="north")
	{
		conv.ask(`Ok master, moving forward.`);
	}
	else if(current_direction==="south")
	{
		conv.ask(`Ok master, moving reverse.`);
	}
	else if(current_direction==="east")
	{
		conv.ask(`Ok master, turning right.`);
	}
	else if(current_direction==="west")
	{
		conv.ask(`Ok master, turning left.`);
	}
	else if(current_direction==="stop")
	{
		conv.ask(`Ok I've stopped.`);
	}

	else if(current_direction==="fridge")
	{
		conv.ask(`Ok going towards the fridge`);
	}

	else if(current_direction==="table")
	{
		conv.ask(`Ok attending the table no. 4`);
	}

	else
	{
		conv.ask(`I did not get that`)
	}
	  
    }).catch(err => {
      console.log(`Error writing to Firestore: ${err}`);
	//   conv.ask(`Failed to write "${current_direction}" to the Firestore database.`);
	conv.ask(`Im facing trouble accesing the robot`);
    });
}


agent.intent('Default Welcome Intent', welcome);
agent.intent('Default Fallback Intent', fallback);
// agent.intent('your intent name here', yourFunctionHandler);

agent.intent('moveTiagoIntent', moveTiagoIntentHandler);


exports.dialogflowFirebaseFulfillment = functions.https.onRequest(agent);