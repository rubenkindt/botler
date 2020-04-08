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

        self.duvel=cv2.cvtColor(self.duvel, cv2.COLOR_BGR2GRAY)
        self.omer=cv2.cvtColor(self.omer, cv2.COLOR_BGR2GRAY)
        self.hoe=cv2.cvtColor(self.hoe, cv2.COLOR_BGR2GRAY)

        self.orb = cv2.ORB_create()
        self.BFmatcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        flann_index_kdtree = 1
        index_params = dict(algorithm = flann_index_kdtree, trees=5 )
        search_param = dict(checks = 50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_param)


    def templateMatch(self,frame):
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if (frame is None):
            print("image img is none")

        kp_orb_frame, desciptor_frame = self.orb.detectAndCompute(frame, None)
        #des_frame_f32 = np.float32(desciptor_frame)


        templates=(self.duvel,self.omer,self.hoe)

        best_photo_nr=0 #see readme.md
        max=0
        teller=0
        for template in templates:
            teller += 1
            img2 = copy.deepcopy(frame)
            h, w = template.shape[0:2]
            kp_orb_template, desciptor_template = self.orb.detectAndCompute(template, None)
            #des_templ_f32 = np.float32(desciptor_template)
            #matches = self.BFmatcher.match(desciptor_template, desciptor_frame)
            #matches = self.flann.knnMatch(des_templ_f32, des_frame_f32, 2)
            matches = self.flann.knnMatch(desciptor_template, desciptor_frame, k=2)
            good=[]
            for m,n in matches:
                if m.distance < 0.9*n.distance:
                    good.appende(m)
            if len(good) > 15:
                if max < len(good):
                    max=len(good)
                    best_photo_nr=teller

        #debug
        top_left = (50,50)
        bottom_right = (100,100)#(top_left[0] + w, top_left[1] + h)

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
