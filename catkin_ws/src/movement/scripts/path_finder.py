#!/usr/bin/env python
#Kwinten Vanlathem
import rospy
from std_msgs.msg import String

status = 0
STATUS_TO_SCAN = 1
STATUS_TO_FRIDGE = 3
THRESH = 0.5
SCAN_LOCATION = (10, 20)
beer = 0
DUVEL = 1
DUVEL_LOCATION = (50,20)
ORVAL = 2
ORVAL_LOCATION = (50,25)

log = 1

def callbackStatus(data):
	global status
	status = int(data.data)

def callbackBeer(data):
	global beer
	beer = int(data.data)

def callbackLidar(data):
	global status
	global beer
	global log
	line = data.data.split(";")
	currentPos = (int(line[0]), int(line[1]))

	message = "StayPut"

	if(status == STATUS_TO_SCAN): #drive to scanning position
		message = calculateDirection(currentPos, SCAN_LOCATION)
	elif(status == STATUS_TO_FRIDGE):
		if(beer == DUVEL) :
			message = calculateDirection(currentPos, DUVEL_LOCATION)
		elif(beer == ORVAL) :
			message = calculateDirection(currentPos, ORVAL_LOCATION)
	log.publish(message)

def calculateDirection(currentPos, targetPos):
	if(abs(currentPos[0] - targetPos[0]) > THRESH):
		if(currentPos[0] < targetPos[0]):
			return "1" #drive to positive x
		else:
			return "2" #drive to negative x
	elif(abs(currentPos[1] - targetPos[1]) > THRESH):
		if(currentPos[1] < targetPos[1]):
			return "3" #drive to positive y
		else:
			return "4" #drive to negative y
	else: #reached target pos
			return "5" #stop driving

def main():
	rospy.init_node('pathFinder', anonymous=True)

	rospy.Subscriber('status', String, callbackStatus)
	rospy.Subscriber('image_detection/detection_id', String, callbackBeer)
	rospy.Subscriber('curPos', String, callbackLidar)
	global log
	log = rospy.Publisher("logFile", String, queue_size=10)

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

if __name__ == '__main__':
	main()
