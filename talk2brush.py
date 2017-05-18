import argparse
import struct
import time
from gattlib import GATTRequester

'''
__author__ = "Axelle Apvrille"
__version__ = "0.1"

Requirements: gattlib and bluetooth dev libs
sudo apt-get install libglib2.0-dev python-setuptools python-pip \
g++ libbluetooth-dev libboost-python-dev libboost-thread-dev
sudo pip install gattlib

Normally run as:
$ sudo python talk2brush.py 

Beware: only one connection at a time on the toothbrush
=> if the app is connected, this program won't work. Stop the app first.

Troubleshooting:
  "Channel or attrib not ready" -> make sure you don't have another program (smartphone?)
                                                    using BLE and connected to the toothbrush
  "Device busy" => sudo bccmd -d hci0 warmreset
'''

class MyRequester(GATTRequester):
    def on_notification(self, handle, data):
        print "Notification on handle: 0x%x" % (handle)
        if handle == 0x38:
            print "-> Accelerometer data: %s" % (data.encode('hex'))
        if handle == 0x3b:
            print "-> Gyroscope data: %s" % (data.encode('hex'))
        if handle == 0x3e:
            if len(data) > 3:
                button = struct.unpack('B', data[3])[0]
                if button == 0:
                    print "-> Button is not pressed"
                else:
                    print "-> Button is pressed"
            else:
                print "-> Error in button state: %s" % (data.encode('hex'))

