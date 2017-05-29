// A. Apvrille - Fortinet

var util = require('util');
var bleno = require('bleno');
var BlenoPrimaryService = bleno.PrimaryService;

var motorSpeedCharacteristic =  new bleno.Characteristic({ // motor speed
    uuid: '833da694-51c5-4418-b4a9-3482de840aa8',
    properties: ['read', 'write'],
    onReadRequest: speedRead,
    onWriteRequest: speedWrite
});

var autoquadrantCharacteristic = new bleno.Characteristic({
    uuid: '19dc94fa7bb342489b2d1a0cc6437af5',
    properties: ['read','write'],
    onReadRequest: autoquadrantRead,
    onWriteRequest: autoquadrantWrite
});

var buzzCharacteristic = new bleno.Characteristic({
    uuid: 'ca048932cec74b82a086f384c3270df5',
    properties: ['read','write'],
    onReadRequest: buzzRead,
    onWriteRequest: buzzWrite
});

var timeCharacteristic = new bleno.Characteristic({
    uuid: '3530b2ca94f84a1d96beaa76d808c131',
    properties: ['read','write'],
    onReadRequest: timeRead,
    onWriteRequest: timeWrite
});

function BeamService() {
    //console.log('Creating Beam Service');
    BeamService.super_.call(this, {
	uuid: '04234f8e75b045259a32193d9c899d30',
	characteristics: [ new bleno.Characteristic({ // Brush color
	    uuid: '0971ed14e92949f9925f81f638952193',
	    properties: ['read'],
	    value : colorRead,
	}),
			   new bleno.Characteristic({ // hardware revision
	                       uuid: 'cf16681d78fd431f965ec7b7b5d1d147',
	                       properties: ['read'],
	                       value : new Buffer('06', 'hex')  // 2.6
			   }),
			   new bleno.Characteristic({ // motor state
	                       uuid: '267b09fdfb8e4bb985ccade55975431b',
	                       properties: ['read', 'write', 'notify'], 
	                       onReadRequest : motorStateRead,
			       onWriteRequest : motorStateWrite,
			       onSubscribe: motorStateSubscribe
			    }),
			   new bleno.Characteristic({ // actively brushing indicator
	                       uuid: 'a8902afd49374346a4f1b7e71616a383',
	                       properties: ['read'], // To do: notify
	                       value : new Buffer('00', 'hex')  // 0 = off
			   }),
			   new bleno.Characteristic({ // battery level
			       uuid : '6dac0185-e4b7-4afd-ac6b-515eb9603c4c',
			       properties: ['read'],
			       value : new Buffer('584c','hex')
			   }),
			   motorSpeedCharacteristic,
			   autoquadrantCharacteristic,
			   buzzCharacteristic,
			   timeCharacteristic,
			 ]
    });
}

var motorSpeed = 0xd0; // lowest speed by default
var motorState = 0;
var autoquadrant = 0x00;
var time = '001011310117'; // SSMMHHDDMMYY

function colorRead(offset, callback) {
    console.log('reading toothbrush color: 0x02 (pink)');
    callback(this.RESULT_SUCCESS, new Buffer('02','hex'));
}

function speedRead(offset, callback) {
    console.log('reading motor speed: 0x', new Buffer.from( [motorSpeed]).toString('hex'));
    callback(this.RESULT_SUCCESS, new Buffer.from( [ motorSpeed ] ));
}

function speedWrite(data, offset, withoutResponse, callback) {
    if (offset) {
	console.log('[-] Failed to write motor speed - bad offset: data=',data, ' offset=',offset);
	callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 1) {
	console.log('[-] Failed to write motor speed - bad data length: data=',data, ' offset=',offset);
	callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
	var newSpeed = data.readUInt8(0);
	console.log('[+] Wrote motor speed: 0x', data.toString('hex'));
	motorSpeed = newSpeed;
	callback(this.RESULT_SUCCESS);
    }
}

function autoquadrantRead(offset,callback){
    console.log('reading auto / quadrant : 0x', new Buffer.from( [autoquadrant]).toString('hex'));
    callback(this.RESULT_SUCCESS, new Buffer.from( [ autoquadrant ] ));
}

function autoquadrantWrite(data, offset, withoutResponse, callback) {
    if (offset) {
	console.log('[-] Failed to write auto off / quadrant buzz - bad offset: data=',data, ' offset=',offset);
	callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 1) {
	console.log('[-] Failed to write auto off / quadrant buzz - bad data length: data=',data, ' offset=',offset);
	callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
	autoquadrant = data.readUInt8(0);
	console.log('[+] Wrote auto off / quadrant buzz: 0x', data.toString('hex'));
	callback(this.RESULT_SUCCESS);
    }
}

function buzzRead(offset, callback) {
    console.log('reading buzz: 0x00');
    callback(this.RESULT_SUCCESS, new Buffer.from( [ 0x00 ] ));
}

function buzzWrite(data, offset, withoutResponse, callback) {
    if (offset) {
	console.log('[-] Failed to write buzz - bad offset: data=',data, ' offset=',offset);
	callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 1) {
	console.log('[-] Failed to write buzz - bad data length: data=',data, ' offset=',offset);
	callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
	if (data.readUInt8(0) == 1) 
	    console.log('[+] Buzzed');
	callback(this.RESULT_SUCCESS);
    }
}

function timeRead(offset,callback) {
    console.log('reading time: ',time);
    callback(this.RESULT_SUCCESS, new Buffer(time,'hex'));
}

function timeWrite(data, offset, withoutResponse, callback) {
    if (offset) {
	console.log('[-] Failed to write time - bad offset: data=',data, ' offset=',offset);
	callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 6) {
	console.log('[-] Failed to write time - bad data length: data=',data, ' offset=',offset);
	callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
	time = data.toString('hex');
	console.log('[+] Wrote time: ', time);
	callback(this.RESULT_SUCCESS);
    }
}


function motorStateRead(offset,callback) {
    console.log('reading motor speed: 0x', new Buffer.from( [motorState]).toString('hex'));
    callback(this.RESULT_SUCCESS, new Buffer.from( [ motorState ] ));
}

function motorStateWrite(data, offset, withoutResponse, callback) {
    if (data.length !== 1) {
	console.log('[-] Failed to write motor state - bad data length: data=',data, ' offset=',offset);
	callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
	motorState = data.readUInt8(0); // data = <Buffer 01>, motorState = 1
	if (motorState == 0)
	    console.log("[+] Turning toothbrush off");
	else
	    console.log("[+] Turning toothbrush on");

	console.log("update: ", this._updateValueCallback);
	if (this._updateValueCallback) {
	    this._updateValueCallback(data);
	    //callback(this.RESULT_SUCCESS);
	} else {
	    console.log("[-] Callback is not set");
	    callback(this.RESULT_UNLIKELY_ERROR);
	}
    }
}

function motorStateSubscribe(maxValueSize, updateValueCallback) {
    console.log("motorStateSubscribe(): ", updateValueCallback);
    this._updateValueCallback = updateValueCallback;
}

function motorStateUnsubscribe() {
    console.log("motorStateUnsubscribe()");
    this._updateValueCallback = null;
}

util.inherits(BeamService, BlenoPrimaryService);

module.exports = BeamService;
