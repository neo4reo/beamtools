// A. Apvrille - Fortinet

var util = require('util');
var bleno = require('bleno');
var BlenoPrimaryService = bleno.PrimaryService;

function DeviceInfoService() {
    //console.log("Creating device info service");
    DeviceInfoService.super_.call(this, {
	uuid: '180A',
	characteristics: [ new bleno.Characteristic({ // Manufacturer Name String
	                          uuid: '2A29',
	                          properties: ['read'],
	                          value : 'Beam Technologies' }),
			   new bleno.Characteristic({ // Model Number
			       uuid : '2a24',
			       properties : ['read'],
			       value : 'BB-0002'}),
			   new bleno.Characteristic({ // Firmware Revision String
			       uuid : '2a26',
			       properties : ['read'],
			       value : 'V0.28'}),
			   /*new bleno.Characteristic({ // Serial Number String
			       uuid : '2a25',
			       properties : ['read'],
			       value : '0671DA7D1A00'}),*/
			 ]
    });
}

util.inherits(DeviceInfoService, BlenoPrimaryService);

module.exports = DeviceInfoService;
