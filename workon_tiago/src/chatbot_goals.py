#!/usr/bin/env python

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# import datetime
# from time import sleep
import rospy
from geometry_msgs.msg import Twist
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point

# Use the application default credentials
cred = credentials.Certificate("private_key/rosteleop-firebase-adminsdk-x6mz9-da9bfa8104.json")
firebase_admin.initialize_app(cred, {
  'projectId': "rosteleop",
})

db = firestore.client()

doc_ref = db.collection(u'robots').document(u'diff-drive')

#this method will make the robot move to the goal location
def move_to_goal(xGoal,yGoal,zQuat,wQuat):

    #define a client for to send goal requests to the move_base server through a SimpleActionClient
    ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

    #wait for the action server to come up
    while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
        rospy.loginfo("Waiting for the move_base action server to come up")

    goal = MoveBaseGoal()


    #set up the frame parameters
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    # moving towards the goal*/

    goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = zQuat
    goal.target_pose.pose.orientation.w = wQuat

    rospy.loginfo("Sending goal location ...")
    ac.send_goal(goal)

    ac.wait_for_result(rospy.Duration(60))

    if(ac.get_state() ==  GoalStatus.SUCCEEDED):
        rospy.loginfo("You have reached the destination")
        return True

    else:
        rospy.loginfo("The robot failed to reach the destination")
        return False


# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    global joystickDirection
    print(u'Callback received query snapshot.')
    for change in changes:
        if change.type.name == 'ADDED':
            print(u'New data: {}'.format(change.document.to_dict().get('joystick_direction')))
        elif change.type.name == 'MODIFIED':
            joystickDirection=change.document.to_dict().get('joystick_direction')
            if joystickDirection=="fridge":
                x_goal = -5.2
                y_goal = 2.17
                zQuat = -0.9939
                wQuat = 0.109826
                print'start go to goal'
                move_to_goal(x_goal,y_goal,zQuat,wQuat)
            elif joystickDirection=="table":
                x_goal = 0.367
                y_goal = -5.869
                zQuat = -0.621555
                wQuat = 0.78336977
                print'start go to goal'
                move_to_goal(x_goal,y_goal,zQuat,wQuat)
            print(u'Modified data: {}'.format(joystickDirection))
            
        elif change.type.name == 'REMOVED':
            print(u'Removed data: {}'.format(change.document.id))

if __name__ == '__main__':
   rospy.init_node('map_navigation', anonymous=True)
   # Watch the document
   doc_watch = doc_ref.on_snapshot(on_snapshot)
   
   rospy.spin()
