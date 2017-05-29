// A. Apvrille - Fortinet

var bleno = require('bleno');
var DeviceInfoService = require('./deviceinfo-service');
var GenericAccessService = require('./genericaccess-service');
var BeamService = require('./beam-service');
var OtaService = require('./ota-service');

console.log('----- Fake Toothbrush BLE device ------');

var deviceInfoService = new DeviceInfoService();
var genericAccessService = new GenericAccessService();
var beamService = new BeamService();
var otaService = new OtaService();

bleno.on('stateChange', function(state) {
    // console.log('on -> stateChange: ' + state);

    if (state === 'poweredOn') {
	var name = 'My Fake Toothbrush';
	bleno.startAdvertising(name, [beamService.uuid], function(error) {
	    console.log('[' + (error ? '-' + error : '+') + '] startAdvertising');
	});
    } else {
	console.log('[-] Stop advertising');
	bleno.stopAdvertising();
    }
});

// Notify the console that we've accepted a connection
bleno.on('accept', function(clientAddress) {
    console.log("Accepted connection from address: " + clientAddress);
});

bleno.on('advertisingStart', function(error) {
   // console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

    if (!error) {
	bleno.setServices([genericAccessService, deviceInfoService, beamService, otaService ], function(error){
	    console.log('[' + (error ? '-' + error : '+') + '] setServices');
	});
    }
});


