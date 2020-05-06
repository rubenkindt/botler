#!/usr/bin/env python
#https://docs.opencv.org/4.2.0/d1/de0/tutorial_py_feature_homography.html
import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np

class TemplateMatcher:
    def __init__(self):

        self.sift = cv2.xfeatures2d.SIFT_create()
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)


        dir = "src/template_matcher/script/pics/"
        #dir = "pics/"
        self.duvel = cv2.imread(dir+'small_Duvel.png', 1)
        self.omer = cv2.imread(dir+'small_Omer.png', 1)
        self.hoe = cv2.imread(dir+'small_Hoegaarden.png', 1)


        if (self.duvel is None):
            print("duvel template is none")
        if (self.omer is None):
            print("omer template is none")
        if (self.hoe is None):
            print("hoe template is none")

        self.duvel=cv2.cvtColor(self.duvel, cv2.COLOR_BGR2GRAY)
        self.omer=cv2.cvtColor(self.omer, cv2.COLOR_BGR2GRAY)
        self.hoe=cv2.cvtColor(self.hoe, cv2.COLOR_BGR2GRAY)

        _,self.des_duvel= self.sift.detectAndCompute(self.duvel, None)
        _,self.des_omer= self.sift.detectAndCompute(self.omer, None)
        _,self.des_hoe= self.sift.detectAndCompute(self.hoe, None)


    def templateMatch(self,frame = cv2.imread('/home/user/botler/catkin_ws/src/template_matcher/script/pics/big_Duvel.png', 1)):
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if (frame is None):
            print("image img is none")

        kpts1, des_frame = self.sift.detectAndCompute(frame, None)

        max=0
        teller=0
        best_photo_nr=0
        descriptors=[self.des_duvel,self.des_omer, self.des_hoe]
        for des in descriptors:
            teller+=1

            matches = self.flann.knnMatch(des,des_frame,k=2)
            matches = sorted(matches, key = lambda x:x.distance)
            good=[]
            for m,n in matches:
                if m.distance < 0.9*n.distance:
                    good.append(m)
                    print("works")

            print(len(matches),teller)
            MIN_MATCH_COUNT=100
            if len(matches)>MIN_MATCH_COUNT:
                if max < len(matches):
                    max = len(matches)
                    best_photo_nr=teller

        top_left = (50,50)
        bottom_right = (100,100)#(top_left[0] + w, top_left[1] + h)

        return best_photo_nr, top_left, bottom_right

t = TemplateMatcher()
nr = t.templateMatch()
print(nr)
