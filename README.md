# pyvito

Python interface to vitotronic regulation based on Optolink communication

## Content
1. settings.py
	* file that contains all parameters about adresses of the vitotronic
	* must be modified according personal settings
2. telegram.py
	* definition of Msg Classes that is used to define the telegram to be sent
3. vito.py
	* main file that must be set to executable and launch with cron for instance

## Default configuration
The program is provided without any guarantees and must be used carefully.
For the moment, the reading is safe and the writting is still under development.
VBC 550P 
vitotronic 200 (FO1)
vitoligno 300-P
