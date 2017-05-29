// A. Apvrille - Fortinet

var util = require('util');
var bleno = require('bleno');
var BlenoPrimaryService = bleno.PrimaryService;

function GenericAccessService() {
    GenericAccessService.super_.call(this, {
	uuid: '1800',
	characteristics: [ new bleno.Characteristic({ // Device Name
	    uuid: '2A00',
	    properties: ['read'],
	    value : 'Beam Brush'
	}),
			   new bleno.Characteristic({ // Appearance
			       uuid: '2A01',
			       properties: ['read'],
			       value : new Buffer('02','hex')
	}),
			 ]
    });
}

util.inherits(GenericAccessService, BlenoPrimaryService);

module.exports = GenericAccessService;