class BeamBrush(object):
    def __init__(self, address, verbose=False):
        self.address = address
        self.req = MyRequester(address, False)
        if verbose:
            print "[+] Beam Brush object instantiated"
        
    def connect(self, verbose=False):
        if verbose:
            print "Connecting to %s..." % (self.address)
        self.req.connect(wait=True, channel_type='public')
        if verbose:
            print "[+] Connected to %s" % (self.address)

    def disconnect(self, verbose=False):
        self.req.disconnect()
        if verbose:
            print("[+] Disconnected")

    def is_connected(self):
        return self.req.is_connected()

    def _read(self, handle, verbose=False):
        if verbose:
            print "Reading string from handle=0x%02x" % (handle)
        assert self.req.is_connected(), "Please perform BLE GATT connect first"
        data = self.req.read_by_handle(handle)
        if verbose:
            print "Bytes read: %s" % (data[0].encode('hex'))
        return data[0]

    def read_string(self, handle, message, verbose=False):
        data = self._read(handle, verbose)
        print "[+] %s: %s" % (message, data)

    def read_bytes(self, handle, message, verbose=False):
        data = self._read(handle, verbose)
        print "[+] %s: %s" % (message, ':'.join([ "%02X" % i for i in list(bytearray(data))]))

    def read_integer(self, handle, message, verbose=False):
        data = self._read(handle, verbose)
        value = struct.unpack("I", data)[0]
        print "[+] %s: %d" % (message, value)

    def read_boolean(self, handle, message, verbose=False):
        data = self._read(handle, verbose)
        print "[+] %s: %d" % (message, int(bytearray(data)[0]))

    def read_device_name(self, handle=0x03, verbose=False):
        return self.read_string(handle, "Device Name", verbose)

    def read_appearance(self, handle=0x05, verbose=False):
        return self.read_bytes(handle, "Appearance", verbose)
    
    def read_firmware(self, handle=0x12, verbose=False):
        return self.read_string(handle, "Firmware Revision", verbose)

    def read_manufacturer(self, handle=0x0c, verbose=False):
        return self.read_string(handle, "Manufacturer Name", verbose)

    def read_model(self, handle=0x0e, verbose=False):
        return self.read_string(handle, "Model Number", verbose)
        
    def read_serial_number(self, handle=0x10, verbose=False):
        return self.read_bytes(handle, "Serial Number", verbose)

    def read_brushing(self, handle=0x1a, verbose=False):
        return self.read_boolean(handle, "Actively brushing indicator", verbose)

    def read_motor_state(self, handle=0x20, verbose=False):
        return self.read_boolean(handle, "Motor state", verbose)

    def read_date(self, handle=0x23, verbose=False):
        data = self._read(handle, verbose)
        date = list(bytearray(data))
        print "[+] Date: 20%02x-%x-%x at %x:%x:%x" % (date[5], date[4], date[3], date[2], date[1], date[0])
        return data

    def read_color(self, handle=0x31, verbose=False):
        data = self._read(handle, verbose)
        value = struct.unpack("B", data)[0]
        color = { 1 : 'Blue', 2 : 'Pink', 3 : 'Green' }
        if value not in color:
            print "[+] Unknown brush color"
        else:
            print "[+] %s toothbrush" % (color[value])

    def read_hardware_revision(self, handle=0x33, verbose=False):
        data = self._read(handle, verbose)
        value = struct.unpack("B", data)[0]
        print "[+] Hardware revision: 2.%d" % (value)

    def read_duration(self, handle=0x1d, verbose=False):
        '''How long I brushed my teeth since the last time I stopped the toothbrush
        In seconds
        '''
        return self.read_integer(handle, "Duration", verbose)

    def read_battery_level(self, handle=0x2f, verbose=False):
        data = self._read(handle, verbose)
        value=(struct.unpack("<H",data)[0]) >> 4
        level =  ((value * 0.001221) - 1.1) * 100 / (1.5-1.1)
        print "[+] Battery percentage: %2.1f %%" % (level)

    def read_auto_quadrant(self, handle=0x2d, verbose=False):
        data = self._read(handle, verbose)
        value = struct.unpack("B", data)[0]
        auto_off = False
        quadrant = False
        if (value & 0x01):
            auto_off = True
        if (value & 0x02):
            quadrant = True
        print "[+] Auto off: %d, Quadrant buzzer: %d" % (auto_off, quadrant)

    def read_motor_speed(self, handle=0x2b, verbose=False):
        data = self._read(handle, verbose)
        value = struct.unpack("B", data)[0]
        intensity = (208-(float(value)))*100 / 139
        print "[+] Motor speed: %2.1f %%" % (intensity)

    def write_motor_speed(self, handle=0x2b, intensity=0, verbose=False):
        value = int(((1-(float(intensity)/100))*139) + 69)
        hexstring = struct.pack('B', value) # hexstring is of type string            
        data = self.req.write_by_handle(handle, hexstring)
        if verbose:
            print "[+] Wrote motor speed: intensity=%2.1f" % (intensity)

    def write_auto_quadrant(self, handle=0x2d, auto_off=False, quadrant=False, verbose=False):
        value = 0
        if auto_off:
            value = value | 0x01
        if quadrant:
            value = value | 0x02
        hexstring = struct.pack('B', value) # hexstring is of type string  
        if verbose:
            print "Value=%d" % (value)
        data = self.req.write_by_handle(handle, hexstring)
        if verbose:
            print "[+] Wrote settings auto_off=%d, quadrant_buzz=%d" % (auto_off, quadrant)

    def buzz(self, handle=0x35, verbose=False):
        value = 1
        hexstring = struct.pack('B', value) # hexstring is of type string  
        data = self.req.write_by_handle(handle, hexstring)
        if verbose:
            print "[+] Buzzing"

        
    def enable_accelerometer_notif(self, verbose=False):
        # not working currently
        hexstring = str(bytearray([01, 00]))
        notif_handle = 0x0039
        self.req.write_by_handle(notif_handle, hexstring)
        if verbose:
            print "[+] Will receive accelerometer notifications"

            
    def enable_gyroscope_notif(self, verbose=False):
        # not working currently
        hexstring = str(bytearray([01, 00]))
        notif_handle = 0x003c
        self.req.write_by_handle(notif_handle, hexstring)
        if verbose:
            print "[+] Will receive gyroscope notifications"

    def enable_button_notif(self, verbose=False):
        hexstring = str(bytearray([01, 00]))
        notif_handle = 0x003f
        self.req.write_by_handle(notif_handle, hexstring)
        if verbose:
            print "[+] Will receive button state notifications"

    def read_button_state(self, handle=0x3e, verbose=False):
        return self.read_boolean(handle, "Button state", verbose)

    def read_all_info(self, verbose=False):
        self.read_device_name(verbose=verbose)
        self.read_appearance(verbose=verbose)
        self.read_color(verbose=verbose)
        self.read_manufacturer(verbose=verbose)
        self.read_model(verbose=verbose)
        self.read_serial_number(verbose=verbose)
        self.read_firmware(verbose=verbose)
        self.read_hardware_revision(verbose=verbose)
        self.read_brushing(verbose=verbose)
        self.read_duration(verbose=verbose)
        self.read_motor_state(verbose=verbose)
        self.read_motor_speed(verbose=verbose)
        self.read_auto_quadrant(verbose=verbose)
        self.read_battery_level(verbose=verbose)
        self.read_button_state(verbose=verbose)

    def update_firmware(self, filename, verbose=False):
        # set Flash to Enable
        flash_handle = 0x15
        hexstring = struct.pack('B', 4) # hexstring is of type string  
        if verbose:
            print "Enabling flash: handle=0x%02x str=%s ..." % (flash_handle, hexstring)
        self.req.write_by_handle(flash_handle, hexstring)
        time.sleep(1)
        hexstring = struct.pack('B', 0)
        self.req.write_by_handle(flash_handle, hexstring)
        time.sleep(1)
        hexstring = struct.pack('B', 1)
        self.req.write_by_handle(flash_handle, hexstring)
        time.sleep(2)
        hexstring = struct.pack('B', 2)
        self.req.write_by_handle(flash_handle, hexstring)

        # write the firmware
        try:
            write_handle = 0x17
            index = 0
            chunk_len = 10
            buf = open(filename, 'rb').read()
            while index < len(buf):
                if index + chunk_len >= len(buf):
                    towrite = str(buf[index:])
                else:
                    towrite = str(buf[index:index+chunk_len])
                if verbose:
                    print "Writing handle=0x%02x chunk=%s" % (write_handle, towrite)
                self.req.write_by_handle(write_handle, towrite)
                time.sleep( 2 )
                index = index + chunk_len

        except IOError:
            print "Error reading %s" % (filename)
            return
        

        # reboot
        hexstring = struct.pack('B', 3)
        if verbose:
            print "Rebooting...: handle=0x%02x str=%s" % (flash_handle, hexstring)
        self.req.write_by_handle(flash_handle, hexstring)
        
    def morse(self, message, verbose=False):
        alphabet = { 'a' : '.-',
                     'b': '-...',
                     'c': '-.-.',
                     'd': '-..',
                     'e': '.',
                     'f': '..-.',
                     'g': '--.',
                     'h':'....',
                     'i': '..',
                     'j':'.---',
                     'k': '-.-',
                     'l' : '.-..',
                     'm': '--',
                     'n':'-.',
                     'o':'---',
                     'p':'.--.',
                     'q':'--.-',
                     'r':'.-.',
                     's':'...',
                     't':'-',
                     'u':'..-',
                     'v':'...-',
                     'w':'.--',
                     'x':'-..-',
                     'y': '-.--',
                     'z':'--..',
                     '1':'.----',
                     '2':'..---',
                     '3':'...--',
                     '4':'....-',
                     '5':'.....',
                     '6':'-....',
                     '7':'--...',
                     '8':'---..',
                     '9':'----.',
                     '0':'-----'
        }
        alpha_message = [e.lower() for e in message if e.isalnum()]
        if verbose:
            print "message=%s -> %s" % (message, ''.join(alpha_message))
        for i in range(0, len(alpha_message)):
            morse_value = alphabet[alpha_message[i]]
            for c in morse_value:
                if verbose:
                    print "Character %c in morse: %s, currently playing %c" % (alpha_message[i], morse_value, c)
                if c == '.':
                    # a dot is one unit
                    self.write_motor_speed(intensity=40, verbose=verbose)
                    time.sleep(1)
                else:
                    # a dash is 3 units
                    self.write_motor_speed(intensity=100, verbose=verbose)
                    time.sleep(3)
                # space between parts of the same character is 1 unit
                if verbose:
                    print "1 space"
                self.write_motor_speed(intensity=5, verbose=verbose)
                time.sleep(1)
            # space between letters is 3 units
            if verbose:
                print "2 spaces"
            time.sleep(2) # we already did one
            
    

