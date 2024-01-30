#!/usr/bin/env python

'''
ackermann_drive_joyop.py:
    A ros joystick teleoperation script for ackermann steering based robots
'''

__author__ = 'George Kouros'
__license__ = 'GPLv3'
__maintainer__ = 'George Kouros'
__email__ = 'gkourosg@yahoo.gr'

import rospy
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import Joy
import sys

class AckermannDriveJoyop:
    

    def __init__(self, args):
        if len(args)==1 or len(args)==2:
            self.max_speed = float(args[0])
            self.max_steering_angle = float(args[len(args)-1])
            cmd_topic = 'ackermann_cmd'
        elif len(args) == 3:
            self.max_speed = float(args[0])
            self.max_steering_angle = float(args[1])
            cmd_topic = '/' + args[2]
        else:
            self.max_speed = 10
            self.max_steering_angle = 0.7
            cmd_topic = 'ackermann_cmd'
        self.rate=rospy.Rate(10)

        self.speed = 0
        self.steering_angle = 0
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.drive_pub = rospy.Publisher('/vesc/ackermann_cmd', AckermannDriveStamped,
                                         queue_size=1)
        rospy.loginfo('ackermann_drive_joyop_node initialized')
        self.stop=0
        while not rospy.is_shutdown():
            if self.stop==1:
                break
            else:
                self.pub_callback()
                self.rate.sleep()
                
            

    def joy_callback(self, joy_msg):
        self.joy_msg=joy_msg
        self.speed = joy_msg.axes[1] * self.max_speed
        self.steering_angle = joy_msg.axes[3] * self.max_steering_angle
        if joy_msg.buttons[0]==1:
            self.finalize()
            self.stop=1
            


    def pub_callback(self):
        ackermann_cmd_msg = AckermannDriveStamped()
        ackermann_cmd_msg.drive.speed = self.speed
        ackermann_cmd_msg.drive.steering_angle = self.steering_angle
        self.drive_pub.publish(ackermann_cmd_msg)
        self.print_state()

    def print_state(self):
        sys.stderr.write('\x1b[2J\x1b[H')
        rospy.loginfo('\x1b[1M\r'
                      '\033[34;1mSpeed: \033[32;1m%0.2f m/s, '
                      '\033[34;1mSteering Angle: \033[32;1m%0.2f rad\033[0m',
                      self.speed, self.steering_angle)

    def finalize(self):
        rospy.loginfo('Halting motors, aligning wheels and exiting...')
        ackermann_cmd_msg = AckermannDriveStamped()
        ackermann_cmd_msg.drive.speed = 0
        ackermann_cmd_msg.drive.steering_angle = 0
        self.drive_pub.publish(ackermann_cmd_msg)
        
        sys.exit()

if __name__ == '__main__':
    rospy.init_node('ackermann_drive_joyop_node')
    joyop = AckermannDriveJoyop(sys.argv[1:len(sys.argv)])
    
