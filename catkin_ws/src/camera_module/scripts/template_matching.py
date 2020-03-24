#!/usr/bin/env python
import copy
import argparse
import rospy
import cv2
import numpy as np
from std_msgs.msg import String

from matplotlib import pyplot as plt
def templateMatch(	frame = cv2.imread('/home/user/botler/catkin_ws/src/camera_module/scripts/big_logo.png')):
	template = cv2.imread('/home/user/botler/catkin_ws/src/camera_module/scripts/small_logo.png')
	frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	template=cv2.cvtColor(template,cv2.COLOR_BGR2HSV)

	if (frame is None):
		print("image img is none")
	if ( template is None):
		print("image template is none")
	img2 = copy.deepcopy(frame)
	h, w = template.shape[0:2]

	res = cv2.matchTemplate(img2,template,cv2.TM_CCOEFF)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

	top_left = max_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)
	cv2.rectangle(img2,top_left, bottom_right, 255, 2)
	plt.subplot(121),plt.imshow(res,cmap = 'gray')
	plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(img2,cmap = 'gray')
	plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
	plt.suptitle("cv2.TM_CCOEFF")
	plt.show()
templateMatch()
