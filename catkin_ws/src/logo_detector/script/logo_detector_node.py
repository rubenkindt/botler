#!/usr/bin/env python2

import cv2
import copy
import numpy as np
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from logo_detector import LogoMatcher

class LogoFinder:
	def __init__(self):
		# Create a bridge to transform topics to CV images and back
		self.bridge = CvBridge()
		# Subscribe to camera feed
		self.image_sub = rospy.Subscriber('/gazebo_cam/image_raw', Image, self.callback)

		# Create publisher to publish detection id
		self.color_pub = rospy.Publisher('image_detection/beer_id', String, queue_size = 1)

		# Detector instance
		self.logo_matcher = LogoMatcher()

	def callback(self, data):
		# Try to convert the topic Image to an actual OpenCV image
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		try:
			# Use logo matching to determine the beer type
			beer_id = self.logo_matcher.logoMatch(cv_image)

			# Publish the beer_id
			self.color_pub.publish(str(beer_id))
		except:
			pass

if __name__ == '__main__':
	rospy.init_node('logo_detector')
	color = LogoFinder()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
