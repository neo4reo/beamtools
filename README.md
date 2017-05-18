# Beam Brush tools

The following are **unofficial** tools for security research on the [Beam(R) Brush](http://beam.dental/tech), commercialized by [Beam Dental](http://beam.dental/).

Use with care, and at your own risks.

## Talk2brush

### What is this for?
This tool handles communication with the toothbrush.
For simple tasks, it eliminates the need for the Beam Dental mobile app (and a smartphone).
You just need a laptop, and a standard BLE USB dongle (cost: a few euros) if your laptop does not have a BLE interface.

Example of things you can do:

- Get the battery level. From that you could script it to send you a warning email if the batteries of your toothbrush are getting dangerously low.
- Set motor intensity level.
- Modify auto-off or quadrant buzz settings.
- Buzz.
- etc.

### Supported toothbrush

This tool does not work with the old Bluetooth toothbrush. That toothbrush was Bluetooth not Bluetooth Low Energy.

#### Old toothbrush

![](http://www.foerderland.de/uploads/pics/brush-l_8161.jpg =300)

This is the **old** Bluetooth toothbrush.

#### Supported version

![](https://www.bbva.com/en/data/8663112016/beam-toothbrush-1920x0-c-f.jpg =300)

Those are the toothbrush this tool works with.

### How to install on Linux

Install requirements (mainly, bluetooth dev and gattlib libraries):

```bash
$ sudo apt-get install libglib2.0-dev python-setuptools python-pip g++ libbluetooth-dev libboost-python-dev libboost-thread-dev
$ sudo pip install gattlib
```

Then, make sure your BLE dongle is connected (BLE = Bluetooth Low Energy = Bluetooth Smart = Bluetooth LE 4.0) to your host.

### Run

You need the Bluetooth MAC address of your toothbrush.
You can get this address by scanning BLE device:

```bash
$ sudo hcitool lescan

xx:xx:xx:xx:xx:xx (unknown)
xx:xx:xx:xx:xx:xx Beam Brush
```

Then, launch the tool:

```bash
$ sudo python talk2brush.py --target xx:xx:xx:xx:xx:xx
=== talk2brush - a Beam Brush Linux utility tool ===
 0- Buzz
 1- Enable accelerometer data notifications
 2- Enable button state notifications
 3- Enable gyroscope data notifications
 4- Play morse
 5- Read actively brushing indicator
 6- Read all information
 7- Read appearance
 8- Read auto off and quadrant buzzer settings
 9- Read battery level
10- Read brush color
11- Read button state
12- Read current brushing duration in seconds
13- Read date
14- Read device name
15- Read firmware revision string
16- Read hardware revision
17- Read manufacturer name
18- Read model number
19- Read motor speed
20- Read motor state
21- Read serial number
22- Update firmware
23- Write auto off and quadrant buzzer settings
24- Write motor speed
Any other value will quit.
Your choice? 
```

### Examples

Reading information from the toothbrush:

```
Your choice? 8
[+] Auto off: 1, Quadrant buzzer: 1
Your choice? 9
[+] Battery percentage: 60.8 %
Your choice? 10
[+] Blue toothbrush
Your choice? 14
[+] Device Name: Beam Brush
Your choice? 13
[+] Date: 2017-5-18 at 11:26:31
Your choice? 16
[+] Hardware revision: 2.6
Your choice? 19
[+] Motor speed: 29.5 %
```

Changing motor speed:
```
Your choice? 24
Motor speed percentage: => Your choice? [0] 99
```
Then, turn the toothbrush on to see the difference for motor speed.
You can also do this while the toothbrush is on.




### Usage

```bash
$ sudo python talk2brush.py --help
```

### Screenshot


### Troubleshooting

**Talk2brush responds "Channel or attrib not ready"**:
Make sure you don't have another program which is using the toothbrush.
Typically, close the Beam app on your smartphone and disable Bluetooth.

**Talk2brush responds "Device busy"**:
Try this command to reset your BLE, and then try again talk2brush.

```bash
$ sudo bccmd -d hci0 warmreset
```

**Talk2brush answers "RuntimeError: Could not update HCI connection: Operation not permitted"**
Please run the tool as root (or as a user with appropriate rights for BLE).


**I'm not receiving gyroscope or accelerometer notifications?**
Yes, that's not working for the moment. It seems the service is not yet operational on the toothbrush.


**Why is first request longer than next ones?**
Because we have to connect to the toothbrush (BLE connection).




