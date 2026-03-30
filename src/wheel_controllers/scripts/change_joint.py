#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

rospy.init_node("hold_joints")

joints = [
    "joint_0","joint_1","joint_2","joint_3","joint_4",
    "joint_5","joint_6","joint_7","joint_8","joint_9"
]

# Publishers for each joint's position controller
pubs = {j: rospy.Publisher(f"/{j}_position_controller/command", Float64, queue_size=10) for j in joints}

rate = rospy.Rate(50)  # 50 Hz

# Default joint positions
joint_positions = {j: 0 for j in joints}  # initial pose

print("Press Enter to input new joint positions, or Ctrl+C to exit.")

while not rospy.is_shutdown():
    # Publish current positions
    for j, pub in pubs.items():
        pub.publish(joint_positions[j])
    rate.sleep()

    # Non-blocking check for Enter press
    try:
        # Python 3 input (blocking), but we only call it occasionally
        if rospy.get_time() % 5 < 0.05:  # every ~5 seconds, prompt
            user_input = input("Enter new positions for all 10 joints (comma-separated):\n")
            if user_input.strip():  # if not empty
                values = [float(v) for v in user_input.split(",")]
                if len(values) == len(joints):
                    joint_positions = dict(zip(joints, values))
                else:
                    print(f"Please enter exactly {len(joints)} values.")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Invalid input:", e)