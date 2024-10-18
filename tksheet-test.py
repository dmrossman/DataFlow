# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 08:54:22 2024

@author: dmros
"""

# This code requires tksheet which is not a builtin library.  Use pip install tksheet to install

from tksheet import Sheet
import tkinter as tk
from serial_handler import SerialHandler

class demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
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
        
        var_data = ['1.0e14', '1.23', '6', '25', '5.23', '2/12', '0', '1.0', '60.0', '49.0',
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
            
        # Setup serial
        # Create the serial object
        self.serialHandler = SerialHandler()
        
        # Find the open ports.  If there is only one, go ahead
        # and open it.
        ports = self.serialHandler.serial_ports()
        print('Number of serial ports is:')
        print(len(ports))
        self.serialHandler.openSerialPort("COM9", 9600, self.serialCallback)
        self.serialHandler.startThread()
            
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
        
        
    def closeSerial(self):
        self.serialHandler.stopThread()
        self.serialHandler.closeSerialPort()
    
    def setDose(self, message):
        print('Dose changed')
        
    def setVac(self, message):
        print('Vac changed')
        
    def setAMU(self, message):
        print('AMU changed')

    def setBeam(self, message):
        print('Beam changed')
        
app = demo()
app.mainloop()