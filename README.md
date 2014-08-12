Interface for communication with open dataloggers
====
This interface allows communication with the datalogger, extract the stored data and obtain values ​​measured by the sensors. 

The principal component is a class called Datalogger developed in Python which uses a configuration file where is the list of devices that can operate.

Based on this list, the class identifies the equipment and obtains information on the communication settings and commands necessary to perform the dialogue.



### Features

* Establish communication with datalogger
* Remove stored and real-time information (if possible)
* Logging of each of the actions
* The ability to add new open dataloggers



### Examples of use

 create an instance of the class
  datalog = datalogger.Datalogger( '/dev/ttyUSB0', 115200, serial.PARITY_NONE, 0, 0, 1)

### Dependencies
* python-pyserial
* python-loggingx
* python-configparser 


