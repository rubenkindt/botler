# Thermal detector package
## thermal_detector.py

Dependant on the largest contour in the image we will determine if the bottle is cold (blue), or hot (red).

## Subscribers
'/gazebo/image_raw' (Image) -> the gazebo_cam image feed
'/master_status' (String) -> tells us if we should publish our results

## Publishers
'thermal_detector/detection_id' (String) -> this returns whether or not the largest bottle (largest contour) in the screen is cold
(0 if no bottle detected, 1 if cold bottle detected, 2 if hot bottle detected)

'thermal_detector/cv_image' (Image) -> this shows an image of the cold bottle detection
