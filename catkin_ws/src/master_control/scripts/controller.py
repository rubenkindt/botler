#!/usr/bin/env python

import rospy
from std_msgs.msg import String

#Status defines
STATUS_STARTUP = 0
STATUS_IDLE = 10
STATUS_TO_SCAN = 20
STATUS_SCANNING = 30
STATUS_TO_FRIDGE = 40
STATUS_TEMPCHECK = 50
STATUS_TO_DROP = 60
STATUS_TO_IDLE = 70

#global status storage
status = 20
publisher = 0

#debug global
log = 0

def callbackArrive(data): #Robot has arrived at intended location; driving complete
	global status
	if(status == STATUS_TO_SCAN):
		status = STATUS_SCANNING
	elif(status == STATUS_TO_FRIDGE):
		status = STATUS_TEMPCHECK
	elif(status == STATUS_TO_DROP):
		status = STATUS_TO_IDLE
	elif(status == STATUS_TO_IDLE):
		status = STATUS_IDLE
	publish()
	
def callbackStart(data): #A glass has been identified, drive to a bottle of the matching beer brand
	global status
	if(status == STATUS_IDLE):
		status = STATUS_TO_SCAN
	publish()
	
def callbackBeer(data): #A glass has been identified, drive to a bottle of the matching beer brand
	global status
	if(status == STATUS_SCANNING):
		status = STATUS_TO_FRIDGE
	publish()
	
def callbackTemp(data): #Temperature has been messured, decide on whether to accept it
	global status
	if(status == STATUS_TEMPCHECK):
		if(int(data.data) == 1):	#Good temperature
			status = STATUS_TO_DROP
		else:	#Too hot or failed to messure, try new bottle
			status = STATUS_TO_FRIDGE
	publish()
	
def publish():
	global status, publisher, log
	publisher.publish(str(status))
	log.publish("New status: " + str(status))
	
def main():
	global log, publisher
	rospy.init_node('master_control', anonymous=True)

	rospy.Subscriber('control_start', String, callbackStart)
	rospy.Subscriber('movement/status_ok', String, callbackArrive)
	rospy.Subscriber('image_detection/beer_id', String, callbackBeer)
	rospy.Subscriber('image_detection/thermal_id', String, callbackTemp)
	
	log = rospy.Publisher("logFile", String, queue_size=10)
	publisher = rospy.Publisher("master_status", String, queue_size=10)

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

if __name__ == '__main__':
	main()