def get_arguments():
    parser = argparse.ArgumentParser(description='Standalone tool to talk to the Beam Toothbrush', prog='talk2brush.py')
    parser.add_argument('-v', '--verbose', help='various debug messages', action='store_true')
    parser.add_argument('-t', '--target', help='MAC address of the device', required=True, action='store')
    parser.add_argument('-m', '--morse', help='Play Morse message provided as arg', action='store')
    args = parser.parse_args()
    return args

def displayMenu(verbose=False):
    '''returns the function to call on the beam brush object or None if we need to exit'''
    choices = { 'Read firmware revision string' : BeamBrush.read_firmware,
                'Read manufacturer name' : BeamBrush.read_manufacturer,
                'Read model number' : BeamBrush.read_model,
                'Read serial number' : BeamBrush.read_serial_number,
                'Read actively brushing indicator' : BeamBrush.read_brushing,
                'Read current brushing duration in seconds' : BeamBrush.read_duration,
                'Read date' : BeamBrush.read_date,
                'Read motor state' : BeamBrush.read_motor_state,
                'Read brush color' : BeamBrush.read_color,
                'Read hardware revision' : BeamBrush.read_hardware_revision,
                'Read motor speed' : BeamBrush.read_motor_speed,
                'Enable accelerometer data notifications' : BeamBrush.enable_accelerometer_notif,
                'Enable gyroscope data notifications' : BeamBrush.enable_gyroscope_notif,
                'Enable button state notifications' : BeamBrush.enable_button_notif,
                'Read button state' : BeamBrush.read_button_state,
                'Read battery level' : BeamBrush.read_battery_level,
                'Read auto off and quadrant buzzer settings' : BeamBrush.read_auto_quadrant,
                'Write auto off and quadrant buzzer settings' : BeamBrush.write_auto_quadrant,
                'Write motor speed' : BeamBrush.write_motor_speed,
                'Buzz' : BeamBrush.buzz,
                'Read device name' : BeamBrush.read_device_name,
                'Read appearance' : BeamBrush.read_appearance,
                'Read all information' : BeamBrush.read_all_info,
                'Update firmware (experimental)' : BeamBrush.update_firmware,
                'Play morse' : BeamBrush.morse,
    }
    
    # Menu
    print "=== talk2brush - a Beam Brush Linux utility tool ==="
    keys = sorted(choices.keys())
    for item in keys:
        print "%2d- %s" % (keys.index(item), item)
    print "Any other value will quit."

    # Reading choice
    try:
        response = int(raw_input("Your choice? "))
    except ValueError:
        print "Please enter a number!"
        return None

    # Handling action
    if response not in range(0, len(keys)):
        if verbose:
            print "Response beyond range: 0-%d" % (len(keys))
        return None

    return choices[keys[response]]

