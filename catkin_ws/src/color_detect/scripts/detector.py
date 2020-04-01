#!/usr/bin/env python2
import cv2
import copy
import numpy as np

class Detector:
    def __init__(self):
        self.color_boundries = [
            	([0, 120, 30], [5, 255, 255], 1),	   # red low
            	([160, 120, 30], [180, 255, 255], 1),      # red high
            	([90, 120, 30], [120, 255, 255], 2),       # blue
            	([50, 120, 30], [80, 255, 255], 3)         # green
                ]

    def detect_color(self, frame):
	cnt_areas = [0, 0, 0, 0]
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for (lower, upper, color) in self.color_boundries:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")

            # find the colors within the specified boundaries and apply the mask
            mask = cv2.inRange(img, lower, upper)

            contours, _ = cv2.findContours(copy.deepcopy(mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) != 0:
                # find the biggest countour (c) by the area
                c_max = max(contours, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(c_max)

                if(cv2.contourArea(c_max) > cnt_areas[color]):
                    cnt_areas[color] = cv2.contourArea(c_max)

        return (cnt_areas.index(max(cnt_areas)), (x,y,w,h))
