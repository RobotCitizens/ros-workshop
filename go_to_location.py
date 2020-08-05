#!/usr/bin/env python
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from tf.transformations import quaternion_from_euler

class RobotNavigation():
    def __init__():
        rospy.init_node('nav_test', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        #tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("wait for the action server to come up")
        #allow up to 5 seconds for the action server to come up
        move_base.wait_for_server(rospy.Duration(5))

    def go_to_location(self, position_name):
        x,y,theta = read_position(position_name)        
        x,y,theta = float(x), float(y), float(theta)
        #convert euler to quanternion
        q = quaternion_from_euler(0,0,theta) 
        goal = MoveBaseGoal()        
        goal.target_pose.header.frame_id = 'map'        
        goal.target_pose.header.stamp = rospy.Time.now()        
        goal.target_pose.pose = Pose(Point(x, y, 0.000), Quaternion(q[0], q[1], q[2], q[3]))            
        self.move_base.send_goal(goal)        
        success = self.move_base.wait_for_result(rospy.Duration(60))
        state = self.move_base.get_state()        
        result = False        
        if success and state == GoalStatus.SUCCEEDED:            
            # We made it!            
            result = True        
        else:            
            self.move_base.cancel_goal()        
            self.goal_sent = False        
            return result
    def read_csv(self):        
        thisdict = {}        
        with open("path_to_csv_file", "r") as csv_file:            
            csv_reader = csv.reader(csv_file,delimiter = ',')            
            for row in csv_reader:                
                thisdict[row[0]] = [row[1], row[2], row[3]]        
        return thisdict 
    def read_position(position_name):        
        dict_position = read_csv()        
        rospy.loginfo(dict_position[position_name])        
        return dict_position[position_name]
        
    def shutdown(self):
        stop_goal = MoveBaseGoal()
        self.move_base.send_goal(stop_goal)
        rospy.loginfo("Stop")

if __name__ == '__main__':
    try:
        robot_nav = RobotNavigation()
        robot_nav.go_to_location("location_name")
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")
