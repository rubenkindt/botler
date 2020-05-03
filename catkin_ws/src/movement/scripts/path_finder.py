#!/usr/bin/env python
#Kwinten Vanlathem
import rospy
from std_msgs.msg import String

#Status defines
STATUS_TO_SCAN = 20
STATUS_TO_FRIDGE = 40
STATUS_TO_DROP = 60
STATUS_TO_IDLE = 70
#Location defines
OUDBEERSEL_LOCATION = 		["-1.9;1.6;1.57", "-1.65;1.6;1.57"]
DUVEL_LOCATION = 			["-1.05;1.6;1.57", "-0.75;1.6;1.57"]
GUST_LOCATION = 			["-0.15;1.6;1.57", "0.15;1.6;1.57"]
HOEGAARDEN_LOCATION = 		["1.05;1.6;1.57", "0.75;1.6;1.57"]
TRIPELKARMELIET_LOCATION = 	["1.65;1.6;1.57", "1.9;1.6;1.57"]
SCAN_LOCATION = "0;-1.57;-1.57"
DROP_LOCATION = "0.5;0;3.14"
IDLE_LOCATION = "0;0;0"
#Beer defines
OUDBEERSEL = 2
DUVEL = 1
GUST = 5
HOEGAARDEN = 3
TRIPELKARMELIET = 4
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
		elif(beer == HOEGAARDEN):						#current beer is not cold enough
			message = HOEGAARDEN_LOCATION[index]
			index = (index + 1) % len(HOEGAARDEN_LOCATION)
		elif(beer == OUDBEERSEL):				
			message = OUDBEERSEL_LOCATION[index]
			index = (index + 1) % len(OUDBEERSEL_LOCATION)
		elif(beer == TRIPELKARMELIET)
			message = TRIPELKARMELIET_LOCATION[index]
			index = (index + 1) % len(TRIPELKARMELIET_LOCATION)
		elif(beer == GUST)
			message = GUST_LOCATION[index]
			index = (index + 1) % len(GUST_LOCATION)
		else:
			return #No valid beer detected
	elif(status == STATUS_TO_DROP):
		message = DROP_LOCATION
	elif(status == STATUS_TO_IDLE):
		message = IDLE_LOCATION
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
