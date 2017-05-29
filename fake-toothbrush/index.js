
var name = 'My Fake Toothbrush';
var uuid = '04234f8e75b045259a32193d9c899d30';

var onMotorStateOn = function(e) {
    return navigator.bluetooth.requestDevice({
	filters: [{ services: [ uuid ], name: name }]
    }).then(function(device) {
	return device.gatt.connect();
    }).then(function(server) {
	return server.getPrimaryService(uuid);
    });
};
