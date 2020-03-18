#!/usr/bin/env python
import cv2
import copy
import argparse
import numpy as np
import rospy
from std_msgs.msg import String

# parameters
CAMERA_BRIGHTNESS = 0
ROI_Y_U_LOC = 0.25              # ROI y upper location
ROI_X_B_LOC = 0.75              # ROI x bottom location
ROI_X_SIZE = 0.5
ROI_Y_SIZE = 0.5

# define the list of color boundaries
color_boundries = [
	([0, 120, 30], [5, 255, 255], 1),	# red low
	([160, 120, 30], [180, 255, 255], 1),       # red high
	([90, 120, 30], [120, 255, 255], 2),        # blue
	([50, 120, 30], [80, 255, 255], 3)   # green
]

cnt_areas = [0, 0, 0, 0]

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("camera", String, callback)

    rospy.spin()

def talker(color):
	pub = rospy.Publisher('chatter', String, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		color_str = str(color)
		rospy.loginfo(color_str)
		pub.publish(color_str)
 		rate.sleep()

def colorDetector(frame):
	# ROI size
	lu_y = int(frame.shape[0]*ROI_Y_U_LOC)
	rl_x = int(frame.shape[1]*ROI_X_B_LOC)
	left_upper = (rl_x - int(ROI_X_SIZE * frame.shape[1])-5, lu_y-5)
	right_lower = (rl_x + 5, int(ROI_Y_SIZE * frame.shape[0])+5 + lu_y+5)

	cv2.rectangle(frame, left_upper, right_lower, (255, 0, 255), 3)
	img_roi = frame[lu_y : (int(ROI_Y_SIZE * frame.shape[0])) + lu_y, (rl_x - int(ROI_X_SIZE * frame.shape[1])) : rl_x]
	img_roi_hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
	img_roi_grey = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)

	total_mask = np.zeros(img_roi_grey.shape, dtype=np.uint8)

	for (lower, upper, color) in color_boundries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply the mask
		mask = cv2.inRange(img_roi_hsv, lower, upper)
		total_mask = cv2.bitwise_or(total_mask, mask)

		_, contours, _ = cv2.findContours(copy.deepcopy(mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		if len(contours) != 0:
			# find the biggest countour (c) by the area
			c_max = max(contours, key = cv2.contourArea)
			x,y,w,h = cv2.boundingRect(c_max)

			if(cv2.contourArea(c_max) > cnt_areas[color]):
				cnt_areas[color] = cv2.contourArea(c_max)

		# cv2.imshow("images", img_roi)
		# cv2.imshow("mask", mask)
		# key = cv2.waitKey(0)

	return (cnt_areas.index(max(cnt_areas)))

if __name__ == '__main__':
	frame = listener()
	try:
		talker(frame)
	except rospy.ROSInterruptException:
		pass
