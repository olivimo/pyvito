# Communication with Vitoligno 300-P
## Hardware
* raspberry pi3
* optolink module

## Installation
1. raspbian installation
2. ssh working with livebox:
```
sudo apt-get remove openssh-server --purge
sudo apt-get install openssh-server
```
3. communication with usb
`lsusb`
`dmesg | grep "now attached"`
Localisez le ID_SERIAL_SHORT : `/sbin/udevadm info --query=all --name=/dev/ttyUSB0` :
	ID_SERIAL_SHORT=AH03F5ZR
	ID_SERIAL=FTDI_FT232R_USB_UART_AH03F5ZR
	ID_VENDOR_FROM_DATABASE=Future Technology Devices International, Ltd

Editez le fichier
`sudo nano /etc/udev/rules.d/70-lesekopf.rules`

SUBSYSTEM=="tty", ATTRS{product}=="FT232R USB UART", ATTRS{serial}=="AH03F5ZR", NAME="vitoir0"

Redémarrez le service udev
`sudo service udev restart`

Check with: `ls -l /dev/serial/{by-path,by-id}/*`

## domoticz installation
1. update sources
`sudo apt-get update`

2. intall from web
`sudo curl -L install.domoticz.com | bash`

## python scripts
1. put the python scripts in /domoticz/scripts
2. change the right to executable
`chmod +x opto.py`

## cron
1. open crontab
`crontab -e`

2. edit
update every 20 min.
`*/20 * * * * /home/pi/domoticz/scripts/vito.py`

upadte every 20 min with log file
`*/20 * * * * /home/pi/domoticz/scripts/vito.py >> /home/pi/vito.log 2>&1`

## synchronize time of the raspberrypi
`sudo dpkg-reconfigure tzdata`

## copying file between remote and host
 
* Copying file to host (i.e. from local to remote computer):
`scp vito.py pi@192.168.1.23:~/domoticz/scripts/vito.py`

* Copying file from host (i.e. from remote computer to local):
`scp pi@192.168.1.23:~/domoticz/scripts/vito .`
NB: the dot at the end of the command means copy file to the current folder.

use the option "-r" to recursively copy entire directories instead of a simple file.

## better option using sshfs
1. `mkdir raspi`
2. `sshfs pi@molnay.ddns.net:pyvito raspi`


## usefull links 
* [http://openv.wikispaces.com/]
* [https://github.com/steand/optolink]
* [https://gist.github.com/mqu/9519e39ccc474f111ffb]

