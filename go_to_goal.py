#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import cos, sin, sqrt
class GoToGoal():
    def __init__(self):
        rospy.init_node('go_to_goal_node', anonymous=False, log_level=rospy.DEBUG)
        rospy.loginfo("To stop Turtlebot press CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/navi' , Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber('odom', Odometry, self.odom_callback)
        self.goal_pose_x = 0
        self.goal_pose_y = 0
        self.current_pose_x = 0
        self.current_pose_y = 0
        self.current_theta = 0
        self.vel_x = 0
        self.tol = 0.1
        self.move_cmd = Twist()
        rospy.wait_for_message("odom", Odometry) # wait for odometry data
    def odom_callback(self, odom_data):
        self.current_pose_x = odom_data.pose.pose.position.x
        self.current_pose_y = odom_data.pose.pose.position.y
        orientation_q = odom_data.pose.pose.orientation # orientation data
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]         
	    # change orientation data to radius
	    (roll, pitch, yaw) = euler_from_quaternion(orientation_list) 
        self.current_theta = yaw # currently radius of robot

    def go_to_goal(self, vel_x):
        self.move_cmd.linear.x = vel_x  # set velocity
        while not rospy.is_shutdown():
            if self.check_stop():
                self.shutdown()
                break
            else:
                self.cmd_vel_pub.publish(self.move_cmd)
    def set_goal(self, distance, tol):
        self.goal_pose_x = self.current_pose_x + (distance * cos(self.current_theta))
        self.goal_pose_y = self.current_pose_y + (distance * sin(self.current_theta))
        self.tol = tol
        rospy.logdebug(" Current Pose : " + str([self.current_pose_x,self.current_pose_y]))
        rospy.logdebug("Move Distance : " + str(distance) + " m with TOL : " + str(tol) + "m")
        rospy.logdebug("    Goal Pose : " + str([self.goal_pose_x,self.goal_pose_y]))

    def check_stop(self):
        delta_x = self.goal_pose_x - self.current_pose_x
        delta_y = self.goal_pose_y - self.current_pose_y
        error = sqrt(delta_x ** 2 + delta_y ** 2)
        rospy.logdebug(error)
        if error <= self.tol:
           return True
        else:
           return False
    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

if __name__ == "__main__":
    try:
        go_to_goal = GoToGoal()
	 # Set go at 1m ahead with 0.05m tolerant
        go_to_goal.set_goal(1, 0.05)
	 # Start moving forward at speed 0.1 m/s 
        go_to_goal.go_to_goal(0.1)
	
    except rospy.ROSInterruptException:
        rospy.loginfo("GoToGoal Forward node terminated")
