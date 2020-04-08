#!/usr/bin/env python
import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np

class TemplateMatcher:
    def __init__(self):

        self.BFmatcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)


    def templateMatch(self,frame = cv2.imread('/home/user/botler/catkin_ws/src/template_matcher/script/pics/big_Duvel.png', 1)):
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if (frame is None):
            print("image img is none")

        orb = cv2.ORB_create()
        kp_orb_frame, desciptor_frame = orb.detectAndCompute(frame, None)
        #des_frame_f32 = np.float32(desciptor_frame)

        dir="pics/"
        duvel = cv2.imread(dir+'small_Duvel.png', 1)
        omer = cv2.imread(dir+'small_Omer.png', 1)
        hoe = cv2.imread(dir+'small_Hoegaarden.png', 1)

        if (duvel is None):
            print("duvel template is none")
        if (omer is None):
            print("omer template is none")
        if (hoe is None):
            print("hoe template is none")

        duvel=cv2.cvtColor(duvel, cv2.COLOR_BGR2GRAY)
        omer=cv2.cvtColor(omer, cv2.COLOR_BGR2GRAY)
        hoe=cv2.cvtColor(hoe, cv2.COLOR_BGR2GRAY)



        kp1, des1 = orb.detectAndCompute(frame,None)
        kp2, des2 = orb.detectAndCompute(duvel,None)

        index_params = dict(algorithm = 1, trees=5 )
        search_param = dict(checks = 50)
        flann = cv2.FlannBasedMatcher(index_params, search_param)

        des1_32 = np.float32(des1)
        des2_32 = np.float32(des2)
        matches = flann.knnMatch(des1_32,des2_32,k=2)
        best_photo_nr=len(matches)

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
        print(best_photo_nr)
        print(top_left, bottom_right)
        return best_photo_nr, top_left, bottom_right

t = TemplateMatcher()
nr = t.templateMatch()
print(nr)
