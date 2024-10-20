# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 08:54:22 2024

@author: dmros
"""

# This code requires tksheet which is not a builtin library.  Use pip install tksheet to install

import tkinter as tk
from tkinter import messagebox
from tksheet import Sheet
from serial_handler import SerialHandler

class demo(tk.Tk):
    def __init__(self):
        self.window = tk.Tk.__init__(self)
        self.geometry("900x700")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        var_names = ['Dose', 'Beam Current', 'Wafer Size', 'Preset Scans', 'Estimated Time', 'Actual Time', 'Press Comp', 'Trim', 'Beam Energy', 'A.M.U.',
                     'Magnet Current', 'Pressure P1', 'Pressure P2', 'Pressure P3', 'E.S. Press Start', 'E.S. Press Stop', 'Source Arc I', 'Source Arc V', 
                     'Source Fil I', 'Source Fil V', 'Source Mag I', 'Vaporizer', 'Vaporizer Oven', 'Vaporizer Heater', 'Extraction I', 'Extraction V',
                     'E.S. Aperture V', 'Extraction Axis 1', 'Extraction Axis 2', 'Extraction Axis 3', 'Ext Suppress I', 'Ext Suppress V', 'Acceleration I',
                     'Accel Axis 3', 'Accel Supp I', 'Accel Supp V', 'E.S. Primary I', 'E.S. Secondary I', 'Gas Leak Valv 1', 'Gas Leak Vlv 2', 'Gas Leak Vlv 3', 
                     'Gas Leak Vlv 4', 'Plus Ten 1', 'Plus Ten 2', 'Plus Ten 3', 'Ground']
        
        var_data = ['1.0e14', '1.23', '6', '25', '5.23', '2:12', '0', '1.0', '60.0', '49.0',
                     '123.0', '1.0e-5', '1.0e-6', '1.0e-7', '1.0e-5', '1.0e-4', '0.8', '60.1', 
                     '127.5', '5.24', '8.1', 'OFF', '23.1', '25.2', '1.27', '50.1',
                     '1.27', '500', '450', '350', '0.12', '1.2', '0.1',
                     '850', '0.12', '1.2', '10.0', '0.1', '100', '200', '300', 
                     '400', '991', '992', '993', '994']
        
        self.sheet1 = Sheet(self.frame)
        self.sheet2 = Sheet(self.frame)
        
        # Set up a list to hold the Column Header values.
        head = ['Variable Names','Actual']
        # and apply them to the data grid.
        self.sheet1.headers(head)
        self.sheet2.headers(head)
        
        self.sheet1.enable_bindings()
        self.sheet2.enable_bindings()
        
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet1.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet2.grid(row = 0, column = 1, sticky = "nswe")
        
        # Populate the data
        for row in range(0, 22):
            self.sheet1.insert_row()
            self.sheet1.set_cell_data(row, 0, var_names[row])
            self.sheet1.set_cell_data(row, 1, var_data[row])
        for row in range(23, 46):
            self.sheet2.insert_row()
            self.sheet2.set_cell_data(row - 23, 0, var_names[row])
            self.sheet2.set_cell_data(row - 23, 1, var_data[row])
            
        # Create a button for doing random stuff
        self.button = tk.Button(text = "Do Something", command=self.changeData)
        self.button.grid(row = 1, column = 0, columnspan=1, sticky = "nswe")
            
        # Setup serial
        # Create the serial object
        # self.serialHandler = SerialHandler()
        
        # Find the open ports.  If there is only one, go ahead
        # and open it.
        # ports = self.serialHandler.serial_ports()
        # print('Number of serial ports is:')
        # print(len(ports))
        # self.serialHandler.openSerialPort("COM9", 9600, self.serialCallback)
        # self.serialHandler.startThread()
            
    def changeData(self):
        print('Change data')
        # print(self.sheet1.get_cell_data(0, 1))
        # self.sheet1.set_cell_data(0, 1, '1.0E15')
        # print(self.sheet1.get_cell_data(0, 1))
        # self.sheet1.refresh()       # Changed data doesn't always show up unless you refresh it?
        # print('Data changed')
        amu_message = [22, 22, 22, 4, 18, 1, 71, 135, 190 ,0, 66, 147, 153, 153, 66, 198, 0, 0, 5, 0, 0, 179, 255]
        # self.serialCallback(amu_message)
        self.setAMU(amu_message)

    
    def serialCallback(self, message):
        print("App: callBack: message:")
        print(message)
        # Decode the message coming from the arduino.  
        # decodedMsg = self.implanter.decodeMessage(message)
        # print("decoded message")
        # print(decodedMsg)
        
        # Depending on where the message came from, update the right part of the user interface
        channel = message[3]
        
        # Channel 1 = Dose, 2 = Vac, 4 = AMU, 5 = Beam
        if(channel == 1):
            self.setDose(message)
        elif(channel == 2):
            self.setVac(message)
        elif(channel == 4):
            self.setAMU(message)
        elif(channel == 5):
            self.setBeam(message)
        return("break")     # What does this do?
        
        
    def closeSerial(self):
        self.serialHandler.stopThread()
        self.serialHandler.closeSerialPort()
    
    def setDose(self, message):
        print('Dose changed')
        
    def setVac(self, message):
        print('Vac changed')
        
    def setAMU(self, message):
        print('AMU changed')
        if(self.checkSum(message) == False):
            print('Error - AMU message checksum failure')
        print(message)
        
        beam_energy = self.decodeValue(message[6:9], 0.032, 66)
        # self.sheet1.set_cell_data(0, 9, str(beam_energy))
        self.sheet1.set_data("A9", [[str(beam_energy)]])
        print('beam_energy = ' + str(beam_energy))
        
        magnet_current = self.decodeValue(message[14:17], 1.333, 64)
        # self.sheet1.set_cell_data(0, 11, str(magnet_current))
        self.sheet1.set_data("A11", [[str(magnet_current)]])
        print('magnet_current = ' + str(magnet_current))
        
        amu_val = self.decodeValue(message[10:13], 0.03125038, 61)
        self.sheet1.set_data("A10", [[str(beam_energy)]])
        # self.sheet1.set_cell_data(0, 10, str(amu_val))
        print('amu_val = ' + str(amu_val))
        
        self.sheet1.refresh()
        print(self.sheet1.get_cell_data(0, 9))
        print(self.sheet1.get_cell_data(0, 11))
        print(self.sheet1.get_cell_data(0, 10))
        self.sheet1.edit_cell_validation = False
        self.sheet2.refresh()
        self.sheet1.refresh()
        

    def setBeam(self, message):
        print('Beam changed')
        
    def checkSum(self, message):
        # Check the message and see if the checksum is valid
        # The message format is 22 22 22 <channel id>  <number of remaining columns> .... <checksum> 255
        # The checksum is calculated by summing all of the columns after the channel id up to the 
        # checksum.  First we take the mod of the sum with 255.  Then we subtract the floor of the sum
        # divided by 255.  If the result is negative, we add 255 until it is not negative.
        
        # First get the sum
        sum_of_bytes = 0
        for val in message[4:-2]:
            sum_of_bytes += val
        
        # Now get the modulus of the sum and 255
        mod_val = sum_of_bytes % 255
        
        # Now get the integer division of the sum and 255
        floor_val = sum_of_bytes // 255
        
        # Subtract the floor from the modulous
        result = mod_val - floor_val
        
        # Make sure result is not negative
        while(result < 0):
            result += 255
            
        # If the checksum result matches the checksum in the message, return true
        if(result == message[len(message) - 2]):
            return(True)
        return(False)
    
    def decodeValue(self, msgBytes, K1, K2):
        # decodeValue expects three bytes from one of the messages
        # If the first byte is zero, just return zero
        # Otherwise:
        #      Raise 4 to the power of the result of subtracting K2 from the first byte
        #      Take the second byte, if it is less than 128, then byte 2 and byte 3 don't change
        #      If byte 2 is greater than 127, then byte 2 = byte 2 * 2 - 128
        #      and byte 3 = byte 3 * 2
        # result = (K1/32768) * 4^(byte 1 - K2)*(32768 + 256 * byte 2 + byte 3)
        if(msgBytes[0] == 0):
            return(0)
        
        if(msgBytes[1] >= 128):
            msgBytes[1] = 2 * msgBytes[1] - 128
            msgBytes[2] = 2 * msgBytes[2]
            
        result = (K1/32768) * 4**(msgBytes[0] - K2) * (32768 + (256 * msgBytes[1]) + msgBytes[2])
        return(result)
    
    def on_close(self):
        print("Closing")
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # self.closeSerial()
            self.destroy()

        
app = demo()
app.mainloop()