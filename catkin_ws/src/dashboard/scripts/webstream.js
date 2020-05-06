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

// Initalise string message
var master_news = new ROSLIB.Message({
    data : ""
});

// Publish the values, ordered by the web page buttons.
function pub_message(command) {
	console.log("op een knopje geduwd!")
    // var order = "";
    // console.log(order)
    // // Get the value
    // order = document.getElementById('control_msg').value;
    // console.log(order)
    console.log(command)
    // Set the appropriate values on the message object
    master_news.data = command;

    // Publish the message
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
	document.getElementById("status_msg").innerHTML = m.data;
});

// Beer brand id
var totaalgeenbier_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/drive/test',
	// /image_detection/beer_id
	messageType: 'std_msgs/String'
});
totaalgeenbier_listener.subscribe(function(m) {
	console.log(m)
	document.getElementById("beerbrand_msg").innerHTML = m.data;
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

// Speed
var speed_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/drive/cmd_vel',
	messageType: 'std_msgs/String'
});
speed_listener.subscribe(function(m) {
	document.getElementById("speed_msg").innerHTML = m.data;
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
