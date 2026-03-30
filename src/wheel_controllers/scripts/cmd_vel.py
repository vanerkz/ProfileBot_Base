#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

# WHEEL PARAMETERS
WHEEL_RADIUS = 0.0485  # meters
WHEEL_SEPARATION = 0.31  # meters

# Publishers for each wheel
pub_left = None
pub_right = None

def cmd_vel_cb(msg):
    """Convert cmd_vel to individual wheel velocities"""
    v = msg.linear.x
    w = msg.angular.z

    # Differential drive formulas
    vel_left = (v - (WHEEL_SEPARATION/2.0) * w) / WHEEL_RADIUS
    vel_right = (v + (WHEEL_SEPARATION/2.0) * w) / WHEEL_RADIUS

    # Publish to wheel velocity controllers
    pub_left.publish(Float64(vel_left))
    pub_right.publish(Float64(vel_right))

def main():
    global pub_left, pub_right

    rospy.init_node('diff_drive_controller')

    # Publishers to your velocity controllers
    pub_left = rospy.Publisher('/left_wheel_velocity_controller/command', Float64, queue_size=10)
    pub_right = rospy.Publisher('/right_wheel_velocity_controller/command', Float64, queue_size=10)

    # Subscribe to cmd_vel
    rospy.Subscriber('/cmd_vel', Twist, cmd_vel_cb)

    rospy.loginfo("Differential drive node running. Listening to /cmd_vel...")
    rospy.spin()

if __name__ == '__main__':
    main()
    
