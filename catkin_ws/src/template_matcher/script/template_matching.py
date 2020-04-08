#!/usr/bin/env python
import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np

class TemplateMatcher:
    def __init__(self):
        self.duvel = cv2.imread('src/template_matcher/script/pics/small_Duvel.png', 1)
        self.omer = cv2.imread('src/template_matcher/script/pics/small_Omer.png', 1)
        self.hoe = cv2.imread('src/template_matcher/script/pics/small_Hoegaarden.png', 1)

        if (self.duvel is None):
            print("duvel template is none")
        if (self.omer is None):
            print("omer template is none")
        if (self.hoe is None):
            print("hoe template is none")

        self.duvel=cv2.cvtColor(self.duvel, cv2.COLOR_BGR2RGB)
        self.omer=cv2.cvtColor(self.omer, cv2.COLOR_BGR2RGB)
        self.hoe=cv2.cvtColor(self.hoe, cv2.COLOR_BGR2RGB)

    def templateMatch(self,frame):
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        if (frame is None):
            print("image img is none")

        templates=(self.duvel,self.omer,self.hoe)

        best_photo_nr=0 #see readme.md
        max=0
        teller=0

        for template in templates:
            teller += 1
            img2 = copy.deepcopy(frame)
            h, w = template.shape[0:2]
            res = cv2.matchTemplate(img2,template,cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # print('maxValue',max_val)
            if max < max_val:
                max = max_val
                if max_val > 50000000:
                    best_photo_nr = teller

        #debug
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # cv2.rectangle(img2,top_left, bottom_right, 255, 2)
        # plt.subplot(121),plt.imshow(res,cmap = 'gray')
        # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(img2,cmap = 'gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # plt.suptitle("cv2.TM_CCOEFF")
        # plt.show()
        #debug

        return best_photo_nr, top_left, bottom_right

# t = TemplateMatcher()
# nr = t.templateMatch()
# print(nr)
