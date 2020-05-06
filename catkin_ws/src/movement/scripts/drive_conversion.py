#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Point, Quaternion
import tf
from math import radians, copysign, sqrt, pow, pi, atan2
from tf.transformations import euler_from_quaternion
import numpy as np


class drive_conversion():
    def __init__(self):
        rospy.init_node('drive_conversion', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=5)
	self.moveDone = rospy.Publisher('movement/status_ok', String, queue_size=5)
        self.sub = rospy.Subscriber('/path/driving_destination', String, self.driveTo)
        self.position = Point()
        self.move_cmd = Twist()
        self.r = rospy.Rate(10)
        self.tf_listener = tf.TransformListener()
        self.odom_frame = 'odom'

        try:
            self.tf_listener.waitForTransform(self.odom_frame, 'base_footprint', rospy.Time(), rospy.Duration(1.0))
            self.base_frame = 'base_footprint'
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            try:
                self.tf_listener.waitForTransform(self.odom_frame, 'base_link', rospy.Time(), rospy.Duration(1.0))
                self.base_frame = 'base_link'
            except (tf.Exception, tf.ConnectivityException, tf.LookupException):
                rospy.loginfo("Cannot find transform between odom and base_link or base_footprint")
                rospy.signal_shutdown("tf Exception")
        rospy.loginfo("geinitialiseerd")
        rospy.spin()
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())

    def driveTo(self, data):
        print(str(data.data))
        (self.position, rotation) = self.get_odom()
        last_rotation = 0
        linear_speed = 1
        angular_speed = 1
	(goal_x, goal_y, goal_z) = (str(data.data)).split(';')
	goal_x = int(goal_x)
	goal_y = int(goal_y)
	goal_z = int(goal_z)
        if goal_z > 180 or goal_z < -180:
            print("you input wrong z range.")
            self.shutdown()
        goal_z = np.deg2rad(goal_z)
        goal_distance = sqrt(pow(goal_x - self.position.x, 2) + pow(goal_y - self.position.y, 2))
        distance = goal_distance

        while distance > 0.05:
            (self.position, rotation) = self.get_odom()
            x_start = self.position.x
            y_start = self.position.y
            path_angle = atan2(goal_y - y_start, goal_x- x_start)

            if path_angle < -pi/4 or path_angle > pi/4:
                if goal_y < 0 and y_start < goal_y:
                    path_angle = -2*pi + path_angle
                elif goal_y >= 0 and y_start > goal_y:
                    path_angle = 2*pi + path_angle
            if last_rotation > pi-0.1 and rotation <= 0:
                rotation = 2*pi + rotation
            elif last_rotation < -pi+0.1 and rotation > 0:
                rotation = -2*pi + rotation
            self.move_cmd.angular.z = angular_speed * path_angle-rotation

            distance = sqrt(pow((goal_x - x_start), 2) + pow((goal_y - y_start), 2))
            self.move_cmd.linear.x = min(linear_speed * distance, 0.1)

            if self.move_cmd.angular.z > 0:
                self.move_cmd.angular.z = min(self.move_cmd.angular.z, 1.5)
            else:
                self.move_cmd.angular.z = max(self.move_cmd.angular.z, -1.5)

            last_rotation = rotation
            self.cmd_vel.publish(self.move_cmd)
            self.r.sleep()
        (self.position, rotation) = self.get_odom()
        while abs(rotation - goal_z) > 0.05:
            (self.position, rotation) = self.get_odom()
            if goal_z >= 0:
                if rotation <= goal_z and rotation >= goal_z - pi:
                    self.move_cmd.linear.x = 0.00
                    self.move_cmd.angular.z = 0.5
                else:
                    self.move_cmd.linear.x = 0.00
                    self.move_cmd.angular.z = -0.5
            else:
                if rotation <= goal_z + pi and rotation > goal_z:
                    self.move_cmd.linear.x = 0.00
                    self.move_cmd.angular.z = -0.5
                else:
                    self.move_cmd.linear.x = 0.00
                    self.move_cmd.angular.z = 0.5
            self.cmd_vel.publish(self.move_cmd)
            self.r.sleep()
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())
	self.moveDone.publish("Done")
    


    def get_odom(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
            rotation = euler_from_quaternion(rot)

        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return

        return (Point(*trans), rotation[2])


    def shutdown(self):
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)


if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            drive_conversion()

    except:
        rospy.loginfo("shutdown program.")
