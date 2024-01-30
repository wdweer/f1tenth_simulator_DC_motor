#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import time
rospy.init_node('voltage_publisher')

volt_pub1=rospy.Publisher('/steer_bot/rear_right_dc_motor/supply_voltage', Float32, queue_size=1)
volt_pub2=rospy.Publisher('/steer_bot/rear_right_dc_motor/command', Float32, queue_size=1)
volt_pub3=rospy.Publisher('/steer_bot/rear_left_dc_motor/supply_voltage', Float32, queue_size=1)
volt_pub4=rospy.Publisher('/steer_bot/rear_left_dc_motor/command', Float32, queue_size=1)

x=Float32()
x.data=1000
r=rospy.Rate(10)
y=Float32()
y.data=0
start_time=time.time()

while not rospy.is_shutdown():
    if time.time()-start_time < 10:
       volt_pub1.publish(x)
       volt_pub2.publish(x)
       volt_pub3.publish(x)
       volt_pub4.publish(x)
       
    else:
       volt_pub1.publish(y)
       volt_pub2.publish(y)
       volt_pub3.publish(y)
       volt_pub4.publish(y)
    r.sleep()