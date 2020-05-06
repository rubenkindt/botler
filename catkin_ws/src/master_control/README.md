# master_control package
## controller.py
Used to determin the current state of the global program.

Publishes on: 
* master_status

Listens to:
* dashboard/control_start
* movement/status_ok
* image_detection/beer_id
* image_detection/thermal_id

Current state:
* 10: Idle wait, ready for opperation
* 20: Driving to the scan location
* 30: Scanning the glass
* 40: Identifying glass
* 50: Arriving at bottle
* 60: Drive to dropoff location
* 70: Driving to idle position

How to transfer to another state:
* 10 to 20: Start commando on webinterface
* 20 to 30: Arriving at scan location
* 30 to 40: Identifying glass
* 40 to 50: Arriving at bottle
* 50 to 40: Temperature is too hot
* 50 to 60: Temperature is good
* 60 to 70: Arriving at dropoff location
* 70 to 10: Arriving at idle location
