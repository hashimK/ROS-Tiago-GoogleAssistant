#!/usr/bin/env python

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# import datetime
# from time import sleep
import rospy
from geometry_msgs.msg import Twist

# Use the application default credentials
cred = credentials.Certificate("private_key/rosteleop-firebase-adminsdk-x6mz9-da9bfa8104.json")
firebase_admin.initialize_app(cred, {
  'projectId': "rosteleop",
})

db = firestore.client()

doc_ref = db.collection(u'robots').document(u'diff-drive')

pub = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size=10)
rospy.init_node('iot', anonymous=True)
#set the loop rate
rate = rospy.Rate(10) # 10hz

velocity_message = Twist()
joystickDirection="stop"

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    global joystickDirection
    print(u'Callback received query snapshot.')
    for change in changes:
        if change.type.name == 'ADDED':
            print(u'New data: {}'.format(change.document.to_dict().get('joystick_direction')))
        elif change.type.name == 'MODIFIED':
            joystickDirection=change.document.to_dict().get('joystick_direction')
            print(u'Modified data: {}'.format(joystickDirection))
            
        elif change.type.name == 'REMOVED':
            print(u'Removed data: {}'.format(change.document.id))

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

#keep publishing until a Ctrl-C is pressed
while not rospy.is_shutdown():
    if joystickDirection=="stop":
        angularSpeed=0.0
        linearSpeed=0.0
    elif joystickDirection=="north":
        angularSpeed=0.0
        linearSpeed=1.0
    elif joystickDirection=="east":
        angularSpeed=-1.0
        linearSpeed=0.0
    elif joystickDirection=="south":
        angularSpeed=0.0
        linearSpeed=-1.0
    elif joystickDirection=="west":
        angularSpeed=1.0
        linearSpeed=0.0
    elif joystickDirection=="north-east":
        angularSpeed=-1.0
        linearSpeed=1.0
    elif joystickDirection=="south-east":
        angularSpeed=-1.0
        linearSpeed=-1.0
    elif joystickDirection=="north-west":
        angularSpeed=1.0
        linearSpeed=1.0
    elif joystickDirection=="south-west":
        angularSpeed=1.0
        linearSpeed=-1.0
    velocity_message.angular.z=angularSpeed*2.0
    velocity_message.linear.x=linearSpeed*3.0
    pub.publish(velocity_message)
    rate.sleep()
