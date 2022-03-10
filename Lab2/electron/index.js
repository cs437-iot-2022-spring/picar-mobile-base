document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.10.20";   // the IP address of your Raspberry PI

const net = require('net');

const client = net.createConnection({ port: server_port, host: server_addr }, () => {
    // 'connect' listener.
    console.log('connected to server!');
});

client.on('data', (data) => {
    console.log(data.toString());
    check_status(data);
    // client.end();
});

client.on('end', () => {
    console.log('disconnected from server');
});

function check_response(){

  client.on('data', (data) => {
      document.getElementById("bluetooth").innerHTML = data;
      console.log(data.toString());
      client.end();
      client.destroy();
  });

  client.on('end', () => {
      console.log('disconnected from server');
  });
}

// function client(){
//
//     const net = require('net');
//     var input = document.getElementById("message").value;
//
//     const client = net.createConnection({ port: server_port, host: server_addr }, () => {
//         // 'connect' listener.
//         console.log('connected to server!');
//         // send the message
//         client.write(`${input}\r\n`);
//     });
//
//     // get the data from the server
//     client.on('data', (data) => {
//         document.getElementById("bluetooth").innerHTML = data;
//         console.log(data.toString());
//         client.end();
//         client.destroy();
//     });
//
//     client.on('end', () => {
//         console.log('disconnected from server');
//     });
//
//     return client;
// }

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";

        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";

        send_data("68");
    }
}

// reset the key to the start state
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";

    client.write("STOP");
}

function send_data(data){
  client.write(data);
}

function check_status(data){
  data = data.toString();
  data_arr = data.split(',');


  // Always send status in order DATA_RECEIVED, ACK MESSAGE BACK, DIRECTION, SPEED, TEMPERATURE
  document.getElementById("ret_message").innerHTML = data_arr[1];
  document.getElementById("direction").innerHTML = data_arr[2];
  document.getElementById("speed").innerHTML = data_arr[3];
  document.getElementById("temperature").innerHTML = data_arr[4];


}

// update status data at least every 50ms
setInterval(function(){
    client.write("STATUS");
}, 1000);


function update_data(){
    var input = document.getElementById("message").value;

    client.write("ACK" + `${input}`);
}
