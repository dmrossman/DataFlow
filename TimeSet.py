# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 18:16:02 2024

@author: dmros
"""

import time
import math
import serial

# First get the time since 1970
seconds_since_epoch = time.time()

# This is a float, so convert it to an integer
seconds_since_epoch = math.floor(seconds_since_epoch)

# print(seconds_since_epoch)

try:
    computer = serial.Serial(port='COM6', baudrate=9600, timeout=0)
except:
    print("Error opening serial port")

while (True):
    while (computer.in_waiting > 0):
        value = computer.read()
        print(value)
        
        if(value == 255):
            computer.write('T')
            computer.write(seconds_since_epoch)
        