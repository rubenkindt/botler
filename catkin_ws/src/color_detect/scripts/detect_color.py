#!/usr/bin/env python
import cv2
import copy
import numpy as np
import rospy

from detector import Detector

# parameters
CAMERA_BRIGHTNESS = 0
ROI_Y_U_LOC = 0.25              # ROI y upper location
ROI_X_B_LOC = 0.75              # ROI x bottom location
ROI_X_SIZE = 0.5
ROI_Y_SIZE = 0.5

class Color_detector:
	__init__(self):
		# Subscribe to raspicam feed
        self.subscriber = rospy.Subscriber('camera/image', cameraFeed, self.callback)

        # Create publisher to publish bounding boxes
        self.color_pub = rospy.Publisher('color_detector/detection', colorDetect, queue_size=1)

        # Detector instance
        self.detector = Detector()

	def callback(data):
		cv_image = self.str2cv(data.image)
		color_id = self.detector.detect_color(cv_image)
		self.color_pub.publish(color_id)

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
