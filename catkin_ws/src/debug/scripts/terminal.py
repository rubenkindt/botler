#!/usr/bin/env python
#Kwinten Vanlathem
import rospy
from std_msgs.msg import String

def talker():
	#list of topics
	log = rospy.Publisher("logFile", String, queue_size=10)
	status = rospy.Publisher("status", String, queue_size=10)
	detection_id = rospy.Publisher("image_detection/detection_id", String, queue_size=10)
	arrival = rospy.Publisher("arrival", String, queue_size=10)
	temp = rospy.Publisher("temp", String, queue_size=10)

	rospy.init_node('talker', anonymous=True)
	while not rospy.is_shutdown():
		line = raw_input("Command: ")
		linesplit = line.split(" ")

		if(linesplit[0] == "exit"):
			break
		elif(linesplit[0] == "log"):
			log.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "status"):
			status.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "detection_id"):
			detection_id.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "arrival"):
			arrival.publish(" ".join(linesplit[1:]))
		elif(linesplit[0] == "temp"):
			temp.publish(" ".join(linesplit[1:]))
			#add more topics
		else:
			print(linesplit[0] + " is not a valid topic")

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
