#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#/*
#    @year:        2020/2021
#    @author:      Sekomer
#    @touch:       aksoz19@itu.edu.tr
#*/

import numpy as np
import math
import cv2
import sys
import time
import rospy
import os


from sensor_msgs.msg import LaserScan

center_x, center_y = 400, 400
desired_fps = 15

laser = None
FI = 360/1440


def sin(angle):
    return math.sin(math.radians(angle))

def cos(angle):
    return math.cos(math.radians(angle))

def lidar_data(data):
    global laser

    laser = np.array(data.ranges[-1:0:-1])
    #laser = np.array(data.ranges)
    
    laser[laser > 25] = 0
    
    if len(sys.argv) > 1:
        laser *= int(sys.argv[1])
    else:
        laser *= 50
    
    
    d = np.zeros((center_x * 2, center_y * 2))
    d = cv2.circle(d, (center_x,center_y), 7,	255, 1)

    for index, item in enumerate(laser):
        x = int(sin(index * FI - 90) * item) + center_x
        y = int(cos(index * FI - 90) * item) + center_y
        
        if (0 <= x < (center_x*2)) and (0 <= y < (center_y*2)):
            d[x][y] = 255

    cv2.imshow("LIDAR", d)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        rospy.signal_shutdown("TERMINATING FAKE RVIZ")


if __name__ == "__main__":
    rospy.init_node('fake_rviz', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, lidar_data)

    rospy.spin()
