#!/usr/bin/env python
import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np


class TemplateMatcher:
    def __init__(self):
        self.color_boundries = [
            	([0, 120, 30], [5, 255, 255], 1),	       # red low
            	([160, 120, 30], [180, 255, 255], 1),      # red high
            	([90, 120, 30], [120, 255, 255], 2),       # blue
            	([50, 120, 30], [80, 255, 255], 3)         # green
                ]
        self.cnt_areas = [0, 0, 0, 0]

    def templateMatch(self,frame = cv2.imread('big_Hoegaarden.png') ):

        duvel = cv2.imread('small_Duvel.png')
        omer = cv2.imread('small_Omer.png')
        hoe = cv2.imread('small_Hoegaarden.png')

        duvel=cv2.cvtColor(duvel,cv2.COLOR_BGR2RGB)
        omer=cv2.cvtColor(omer,cv2.COLOR_BGR2RGB)
        hoe=cv2.cvtColor(hoe,cv2.COLOR_BGR2RGB)

        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        if (frame is None):
            print("image img is none")
        if ( duvel is None):
            print("duvel template is none")
        if ( omer is None):
            print("omer template is none")
        if ( hoe is None):
            print("hoe template is none")
        templates=(duvel,omer,hoe)

        best_photo_nr=0 #see readme.md
        max=0
        teller=0
        for template in templates:
            teller += 1
            img2 = copy.deepcopy(frame)
            h, w = template.shape[0:2]
            res = cv2.matchTemplate(img2,template,cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print('maxValue',max_val)
            if max < max_val:
                max = max_val
                if max_val > 50000000:
                    best_photo_nr = teller

        #debug
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img2,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img2,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle("cv2.TM_CCOEFF")
        plt.show()
        #debug

        return best_photo_nr

t = TemplateMatcher()
nr = t.templateMatch()
print(nr)
