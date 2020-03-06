#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def talker():
	#list of topics
	drive = rospy.Publisher("drive", String, queue_size=10)	
	grabber = rospy.Publisher("grabber", String, queue_size=10)
	lidar = rospy.Publisher("lidar", String, queue_size=10)
	camera = rospy.Publisher("camera", String, queue_size=10)
	ultrasonic = rospy.Publisher("ultrasonic", String, queue_size=10)
	log = rospy.Publisher("logFile", String, queue_size=10)

	rospy.init_node('talker', anonymous=True)
	while not rospy.is_shutdown():
		line = raw_input("Command: ")
		linesplit = line.split(" ")
	
		if(linesplit[0] == "exit"):
			break
		elif(linesplit[0] == "drive"):	#turn left 90, stop, forward, forward 25
			drive.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "grabber"): #open, close
			grabber.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "lidar"):	#getposition
			lidar.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "camera"):	#get color, get glass, get beer
			camera.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "ultrasonic"):	#get distance
			ultrasonic.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "log"):	#get distance
			log.publish(" ".join(linesplit[1:]))
			#add more topics
		else:
			print(linesplit[0] + " is not a valid topic")

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
