#!/usr/bin/env python3
import rospy
import tf2_ros

rospy.init_node("tf_delay_relay_safe")

tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer)
tf_broadcaster = tf2_ros.TransformBroadcaster()

DELAY = rospy.Duration(0.01)  # 10 ms
last_stamp = rospy.Time(0)

rate = rospy.Rate(50)  # 50 Hz
while not rospy.is_shutdown():
    try:
        trans = tf_buffer.lookup_transform("map", "odom", rospy.Time(0), rospy.Duration(0.1))
        delayed_stamp = trans.header.stamp - DELAY
        if delayed_stamp > last_stamp:
            trans.header.stamp = delayed_stamp
            tf_broadcaster.sendTransform(trans)
            last_stamp = delayed_stamp
    except tf2_ros.TransformException:
        pass
    rate.sleep()