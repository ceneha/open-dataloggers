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

The following example establish connection with datalogger and extracts its stored information

  > 
    import datalogger
    import serial
    import sys
    import os
    import logging
    # create an instance of the class, need parameters serial port and datalogger number from list (last)
    datalog = datalogger.Datalogger( '/dev/ttyUSB0', 115200, serial.PARITY_NONE, 0, 0, 1)
    datalog.start_conexion()
    # remove stored information, need destination file path
    datalog.get_datalogger_data("pathFile")
    datalog.close_conexion()


This example establish connection with datalogger and and returns to the screen the variables measured by sensors connected to the datalogger

  > 
    import datalogger
    import serial
    import sys
    import os
    import logging
    # create an instance of the class, need parameters serial port and datalogger number from list (last)
    datalog = datalogger.Datalogger( '/dev/ttyUSB0', 115200, serial.PARITY_NONE, 0, 0, 1)
    datalog.start_conexion()
    datalog.get_data_rt()
    datalog.close_conexion()

### Dependencies
* python-pyserial
* python-loggingx
* python-configparser 


