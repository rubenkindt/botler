# Botler - a robot butler

## Installation
* move into the botler repository (cd botler)
* move into the catkin workspace (cd catkin_ws)
* initialise the git modules (git submodules init)
* update the git modules (git submodules update)

Because we use a custom world with a custom robot a few changes have to be made to the turtlebot3 package.
These changes were not implementable into our git repository because of the use of submodules.

* move into the turtlebot3 description folder (cd src/turtlebot3/turtlebot3_description/urdf)
* edit the files "turtlebot3_burger.gazebo.xacro" and "turtlebot3_burger.urdf.xacro" to add the content of the camera in gazebo.txt file in the root of our project

Now you can build the project

* catkin_make

## Execution
* go back to the catkin workspace (cd botler/catkin_ws)
* source devel/setup.sh
* choose the turtlebot robot (export TURTLEBOT3_MODEL=burger)
* define to location of the gazebo files (export GAZEBO_MODEL_PATH=~/botler/catkin_ws/src/botler_sim/models/:$GAZEBO_MODEL_PATH)

Now we will start the different nodes, everytime you open a new terminal don't forget to "source devel/setup.sh"

### General setup
* start a roscore : "roscore"
* the gazebo world : "roslaunch botler_sim the_bar.launch"

### Vision
* the logo detector : "rosrun logo_detector logo_detector_node.py"
* the thermal detector : "rosrun thermal_detector thermal_detector.py"

### Movement
* start our pathfinder : "rosrun movement path_finder.py"
* start the drive converter : "rosrun movement drive_conversion.py"

### Web Dashboard
* start the web video server : "rosrun web_video_server web_video_server"
* start a bridge between the websocket and ros : "roslaunch rosbridge_server rosbridge_websocket.launch"
* To start the webserver first navigate to its folder : "cd src/dashboard/scripts/"
* start the webserver itself : "python -m SimpleHTTPServer"

### Master Controll
* and lastly start the master controll node : "rosrun master_control controller.py"
