#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

class MoveForward():
    def __init__(self):
        rospy.init_node('move_forward_node', anonymous=False)
        rospy.loginfo("To stop Turtlebot press CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel_pub =  rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.move_forward(0.05, 0.0)
        
    def move_forward(self, vel_x, vel_z):
        r = rospy.Rate(10)
        move_cmd = Twist()
        move_cmd.linear.x = vel_x
        move_cmd.angular.z = vel_z
        while not rospy.is_shutdown():
            self.cmd_vel_pub.publish(move_cmd)
            r.sleep()

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel_pub.publish(Twist())
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

 
if __name__ == '__main__':
    try:
        MoveForward()
    except:
        rospy.loginfo("MoveForward node terminated.")
