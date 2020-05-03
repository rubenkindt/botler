#!/usr/bin/env python2

from __future__ import print_function
import cv2
import copy
import numpy as np
import rospy
from std_msgs.msg import String
import roslib
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from detector import Detector

# parameters
CAMERA_BRIGHTNESS = 0
ROI_Y_U_LOC = 0.25              # ROI y upper location
ROI_X_B_LOC = 0.75              # ROI x bottom location
ROI_X_SIZE = 0.5
ROI_Y_SIZE = 0.5

class Color_detector:
	def __init__(self):
		# Subscribe to raspicam feed
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback)

		# Create publisher to publish bounding boxes
		self.color_pub = rospy.Publisher('color_detector/det_id', String)
		self.image_pub = rospy.Publisher("color_detector/cv_image", Image)

		# Detector instance
		self.detector = Detector()

	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		color_id, (x,y,w,h) = self.detector.detect_color(cv_image)
		self.color_pub.publish(str(color_id))
		cv2.rectangle(cv_image, (x,y), (x+w,y+h), (255,0,0), 2)

		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		except CvBridgeError as e:
			print(e)

	def str2cv(self, image_string):
		""" Convert image string to OpenCv image """
		np_arr = np.fromstring(image_string, np.uint8)
		return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

if __name__ == '__main__':
	rospy.init_node('color_detector')
	color = Color_detector()

	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
