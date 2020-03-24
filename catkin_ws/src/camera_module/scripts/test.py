import cv2

cam=cv2.VideoCapture(0)
img=cam.read()
if (img==None):
  print("hello")

img2= cv2.imread("big_logo.jpg",0)
if (img2==None):
    print("none")
