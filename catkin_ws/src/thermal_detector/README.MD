# Thermal detector package
## Subscribers
'/usb_cam/image_raw' (Image) -> the usb_cam image feed

## Publishers
'thermal_detector/detection_id' (String) -> this returns whether or not the largest bottle (largest contour) in the screen is cold
(0 if no bottle detected, 1 if cold bottle detected, 2 if hot bottle detected)

'thermal_detector/cv_image' (Image) -> this shows an image of the cold bottle detection
