#!/usr/bin/env python
#Kwinten Vanlathem
import rospy
from std_msgs.msg import String

#Status defines
STATUS_TO_SCAN = 20
STATUS_TO_FRIDGE = 40
STATUS_TO_DROP = 60
#Location defines
SCAN_LOCATION = "10;20;0" #x=10, y=20, ori=posX
DUVEL_LOCATION = ["50;20;180", "50;19;180", "50;18;180"]
ORVAL_LOCATION = ["50;25;180", "50;26;180"]
DROP_LOCATION = "10;25;0"
#Beer defines
DUVEL = 1
ORVAL = 2
#global variables
status = 0
beer = 0
log = 0
driveto = 0
index = 0

def callbackStatus(data):
	global status
	status = int(data.data)
	move()

def callbackBeer(data):
	global beer, index
	beer = int(data.data)
	index = 0 #reset index each time a new beer is detected
	move()

def move():
	global status, beer, log, driveto, index
	if(status == STATUS_TO_SCAN): #drive to scanning position
		message = SCAN_LOCATION
	elif(status == STATUS_TO_FRIDGE):
		if(beer == DUVEL):
			message = DUVEL_LOCATION[index]
			index = (index + 1) % len(DUVEL_LOCATION) 	#move index to next beer for next time
		elif(beer == ORVAL):							#current beer is not cold enough
			message = ORVAL_LOCATION[index]
			index = (index + 1) % len(ORVAL_LOCATION)
		else:
			return #No valid beer detected
	elif(status == STATUS_TO_DROP):
		message = DROP_LOCATION
	else:
		return #In this status, no movement is required
	log.publish(message)
	driveto.publish(message)

def main():
	global log, driveto
	rospy.init_node('pathFinder', anonymous=True)

	rospy.Subscriber('status', String, callbackStatus)
	rospy.Subscriber('image_detection/detection_id', String, callbackBeer)
	log = rospy.Publisher("logFile", String, queue_size=10)
	driveto = rospy.Publisher("driveTo", String, queue_size=10)

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

if __name__ == '__main__':
	main()
