#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = """
Control Your Robot!
---------------------------
Moving around:
   w
a  s  d
   x

w : forward
x : reverse
a : turn left
d : turn right
q/e : rotate left/right
space key, s : stop
CTRL-C to quit
"""

move_bindings = {
    'w': (1, 0),    # forward
    'x': (-1, 0),   # reverse
    'a': (0, 1),    # turn left
    'd': (0, -1),   # turn right
    'q': (0, 1),    # rotate left
    'e': (0, -1),   # rotate right
    's': (0, 0)     # stop
}

speed = 0.2       # linear speed m/s
turn = 0.5        # angular speed rad/s

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    global settings
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('teleop_keyboard')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    try:
        print(msg)
        while not rospy.is_shutdown():
            key = getKey()
            twist = Twist()

            if key in move_bindings:
                linear = move_bindings[key][0]
                angular = move_bindings[key][1]

                twist.linear.x = linear * speed
                twist.angular.z = angular * turn

            elif key == ' ':
                twist.linear.x = 0
                twist.angular.z = 0
            else:
                continue

            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        pub.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == "__main__":
    main()