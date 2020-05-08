# ROS-Tiago-GoogleAssistant
ROS implementation of Tiago robot which is given commands through Google Assistant.

Dialogflow (a Natural Language Understanding platform) is used to design and integrate the user's conversation into Goggle Assistant. Firebase Firestore DB is used which acts as a communication channel between the Tiago robot and Google Assistant. 
And obviously ROS is used to implement autonomus navigation algorithms on Tiago Robot in order to reach the goal location asked by the user.

The directory <code>workon_tiago</code> is the ROS package which has all the necessary launch, map and command files. 
The <code>src/chatbot_goals.py</code> is the main program that receives the goal location from Firestore DB, translates it to map coordinates and commands the the robot to reach that location autonomously. 

The <code>dialogflow_codes</code> directory has the web fulfillment function file <code>(index.js)</code> which stores the goal location data into Firebase Firestore DB spoken by the user.
