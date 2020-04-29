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
    name : '/master_control/control_status',
    messageType : 'std_msgs/String'
});

// Initalise string message
var master_news = new ROSLIB.Message({
    data : ""
});

// Publish the values, ordered by the web page buttons.
function pubMessage() {
    var order = "";

    // Get the value
    order = document.getElementById('HIER DIE BUTTON WAARDE NEMEN').value;

    // Set the appropriate values on the message object
    master_news.data = order;

    // Publish the message
    controlTopic.publish(master_news);
}

// Subscribe to informational topics
// Status
var status_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/master_control/status',
	messageType: 'std_msgs/String'
});
status_listener.subscribe(function(m) {
	document.getElementById("status_msg").innerHTML = m.data;
});

// Beer brand id
var brand_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/image_detection/brand_id',
	messageType: 'std_msgs/String'
});
brand_listener.subscribe(function(m) {
	document.getElementById("beerbrand_msg").innerHTML = m.data;
});

// Direction
var heading_listener = new ROSLIB.Topic({
	ros: ros,
	name: '/drive/cmd_dir',
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
	name: '/image_detection/temperature_id',
	messageType: 'std_msgs/String'
});
temperature_listener.subscribe(function(m) {
	document.getElementById("temperature_msg").innerHTML = m.data;
});
