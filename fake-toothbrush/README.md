# Fake smart toothbrush

Simulates a Beam Dental toothbrush with a BLE USB dongle.
For test - use with caution, be responsible.

## Run

Pre-requisites:

- Make sure your host supports BLE or purchase a BLE USB dongle
- Docker

Install:

1. Build the container:

```
$ docker build -t cryptax/bleno .
```

2. Insert BLE dongle then, on the **host**:

```
$ sudo service bluetooth stop
$ sudo hciconfig hci0 up
```

3. Run the Docker container:

```
$ docker run -it --net=host --privileged --name fake-toothbrush -v JSSOURCES:/js cryptax/bleno /bin/bash
root@alligator:/data# service bluetooth stop
[ ok ] Stopping bluetooth: /usr/sbin/bluetoothd.
root@alligator:/data# cd /js && node main.js
Fake Toothbrush BLE device
[+] Start advertising as Beam Service
[+] setServices: success
...
```

where JSSOURCES is the absolute path to the .js files in this repository.

Note: bluetooth service must be **stopped** on both container and host.
