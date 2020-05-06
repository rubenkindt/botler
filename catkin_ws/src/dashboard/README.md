# Botler dashboard
## Python HTTP server
Hosts robot control dashboard.

### Packages
Makes use of web_video_server package to live stream the robots camera view.
Makes use of rosbridge_suite suite package (and especially rosbridge server and websocket) to communicate with ros topics.
Roslib is used to create, publish and subscribe to topics within javascript.

### Dashboard functionality:
* Stream live camera feed.
* Display live speed, heading.
* Display measured temperature.
* Display image recognition (recognised beer brand) including snapshot of the recognised item.
* Display current status of the robot.
* Control the robots state (Turn on, Turn off, Return to base).
