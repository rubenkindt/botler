#!/usr/bin/env python
#https://docs.opencv.org/4.2.0/dc/dc3/tutorial_py_matcher.html
import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np

class TemplateMatcher:
    def __init__(self):

        self.orb = cv2.ORB_create()
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


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

        _,self.des_duvel= self.orb.detectAndCompute(self.duvel, None)
        _,self.des_omer= self.orb.detectAndCompute(self.omer, None)
        _,self.des_hoe= self.orb.detectAndCompute(self.hoe, None)


    def templateMatch(self,frame = cv2.imread('/home/user/botler/catkin_ws/src/template_matcher/script/pics/big_Duvel.png', 1)):
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if (frame is None):
            print("image img is none")

        kpts1, des_frame = self.orb.detectAndCompute(frame, None)

        max=0
        teller=0
        best_photo_nr=0
        descriptors=[self.des_duvel,self.des_omer, self.des_hoe]
        for des in descriptors:
            teller+=1

            matches = self.bf.match(des,des_frame)
            matches = sorted(matches, key = lambda x:x.distance)
            good=[]
            #for m,n in matches:
            #    if m.distance < 0.9*n.distance:
            #        good.append(m)

            print(len(matches),teller)
            MIN_MATCH_COUNT=100
            if len(matches)>MIN_MATCH_COUNT:
                if max < len(matches):
                    max = len(matches)
                    best_photo_nr=teller

        top_left = (50,50)
        bottom_right = (100,100)#(top_left[0] + w, top_left[1] + h)

        return best_photo_nr, top_left, bottom_right

#t = TemplateMatcher()
#nr = t.templateMatch()
#print(nr)
