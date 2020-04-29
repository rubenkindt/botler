# movement package
## path_finder.py
checks if the global program is in a drive to somewhere state, and if so, determines where to go based on feedback from diffrent toppics

subscribes to 'status' to determine whether to drive to scanning location, beer location or dropoff location

subscribes to 'image-detection/detection-id' to determine to which beer brand to drive

publisches to 'driveTo' to send a string to the wheels node with a target x, y and orientation in the form of "x;y;o"
