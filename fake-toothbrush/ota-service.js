// A. Apvrille - Fortinet

var util = require('util');
var bleno = require('bleno');
var BlenoPrimaryService = bleno.PrimaryService;

// uncertain
var flashCharacteristic = new bleno.Characteristic({ // Flash
    uuid: '92cf8666cf79448dbba2bc9aa89174d2',
    properties: ['write'],
    onWriteRequest: flashWrite
});

var firmwareCharacteristic = new bleno.Characteristic({ // Firmware Revision String
    uuid : '8fc2d14efbfa41da8d27971b6a25934e',
    properties : ['write'],
    onWriteRequest : firmwareWrite
});
    
function OtaService() {
    OtaService.super_.call(this, {
	uuid: 'c05fc343c0764a9795d3f6d3e92a2799',
	characteristics: [ flashCharacteristic, firmwareCharacteristic ],
    });
}

// uncertain
function flashWrite(data, offset, withoutResponse, callback) {
    console.log('Flash write: ', data.toString('hex')); 
    callback(this.RESULT_SUCCESS);
}

// uncertain
function firmwareWrite(data, offset, withoutResponse, callback) {
    console.log('Firmware write: ', data.toString('hex'));
    callback(this.RESULT_SUCCESS);
}

util.inherits(OtaService, BlenoPrimaryService);

module.exports = OtaService;
