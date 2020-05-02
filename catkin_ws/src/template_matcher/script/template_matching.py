#!/usr/bin/env python
#https://ai-facets.org/robust-logo-detection-with-opencv/
import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np

class TemplateMatcher:
    def __init__(self):

        self.dectector = cv2.ORB_create(nfeatures=2000)

        dir="src/template_matcher/script/pics/"
        self.duvel = cv2.imread(dir+'big_Duvel.png')
        self.geuze = cv2.imread(dir+'Geuze.png')
        self.hoe = cv2.imread(dir+'big_Hoegaarden.png')
        self.karm = cv2.imread(dir+'karmeliet.png')
        self.gust = cv2.imread(dir+'Gust.png')

        self.namen=["duvel","geuze","hoegaarden","karmeliet","gust"]

        self.model_Features=[self.duvel, self.geuze, self.hoe, self.karm, self.gust]

        for teller,img in enumerate(self.model_Features):
            if (img is None):
                print("foto",str(teller),"is none")

        self.model_Features = [self.getFeatures(self.duvel),self.getFeatures(self.geuze),self.getFeatures(self.hoe),self.getFeatures(self.karm),self.getFeatures(self.gust) ]
        #for img in self.model_Features:
        #    self.model_Features.append(self.getFeatures(img))

        self.MIN_MATCH_COUNT=10

    def getFeatures(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detector = self.dectector
        kps, descs = detector.detectAndCompute(gray, None)
        return kps, descs, img.shape[:2][::-1]

    def detectFeatures(self,img, train_features):
        train_kps, train_descs, shape = train_features
        # get features from input image
        kps, descs, _ = self.getFeatures(img)
        # check if keypoints are extracted
        if not kps:
            return None
        # now we need to find matching keypoints in two sets of descriptors (from sample image, and from current image)
        # knnMatch uses k-nearest neighbors algorithm for that
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(train_descs, descs, k=2)
        good = []
        # apply ratio test to matches of each keypoint
        # idea is if train KP have a matching KP on image, it will be much closer than next closest non-matching KP,
        # otherwise, all KPs will be almost equally far
        if len(matches)==0:
            return None
        for m, n in matches:
            if m is None or n is None:
                continue
            if m.distance < 0.8 * n.distance:
                good.append([m])
        # stop if we didn't find enough matching keypoints
        if len(good) < 0.1 * len(train_kps):
            return None
        # estimate a transformation matrix which maps keypoints from train image coordinates to sample image
        src_pts = np.float32([train_kps[m[0].queryIdx].pt for m in good
                              ]).reshape(-1, 1, 2)
        dst_pts = np.float32([kps[m[0].trainIdx].pt for m in good
                              ]).reshape(-1, 1, 2)
        return len(good)
        #m, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if m is not None:
            # apply perspective transform to train image corners to get a bounding box coordinates on a sample image
            scene_points = cv2.perspectiveTransform(np.float32([(0, 0), (0, shape[0] - 1), (shape[1] - 1, shape[0] - 1), (shape[1] - 1, 0)]).reshape(-1, 1, 2), m)
            rect = cv2.minAreaRect(scene_points)
            # check resulting rect ratio knowing we have almost square train image
            #if rect[1][1] > 0 and 0.8 < (rect[1][0] / rect[1][1]) < 1.2:
            return len(good)
        return None


    def templateMatch(self,frame):
        if frame is None:
            return
        img = self.hoe
        train_features = self.getFeatures(img)

        matches_k = self.detectFeatures(frame, self.model_Features[0])
        matches_p = self.detectFeatures(frame, self.model_Features[1])
        matches_hoe = self.detectFeatures(frame, self.model_Features[2])

        matches=[matches_k,matches_p,matches_hoe]

        max=0
        best_photo_nr=0
        for teller,match in enumerate(matches):
            if match>self.MIN_MATCH_COUNT:
                    if max < match:
                        max = match
                        best_photo_nr=teller+1
        print(best_photo_nr)

        top_left = (0,0)
        bottom_right = (1,1)#(top_left[0] + w, top_left[1] + h)

        return best_photo_nr
