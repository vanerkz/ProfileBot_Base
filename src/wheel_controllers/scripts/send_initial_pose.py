#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from cartographer_ros_msgs.srv import StartTrajectory, FinishTrajectory
from cartographer_ros_msgs.srv import StartTrajectory, StartTrajectoryRequest

import rospkg

class WheelController:
    def __init__(self):
        self.state = 0

        # Subscriber
        self.sub = rospy.Subscriber("initialpose", PoseWithCovarianceStamped, self.poseAMCL_callback)

        # Wait for services
        rospy.loginfo("Waiting for Cartographer services...")
        rospy.wait_for_service('start_trajectory')
        rospy.wait_for_service('finish_trajectory')
        self.client_start = rospy.ServiceProxy('start_trajectory', StartTrajectory)
        self.client_finish = rospy.ServiceProxy('finish_trajectory', FinishTrajectory)
        rospy.loginfo("Connected to services.")

        # Get configuration paths
        rospack = rospkg.RosPack()
        self.config_dir = rospack.get_path('wheel_controllers') + '/configuration_files'
        self.config_basename = 'backpack_2d_localization.lua'

    def poseAMCL_callback(self, msg):
        rospy.loginfo(f"x: {msg.pose.pose.position.x}")
        rospy.loginfo(f"y: {msg.pose.pose.position.y}")
        rospy.loginfo(f"w: {msg.pose.pose.orientation.w}")
        rospy.loginfo(f"z: {msg.pose.pose.orientation.z}")

        try:
            # Create a new StartTrajectoryRequest each time
            req = StartTrajectoryRequest()
            req.use_initial_pose = True
            req.configuration_directory = self.config_dir
            req.configuration_basename = self.config_basename
            req.initial_pose = msg.pose.pose

            # If first time, relative_to_trajectory_id = 0
            # For subsequent times, you can still reference 0
            req.relative_to_trajectory_id = 0

            resp_start = self.client_start(req)
            rospy.loginfo("start_trajectory called successfully with new pose!")

            # Optional: track number of resets
            self.state += 1

        except rospy.ServiceException as e:
            rospy.logerr(f"Failed to call start_trajectory: {e}")


if __name__ == "__main__":
    rospy.init_node("getpose", anonymous=True)
    node = WheelController()
    rospy.spin()
