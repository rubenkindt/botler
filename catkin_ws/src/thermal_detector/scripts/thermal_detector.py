#!/usr/bin/env python2
import cv2
import numpy as np
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Detector:
    def __init__(self):
        # The HSV defenition of a "cold" drink
        self.cold_lower = np.array([90, 120, 30])
        self.cold_upper = np.array([120, 255, 255])

    def detect_temp(self, frame):
        # Converting the BGR image to HSV
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Show only the cold bottle(s)
        mask = cv2.inRange(img_hsv, self.cold_lower, self.cold_upper)

        # Get the bottle(s) contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # If there are any contours (so if there are any cold bottles in the screen)
        if len(contours) != 0:
            # Find the biggest countour (c) by the area
            c_max = max(contours, key = cv2.contourArea)

            # The largest contour has to have a minimum size
            if (cv2.contourArea(c_max) > 1000):
                # Get the bounding box information
                x,y,w,h = cv2.boundingRect(c_max)
                return (True, (x,y,w,h))

        return (False, (0,0,0,0))

class Thermal_detector:
	def __init__(self):
        # Create a bridge to transform topics to CV images and back
		self.bridge = CvBridge()

        # Subscribe to camera feed
		self.image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback)

		# Create publisher to publish detection id
		self.color_pub = rospy.Publisher('thermal_detector/det_id', String, queue_size = 1)

        # Create publisher to publish bounding boxes
		self.image_pub = rospy.Publisher("thermal_detector/cv_image", Image, queue_size=1)

		# Detector instance
		self.detector = Detector()

	def callback(self, data):
        # Try to convert the topic Image to an actual OpenCV image
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

        # Detect the color (temperature) of the bottle in the image and place a bounding box around it.
		temp_id, (x,y,w,h) = self.detector.detect_temp(cv_image)

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
