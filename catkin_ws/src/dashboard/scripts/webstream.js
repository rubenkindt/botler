var ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
});


ros.on('connection', function() {
    console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
    console.log('Connection to websocket server closed.');
});

var controlTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/dashboard/control_start',
    messageType : 'std_msgs/String'
});

var master_news = new ROSLIB.Message({
    data : ""
});

function pub_message(command) {
    console.log(command)
    master_news.data = command;
    controlTopic.publish(master_news);
}

// Subscribe to informational topics
// Status
var status_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/master_status',
	messageType: 'std_msgs/String'
});
status_listener.subscribe(function(m) {
	var status = ""
	switch(parseInt(m.data)) {
    case 0:
     	status = "Currently information available"
     	break;
	case 10:
		status = "Idle wait, ready for opperation";
		break;
	case 20:
		status = "Driving to the bar to scan a beerglass";
		break;
	case 30:
		status = "Scanning the glass";
		break;
	case 40:
		status = "Driving to the fridge in order to fetch the appropriate bottle";
		break;
	case 50:
		status = "Checking the temperature of the bottle";
		break;
	case 60:
		status = "Return to the glass ";
		break;
	case 70:
		status = "Return to the home position";
		break;
	}
	document.getElementById("status_msg").innerHTML = status;
});

// Beer brand id
var beer_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/image_detection/beer_id',
	// /image_detection/beer_id
	messageType: 'std_msgs/String'
});
beer_listener.subscribe(function(m) {
	console.log(m)
	var brand = ""
	switch(parseInt(m.data)) {
    case 0:
     	brand = "No beer detected"
     	break;
	case 1:
		brand = "Duvel";
		break;
	case 2:
		brand = "Geuze";
		break;
	case 3:
		brand = "Hoegaarden";
		break;
	case 4:
		brand = "Karmeliet";
		break;
	case 5:
		brand = "Gust";
		break;
	}
	document.getElementById("beerbrand_msg").innerHTML = brand;
});

// Direction
var heading_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/path/driving_destination',
	messageType: 'std_msgs/String'
});
heading_listener.subscribe(function(m) {
	document.getElementById("direction_msg").innerHTML = m.data;
});

// Temperature
var temperature_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/image_detection/thermal_id',
	messageType: 'std_msgs/String'
});
temperature_listener.subscribe(function(m) {
	var temp = ""
	switch(parseInt(m.data)) {
    case 0:
      temp = "No bottle detected"
      break;
	case 1:
		temp = "Cold";
		break;
	case 2:
		temp = "Warm";
		break;
	}
	console.log(temp)
	document.getElementById("temperature_msg").innerHTML = temp;
});
