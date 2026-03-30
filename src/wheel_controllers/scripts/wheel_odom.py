#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Vector3
import tf
import math

# ----------------------------
# Robot parameters
# ----------------------------
WHEEL_RADIUS = 0.0485     # meters
WHEEL_SEPARATION = 0.31   # meters

# ----------------------------
# State variables
# ----------------------------
x = 0.0
y = 0.0
theta = 0.0
last_time = None
last_left = 0.0
last_right = 0.0

# ----------------------------
# Callback for joint states
# ----------------------------
def callback(js):
    global x, y, theta, last_time, last_left, last_right

    try:
        left_idx = js.name.index('left_wheel_joint')
        right_idx = js.name.index('right_wheel_joint')
    except ValueError:
        return

    left_pos = js.position[left_idx]
    right_pos = js.position[right_idx]

    now = rospy.get_rostime()

    if last_time is None:
        last_time = now
        last_left = left_pos
        last_right = right_pos
        return

    dt = (now - last_time).to_sec()
    if dt <= 0:
        return

    # Wheel displacements
    d_left = left_pos - last_left
    d_right = right_pos - last_right

    # Linear and angular velocities
    v = WHEEL_RADIUS * (d_right + d_left) / (2.0 * dt)
    w = WHEEL_RADIUS * (d_right - d_left) / (WHEEL_SEPARATION * dt)

    # Integrate pose
    dx = v * math.cos(theta) * dt
    dy = v * math.sin(theta) * dt
    dtheta = w * dt

    x += dx
    y += dy
    theta += dtheta

    # ----------------------------
    # Publish odometry message with delay
    # ----------------------------
    odom = Odometry()
    odom.header.stamp = now 
    odom.header.frame_id = 'odom'
    odom.child_frame_id = 'base_link'

    odom.pose.pose.position.x = x
    odom.pose.pose.position.y = y
    odom.pose.pose.position.z = 0.0
    odom.pose.pose.orientation = Quaternion(*tf.transformations.quaternion_from_euler(0, 0, theta))

    odom.twist.twist.linear = Vector3(v, 0.0, 0.0)
    odom.twist.twist.angular = Vector3(0.0, 0.0, w)

    pub.publish(odom)

    # ----------------------------
    # Broadcast TF from odom -> base_link with same delay
    # ----------------------------
    """br.sendTransform(
        (x, y, 0.0),
        tf.transformations.quaternion_from_euler(0, 0, theta),
        now ,       
        'base_link',
        'odom'
    )"""

    # Update last values
    last_time = now
    last_left = left_pos
    last_right = right_pos

# ----------------------------
# ROS node initialization
# ----------------------------
rospy.init_node('wheel_odom')
pub = rospy.Publisher('/odom', Odometry, queue_size=10)
rospy.Subscriber('/joint_states', JointState, callback)

# TF broadcaster
br = tf.TransformBroadcaster()

rospy.loginfo("Wheel odometry node started with timestamp delay of 10 ms")
rospy.spin()
