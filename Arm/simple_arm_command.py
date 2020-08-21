#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import actionlib
import geometry_msgs

def simple_arm_command():
  ## First initialize moveit_commander and rospy.
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('simple_arm_command',anonymous=True)

  ## Instantiate a MoveGroupCommander object.  This object is an interface
  ## to one group of joints.  In this case the group refers to the joints of
  ## arm. This interface can be used to plan and execute motions on arm.
  arm_group = moveit_commander.MoveGroupCommander("arm")

  ## Action clients to the ExecuteTrajectory action server.
  arm_client = actionlib.SimpleActionClient('execute_trajectory',
    moveit_msgs.msg.ExecuteTrajectoryAction)
  arm_client.wait_for_server()
  rospy.loginfo('Execute Trajectory server is available for arm')

  while not rospy.is_shutdown():
    ## Set a named joint configuration as the goal to plan for a move group.
    ## Named joint configurations are the robot poses defined 
    ## via MoveIt! Setup Assistant.
    arm_group.set_named_target("vertical")

    ## Plan to the desired joint-space goal using the default planner (RRTConnect).
    arm_plan_home = arm_group.plan()
    ## Create a goal message object for the action server.
    arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
    ## Update the trajectory in the goal message.
    arm_goal.trajectory = arm_plan_home

    ## Send the goal to the action server.
    arm_client.send_goal(arm_goal)
    arm_client.wait_for_result()

    arm_group.set_named_target("resting")
    arm_plan_pregrasp = arm_group.plan()
    arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
    arm_goal.trajectory = arm_plan_pregrasp
    arm_client.send_goal(arm_goal)
    arm_client.wait_for_result()

    arm_group.set_named_target("ready_to_pick")
    arm_plan_pregrasp = arm_group.plan()
    arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
    arm_goal.trajectory = arm_plan_pregrasp
    arm_client.send_goal(arm_goal)
    arm_client.wait_for_result()

    ## Cartesian Paths
    ## ^^^^^^^^^^^^^^^
    ## You can plan a cartesian path directly by specifying a list of waypoints
    ## for the end-effector to go through.
    waypoints = []
    # start with the current pose
    current_pose = arm_group.get_current_pose()
    rospy.sleep(0.5)
    current_pose = arm_group.get_current_pose()

    ## create linear offsets to the current pose
    new_eef_pose = geometry_msgs.msg.Pose()

    # Manual offsets because we don't have a camera to detect objects yet.
    new_eef_pose.position.x = current_pose.pose.position.x
    new_eef_pose.position.y = current_pose.pose.position.y
    new_eef_pose.position.z = current_pose.pose.position.z + 0.05

    # Retain orientation of the current pose.
    new_eef_pose.orientation = copy.deepcopy(current_pose.pose.orientation)

    waypoints.append(new_eef_pose)
    waypoints.append(current_pose.pose)
    ## We want the cartesian path to be interpolated at a resolution of 1 cm
    ## which is why we will specify 0.01 as the eef_step in cartesian
    ## translation.  We will specify the jump threshold as 0.0, effectively
    ## disabling it.
    fraction = 0.0
    for count_cartesian_path in range(0,3):
      if fraction < 1.0:
        (plan_cartesian, fraction) = arm_group.compute_cartesian_path(
                                     waypoints,   # waypoints to follow
                                     0.01,        # eef_step
                                     0.0)         # jump_threshold
      else:
        break

    arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
    arm_goal.trajectory = plan_cartesian
    arm_client.send_goal(arm_goal)
    arm_client.wait_for_result()

    arm_group.set_named_target("resting")
    arm_plan_postgrasp = arm_group.plan()
    arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
    arm_goal.trajectory = arm_plan_postgrasp
    arm_client.send_goal(arm_goal)
    arm_client.wait_for_result()

    arm_group.set_named_target("ready_to_place")
    arm_plan_place = arm_group.plan()
    arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
    arm_goal.trajectory = arm_plan_place
    arm_client.send_goal(arm_goal)
    arm_client.wait_for_result()

    arm_group.set_named_target("vertical")
    arm_plan_vertical = arm_group.plan()
    arm_goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
    arm_goal.trajectory = arm_plan_vertical

    arm_client.send_goal(arm_goal)
    arm_client.wait_for_result()
    
  ## When finished shut down moveit_commander.
  moveit_commander.roscpp_shutdown()


if __name__=='__main__':
  try:
    simple_arm_command()
  except rospy.ROSInterruptException:
    pass
