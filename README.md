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
