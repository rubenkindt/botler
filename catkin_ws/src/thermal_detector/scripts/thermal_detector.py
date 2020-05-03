#!/usr/bin/env python2

import cv2
import numpy as np
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Detector:
    def __init__(self):
        # The HSV defenition of a "cold or hot" drink
        self.color_boundries = [
            	([0, 120, 30], [5, 255, 255], 2),          # "hot" low
            	([160, 120, 30], [180, 255, 255], 2),      # "hot" high
            	([90, 120, 30], [120, 255, 255], 1)]       # "cold"

    def detect_temp(self, frame):
        c_largest_area = 0
        c_largest = None
        c_tem = None

        # Converting the BGR image to HSV
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for (lower, upper, tem) in self.color_boundries:
            # Create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")

            # Find the colors within the specified boundaries and apply the mask
            mask = cv2.inRange(img_hsv, lower, upper)

            # Get the bottle(s) contours
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

            # If there are any contours (so if there are any cold or hot bottles in the screen)
            if len(contours) != 0:
                # Find the biggest countour (c) by the area
                c_max = max(contours, key = cv2.contourArea)

                # The largest contour has to have a minimum size
                if (cv2.contourArea(c_max) > c_largest_area):
                    c_largest_area = cv2.contourArea(c_max)
                    c_largest = c_max
                    c_tem = tem

        if(c_largest_area > 1000):
            return (cv2.boundingRect(c_largest), c_tem)
        else:
            return ((0,0,0,0), 0)

class Thermal_detector:
	def __init__(self):
        # Create a bridge to transform topics to CV images and back
		self.bridge = CvBridge()

        # Subscribe to camera feed
		self.image_sub = rospy.Subscriber('/gazebo_cam/image_raw', Image, self.callback)

		# Create publisher to publish detection id
		self.color_pub = rospy.Publisher('thermal_detector/detection_id', String, queue_size = 1)

        # Create publisher to publish bounding boxes
		self.image_pub = rospy.Publisher('thermal_detector/cv_image', Image, queue_size=1)

		# Detector instance
		self.detector = Detector()

	def callback(self, data):
        # Try to convert the topic Image to an actual OpenCV image
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

        # Detect the color (temperature) of the bottle in the image and place a bounding box around it.
		(x,y,w,h), temp_id = self.detector.detect_temp(cv_image)

        # Publish the temperature id (0 = hot, 1 = cold)
		self.color_pub.publish(str(temp_id))

        # Draw a bounding box around the cold bottle
		cv2.rectangle(cv_image, (x,y), (x+w,y+h), (255,0,0), 2)

        # Try to convert the image back to a topic and publish said topic
		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		except CvBridgeError as e:
			print(e)

if __name__ == '__main__':
    # Create a ROS node called 'thermal_detector'
	rospy.init_node('thermal_detector')

    # Make an instance of the thermal_detector class
	temperature = Thermal_detector()

    # Keep the node spun up
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
