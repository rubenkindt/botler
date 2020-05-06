# Botler logo detector
## logo_detection.py

Through the use of an ORB detector we will determine keypoints in our image.
If enough keypoints overlap with our logo the corresponding logo ID will be published

*	0 when no logo is detected
*	1 when the Duvel logo is detected
*	2 when the Geuze logo is detected
*	3 when the Hoegaarden logo is detected
*	4 when the Karmeliet logo is detected
*	5 when the Gust logo is detected

## Subscribers
* /gazebo_cam/image_raw - this is the image we receive
* /master_status - this gives us a status value to determine if the detector should publish his values

## Publisher
* /image_detection/beer_id - this publishes the beer_id
