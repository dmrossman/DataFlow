# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 12:41:20 2023

@author: Dennis.Rossman
"""
import serial
import threading
import sys
import glob
import time
import math

class SerialHandler:
    def __init__(self):
        
        # This class will capture data coming in on the serial port.
        # When the message ends, a callback function will be called with the 
        # received data.
        
        # Note, take a look at Arduino library SerialTransfer.  It takes care of a lot of things 
        # and it has CRC checking.  I will stick with my code for now, but it looks promising.
        
        # Variable to help us stop the thread
        self.runThread = True
        
        # Create a set of constants for the different messages so I know the message length
        # Message 1 = Dose, 2 = Vac, 4 = AMU, 5 = Beam
        self.messageLengths = {1 : 43, 2 : 33, 4 : 22, 5 : 204}
        self.messageLength = 0    # Place holder for the message length of the current message
        
        # Open a connection
        # self.computer = serial.Serial(port=serialPort, baudrate=serialBaudRate, timeout=0)
        # self.computer = serial.Serial('COM9', 9600)
        
        # Create a thread to grab data from the serial port
        # This will run forever in the background until it is stopped
        self.serial_thread = threading.Thread(target=self.handle_serial_port, args=(), daemon=True)
        print('Created the thread')
        
        # Send the current computer time to the arduino (Should I do this here or in the tksheet code?)
        curr_time = math.floor(time.time())
        curr_time_series = self.int_to_series(curr_time)
        len_of_msg = len(curr_time_series) + 1
        # Create a message out of bytes.  First three are 22 (message into), then channel (0), number of remaining byte, message, then 255
        time_msg = [22, 22, 22, 0, len_of_msg] + curr_time_series
        # End the message with a 255
        time_msg.append(255)
        # Now send it
        # self.sendMessage(time_msg)
        
    def int_to_series(self, num):
        # Used to convert a time value into a series of bytes
        # A time value of 1733011658 would convert to [1, 7, 3, 3, 0, 1, 1, 6, 5, 8]
        num_str = str(num)
        return [int(digit) for digit in num_str]
        
    def startThread(self):
        self.runThread = True
        self.serial_thread.start()
        print('Started the thread')
        
    def stopThread(self):
        self.runThread = False
        self.serial_thread.join()
        print('Stopped the thread')
        
    def openSerialPort(self, serialPort, serialBaudrate, callBackFunction):
        self.port = serialPort
        self.baudrate = serialBaudrate
        self.callBack = callBackFunction
        self.state = "open"
        try:
            self.computer = serial.Serial(port=serialPort, baudrate=serialBaudrate, timeout=0)
            self.computer.reset_input_buffer()
            self.computer.reset_output_buffer()
        except:
            print("Error opening serial port")
            self.state = "closed"
            
    def closeSerialPort(self):
        try:
            self.computer.close()
        except:
            # If the serial port never opened, just ignore and continue
            pass
                   
        
    def handle_serial_port(self):
        inSync = False
        message = []
        messageIndex = 0
        # messageLength = 0
    
        try:
            while (self.runThread):
                while (self.runThread) and (self.computer.in_waiting > 0):
                    value = self.computer.read()
                    print('{}, '.format(value), end='')
                    
                    # Are we in sync (in a message)
                    if inSync:
                        # Are we in a message?
                        # Keep appending data until we get all of the bytes
                        
                        if messageIndex < self.messageLength:
                            message.append(value)
                            messageIndex += 1
                        elif messageIndex == self.messageLength:
                            message.append(value)
                            messageIndex += 1
                            
                            # The last byte should be 255
                            if value == b'\xFF':
                                # We are done with the message
                                messageIndex = 0
                                inSync = False
                                self.callBack(message)
                            else:
                                # Something went wrong
                                print("Error: Last byte in message was not 255")
                                print("Channel = " + str(message[3]))
                                print("Last value = " + str(value))
                                messageIndex = 0
                                inSync = False
    
                    else:
                        # We get in sync if we find the value 22 three times followed by a valid
                        # channel (1, 2, 4, 5)
                        if (messageIndex == 0):
                            if (value == b'\x16'):
                                # print('got 1')
                                message.clear()
                                message.append(value)
                                messageIndex = 1
                            else:
                                print('Sync error: index 0')
                        elif (messageIndex == 1):
                            if (value == b'\x16'):
                                # print('got 2')
                                message.append(value)
                                messageIndex += 1
                            else:
                                print('Sync error: index 1')
                                messageIndex = 0
                        elif (messageIndex == 2):
                            if (value == b'\x16'):
                                # print('got 3')
                                message.append(value)
                                messageIndex += 1
                            else:
                                print('Sync error: index 2')
                                messageIndex = 0
                        elif (messageIndex == 3):
                            if  (value in (b'\x01', b'\x02', b'\x04', b'\x05', b'\x0F')):
                                # This is the channel : 1 = Dose, 2 = Vac, 4 = AMU, 5 = Beam, 3 = End Station?, 0 = Request for time
                                # print('got channel : ' + str(int.from_bytes(value)))
                                message.append(value)
                                # self.messageLength = self.messageLengths[int.from_bytes(value)]
                                messageIndex += 1
                                # inSync = True
                            else:
                                print('Sync error: invalid channel')
                                messageIndex = 0
                        elif (messageIndex == 4):
                            # This is the number of bytes left in the message
                            # It turns out that some messages are shorter than others.  I need
                            # to investigate
                            self.messageLength = int.from_bytes(value) + 4 # The four accounts for the 22, 22, 22, channel
                            message.append(value)
                            messageIndex += 1
                            inSync = True
                            
                            
                        else:
                            # This is an invalid character
                            # Just throw the value away
                            print(f"Not in sync - message index = {messageIndex}")
                            messageIndex = 0
        finally:
            self.computer.close()
            
    def sendMessage(self, message):
        self.computer.write(message)
        

    def serial_ports(self):
        """ Lists serial port names
    
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

        