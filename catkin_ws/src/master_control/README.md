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
* 55: Pick the bottle up
* 60: Drive to dropoff location
* 65: Put the bottle down
* 70: Driving to idle position

How to transfer to another state:
* 10 to 20: Start commando on webinterface
* 20 to 30: Arriving at scan location
* 30 to 40: Identifying glass
* 40 to 50: Arriving at bottle
* 50 to 40: Temperature is too hot
* 50 to 55: Temperature is good
* 55 to 60: Bottle has been picked up
* 60 to 65: Arriving at dropoff location
* 65 to 70: Bottle has been put down
* 70 to 10: Arriving at idle location
* Anything to 70: Return home commando from webinterface
