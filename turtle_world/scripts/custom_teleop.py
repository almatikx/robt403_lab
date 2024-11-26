#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import curses
import sys

def send_command(stdscr):
    rospy.init_node('arrow_key_teleop')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(10)

    # Initialize curses
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.addstr(0, 0, "Use arrow keys to control the robot:")
    stdscr.addstr(1, 0, "UP: Forward, DOWN: Backward, LEFT: Turn Left, RIGHT: Turn Right")
    stdscr.addstr(2, 0, "Press 'q' to quit.")

    twist = Twist()

    try:
        while not rospy.is_shutdown():
            key = stdscr.getch()
            if key == curses.KEY_UP:  # Up arrow key
                twist.linear.x = 0.5
                twist.angular.z = 0.0
            elif key == curses.KEY_DOWN:  # Down arrow key
                twist.linear.x = -0.5
                twist.angular.z = 0.0
            elif key == curses.KEY_LEFT:  # Left arrow key
                twist.linear.x = 0.0
                twist.angular.z = 0.5
            elif key == curses.KEY_RIGHT:  # Right arrow key
                twist.linear.x = 0.0
                twist.angular.z = -0.5
            elif key == ord('q'):  # Quit
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                pub.publish(twist)
                break
            else:
                # Stop the robot for any other key
                twist.linear.x = 0.0
                twist.angular.z = 0.0

            pub.publish(twist)
            rate.sleep()
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C
        rospy.loginfo("Exiting teleoperation control...")
    finally:
        # Ensure the terminal is reset to its normal state
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
        rospy.loginfo("Robot stopped. Terminal restored.")

if __name__ == "__main__":
    try:
        curses.wrapper(send_command)
    except rospy.ROSInterruptException:
        rospy.loginfo("ROS node terminated.")
        sys.exit(0)