def get_boolean_input(message, verbose=False):
    value = raw_input("%s: 0=Off, 1=On => Your choice? (0/1)[0] " % (message))
    if value == '1':
        return True
    return False
    
def get_integer_input( message, verbose=False):
    try:
        value = raw_input("%s: => Your choice? [0] " % (message))
        return int(value)
    except ValueError:
        print "Please enter a number!"
        quit()

def get_string_input(message, verbose=False):
    value = raw_input("%s: => Your choice? " % (message))
    return value

def get_confirmation_input(message, verbose=False):
    value = raw_input("%s: => Your choice? [y/N]" % (message))
    if value == 'y':
        return True
    return False

def call_with_more_input(brush, verbose=False):
    if verbose:
        print "Please provide the following extra information"
        
    if func == BeamBrush.write_auto_quadrant:
        auto_off = get_boolean_input('Auto off', verbose=verbose)
        quadrant = get_boolean_input('Quadrant buzz', verbose=verbose)
        brush.write_auto_quadrant(auto_off=auto_off, quadrant=quadrant, verbose=verbose)

    if func == BeamBrush.write_motor_speed:
        intensity = get_integer_input('Motor speed percentage', verbose=verbose)
        brush.write_motor_speed(intensity=intensity, verbose=verbose)

    if func == BeamBrush.update_firmware:
        filename = get_string_input('Firmware file', verbose=verbose)
        if get_confirmation_input('Do you confirm filename is %s' % (filename), verbose=verbose):
            brush.update_firmware(filename=filename,verbose=verbose)

    if func == BeamBrush.morse:
        message = get_string_input('Message to send', verbose=verbose)
        brush.morse(message, verbose=verbose)
        
if  __name__ == '__main__':
    args = get_arguments()
    brush = None
    
    if args.morse is not None:
        if brush is None:
                brush = BeamBrush(address=args.target, verbose=args.verbose)
        brush.morse(args.morse, verbose=args.verbose)
        brush.disconnect(verbose=args.verbose)
        quit()

    while True:
        func = displayMenu(verbose=args.verbose)
        if func is None:
            if brush is not None and brush.is_connected():
                brush.disconnect(verbose=args.verbose)
            if args.verbose:
                print "Bye!"
            quit()
        else:
            if brush is None:
                brush = BeamBrush(address=args.target, verbose=args.verbose)
            if not brush.is_connected():
                brush.connect(verbose=args.verbose)
            if func == BeamBrush.write_auto_quadrant or \
               func == BeamBrush.write_motor_speed or \
               func == BeamBrush.morse or \
               func == BeamBrush.update_firmware:
                call_with_more_input(brush, verbose=args.verbose)
            else:
                func(brush, verbose=args.verbose)
            print ""
        
