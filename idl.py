# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import datetime as datetime
import os
import re

class Parameter:
    # Used in the recipe
    def __init__(self, beginning, middle, end):        
        self.Beginning_Value = beginning
        self.Middle_Value = middle
        self.End_Value = end
        
# Define a simple class
class IDL:
    def __init__(self):
        # Create a class for a generic DataFlow IDL file
        # Start with the header
        self.Date_Created = datetime.datetime.now().strftime('%m-%d-%Y  %H:%M:%S') 
        self.Lot_ID = ''
        self.Batch_ID = ''
        self.Device_ID = ''
        self.Wafer_Count = ''
        self.Operator_ID = ''
        self.Disk_ID = ''
        self.Recipe = ''
        self.Implant_Time = ''
        
        # Let's try a dictionary of parameters.  The values of the parameter
        # can be looked up by the parameter's name.  Each parameter will have
        # three values: beginning, middle, end of implant.
        self.setupParameters = {'Dose' : [1.0e15, 3], 'Energy Kev' : [80.0, 3], 'A.M.U.' : [11.0, 3], 'Beam Current mAmps' : [1.0, 3], 
                                'Preset Scans' : [42, 3], 'Wafer Size, Inch' : [6, 3], 
                                'P1 Pressure, Torr' : [2.0e-5, 3], 'P2 Pressure, Torr' : [2.0e-5, 3], 'P3 Pressure, Torr' : [2.0e-5, 3],	
                                'Source Arc I, A' : [3.0, 3], 'Source Arc V, V' : [90.0, 3], 'Source Fil I, A' : [150.0, 3], 'Source Fil V, V' : [3.0, 3],
                                'Extraction V, KV' : [40.0, 3], 'Extraction I, mAmps' : [10.0, 3], 'Vap Oven Temp, DegC' : [21.0, 3], 'Vap Heater Temp, DegC' : [1.0, 3],
                                'Gas Leak Valve 1' : [500, 3], 'Gas Leak Valve 2' : [500, 3], 'Gas Leak Valve 3' : [500, 3], 'Gas Leak Valve 4' : [500, 3], 	
                                'Ext Axis 1' : [500, 3], 'Ext Axis 2' : [500, 3], 'Ext Axis 3' : [500, 3], 'Ext Suppress I, mAmps' : [1.0, 3], 
                                'Ext Suppress V, KV' : [1.8, 3], 'Source Magnet I, A' : [17.0, 3], 'Analyzer Mag I, %' : [21.0, 3], 
                                'Post Accel I, A' : [0.2, 3], 'Post Acc Axis 3' : [500, 3], 'Post Acc Supp I, mAmps' : [0.5, 3], 'Post Acc Supp V' : [0.1, 3], 
                                'E.S. Primary I, A' : [10.0, 3], 'E.S. Secondary I, A' : [2.0, 3], 'Aperture Voltage, V' : [0.1, 3], 
                                'Dose Pres Comp, %' : [-1.0, 3], 'E.S. Pres - Start, Torr' : [2.0e-5, 3], 'E.S. Pres - Stop, Torr' : [2.0e-4, 3], 
                                'Estimated Time, Min' : [11.0, 3], 'Actual Time, Min' : [12.0, 3], 'Interruptions' : [0, 3], 'Trim Factor' : [0.96, 3], 
                                'Pump Down Time,sec' : [120, 1], 'Gas #1' : ['OFF', 3], 'Gas #2' : ['OFF', 3], 	'Gas #3' : ['OFF', 3], 'Gas #4' : ['OFF', 3],
                                'Vap' : ['OFF', 3] }
        
        self.Parameters = {}
        
        # Setup a default set of parameteres
        for key in self.setupParameters.keys():
            # Create a temp parameter
            tmpList = []
            # Get the number of times the value is to be repeated in the list
            # This is almost always 3 times, except for Pump Down Time... why can't
            # The all be the same?!
            for i in range(self.setupParameters[key][1]):
                tmpList.append(self.setupParameters[key][0])
                
            # Now create a new entry in the parameters dictionary
            self.Parameters[key] = tmpList
    
    def readIDL(self, fileName):
        # This is the typical way to create the reipe class, from an existing file
        try:
            with open(fileName, 'r') as file:
                lines = file.readlines()
                
                # If the file is a valid recipe, the third line should contain Lot ID
                line = lines[2].strip()
                parts = re.split(r'\s{3,}', line)       # Split the line with 3 or more consecutive white space characters
                if(parts[0] != 'Lot ID'):
                    print('fileName: ' + fileName + ' is not valid')
                    return()
                
                # Ok the file looks valid, since I am here, let's take care
                # of the LotId
                if(len(parts) > 1):
                    self.Lot_ID = parts[1]
                else:
                    self.Lot_ID = ''
                    
                # Date time is the first field in the file.  I am assuming that there is always a date time entry
                self.Date_Created = lines[0].strip()
                
                # Batch ID
                line = lines[3].strip()
                parts = re.split(r'\s{3,}', line)
                if(len(parts) > 1):
                    self.Batch_ID = parts[1]
                else:
                    self.Batch_ID = ''
                    
                # Device ID
                line = lines[4].strip()
                parts = re.split(r'\s{3,}', line)
                if(len(parts) > 1):
                    self.Device_ID = parts[1]
                else:
                    self.Device_ID = ''
                    
                # Wafer count
                line = lines[5].strip()
                parts = re.split(r'\s{3,}', line)
                if(len(parts) > 1):
                    self.Wafer_Count = parts[1]
                else:
                    self.Wafer_Count = ''
                    
                # Operator ID
                line = lines[6].strip()
                parts = re.split(r'\s{3,}', line)
                if(len(parts) > 1):
                    self.Operator_ID = parts[1]
                else:
                    self.Operator_ID = ''
                    
                # Disk ID
                line = lines[7].strip()
                parts = re.split(r'\s{3,}', line)
                if(len(parts) > 1):
                    self.Disk_ID = parts[1]
                else:
                    self.Disk_ID = ''
                    
                # Recipe
                line = lines[8].strip()
                parts = re.split(r'\s{2,}', line)
                if(len(parts) > 1):
                    self.Recipe = parts[1]
                else:
                    self.Recipe = ''
                    
                # Implant Time
                line = lines[9].strip()
                parts = re.split(r'\s{2,}', line)
                if(len(parts) > 1):
                    # Implant time is different, it is followed by '(minutes)'
                    # For now, leave the (minutes) part in
                    self.Implant_Time = parts[1]
                else:
                    self.Implant_Time = ''
                
                # For the remaining lines, put the data into the Parameters
                for i in range(10, 58):
                    line = lines[i].strip()
                    parts = re.split(r'\s{2,}', line)
                    key = parts[0]
                    values = parts[1:]
                    self.Parameters[key] = values
                    
        except Exception as e:
            print(f'An error occurred: {e}')
            return
        
    def writeIDL(self, fileName):
        # This is the typical way to create the reipe class, from an existing file
        try:
            
            with open(fileName, 'w') as file:
                
                # Write out the header rows
                file.write(f'{self.Date_Created:>60}\n\n')
                file.write(f'{"Lot ID":<10}\t{self.Lot_ID}\n')
                file.write(f'{"Batch ID":<10}\t{self.Batch_ID}\n')
                file.write(f'{"Device ID":<14}\t{self.Device_ID}\n')
                file.write(f'{"Wafer Count":<14}\t{self.Wafer_Count}\n')
                file.write(f'{"Operator ID":<14}\t{self.Operator_ID}\n')
                file.write(f'{"Disk ID":<14}\t{self.Disk_ID}\n')
                file.write(f'{"Active Recipe":<14}\t{self.Recipe}\n')
                file.write(f'{"Implant total time":<19}\t{self.Implant_Time}\n\n')
                
                # Now write out the parameter data
                for key, values in self.Parameters.items():
                    if len(values)  == 3:
                        file.write(f'{key:<30}{values[0]:<14}\t{values[1]:<14}\t{values[2]:<14}\n')
                    elif len(values) == 1:
                        file.write(f'{key:<30}{values[0]:<14}\n')
                    else:
                        pass
                        # file.write('\n')
                
        except Exception as e:
            print(f'An error occurred: {e}')
            return
    
    def __repr__(self):
        # return f"Person(name={self.name}, age={self.age}, email={self.email})"
        pass

if __name__ == "__main__":
    
    # inputPath = 'C:/Users/DRossman/OneDrive - Coherent Corporation/Documents/GitHub/DataFlow/IDLs/565442_202411121320.1'
    # outputPath = 'C:/Users/DRossman/OneDrive - Coherent Corporation/Documents/GitHub/DataFlow/IDLs/565442_202411121320.1.output'
    
    inputPath = 'C:/Users/DRossman/Downloads/DF/'
    outputPath = 'C:/Users/DRossman/Downloads/DF2/'
    for fileName in os.scandir(inputPath):
        myIDL = IDL()
        myIDL.readIDL(inputPath + fileName.name)
        myIDL.writeIDL(outputPath + fileName.name)