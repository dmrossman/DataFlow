# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 08:54:22 2024

@author: dmros
"""

# This code requires tksheet which is not a builtin library.  Use pip install tksheet to install

from serial_handler import SerialHandler
            
# Setup serial
# Create the serial object
serialHandler = SerialHandler()

def serialCallback(message):
    # Decode the message coming from the arduino.  
    # print(message)
    
    # First convert the message from bytes to ints - just easier to deal with
    intMessage = []
    for val in message:
        intMessage.append(int.from_bytes(val, "big"))
    
    # Depending on where the message came from, update the right part of the user interface
    channel = intMessage[3]
    messageNum = inMessage[5]
    
    # Channel 1 = Dose, 2 = Vac, 4 = AMU, 5 = Beam
    if(channel == 0):
        print('channel 0 - {}'.format(messageNum))
    elif(channel == 1):
        print('channel 1 - {}'.format(messageNum))
    elif(channel == 2):
        print('channel 2 - {}'.format(messageNum))
    elif(channel == 3):
        print('channel 3 - {}'.format(messageNum))
    elif(channel == 4):
        print('channel 4 - {}'.format(messageNum))
    return("break")     # What does this do?
    

# Find the open ports.  If there is only one, go ahead
# and open it.
ports = serialHandler.serial_ports()
print('Number of serial ports is:')
print(len(ports))
serialHandler.openSerialPort("COM6", 9600, serialCallback)
serialHandler.startThread()
            
    
def closeSerial(self):
    self.serialHandler.stopThread()
    self.serialHandler.closeSerialPort()
    
    
