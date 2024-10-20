# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 12:41:20 2023

@author: Dennis.Rossman
"""
import serial
import threading
import sys
import glob

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
                if (self.computer.in_waiting > 0):
                    value = self.computer.read()
                    # print(value)
                    
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
                        if (messageIndex == 0) and (value == b'\x16'):
                            print('got 1')
                            message.clear()
                            message.append(value)
                            messageIndex = 1
                        elif (messageIndex == 1) and (value == b'\x16'):
                            print('got 2')
                            message.append(value)
                            messageIndex += 1
                        elif (messageIndex == 2) and (value == b'\x16'):
                            print('got 3')
                            message.append(value)
                            messageIndex += 1
                        elif (messageIndex == 3) and (value in ('\x01', b'\x02', b'\x04', b'\x05')):
                            # This is the channel : 1 = Dose, 2 = Vac, 4 = AMU, 5 = Beam
                            print('got 4')
                            message.append(value)
                            self.messageLength = self.messageLengths[value]
                            messageIndex += 1
                            inSync = True
                        else:
                            # This is an invalid character
                            # Just throw the value away
                            # print(f"Not in sync - message index = {messageIndex}")
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

        