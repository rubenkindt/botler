#!/usr/bin/env python
import rospy
from datetime import datetime
from std_msgs.msg import String

logfile = open("log.txt", "w")

def callback(data):
	global logfile
	print(datetime.today().strftime("%H:%M:%S %d/%m/%Y") + ": " + data.data)
	logfile.write(datetime.today().strftime("%H:%M:%S %d/%m/%Y") + ": " + data.data + "\n")

def listener():

    rospy.init_node('logFileWriter', anonymous=True)

    rospy.Subscriber('logFile', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
	listener()
