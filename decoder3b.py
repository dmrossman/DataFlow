# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 08:54:22 2024

@author: dmros
"""

# This version of decode extends the last version by only writing out the data for sections of data
# where an implant occurred.  For the purpose of this code, an implant starts when the dose state
# goes to 11 (hah, takes the raw dataflow data and puts the data into a single row as if 
# dataflow made a request for data and the data frmo dose, amu, beam, vac, were put into one line
# and then saved.  For now if there is missing data (i.e. Vac controller doesn't respond) it will 
# leave the previous data in the buffer.

# The 'b' version is trying to convert the data to floats like I found in Kevin Hague's code.

import struct

class fileDecoder():
    def __init__(self):
        var_names = ['Dose', 'Beam Current', 'Wafer Size', 'Preset Scans', 'Estimated Time', 'Actual Time', 'Press Comp', 'Trim', 'Beam Energy', 'A.M.U.',
                     'Magnet Current', 'Pressure P1', 'Pressure P2', 'Pressure P3', 'E.S. Press Start', 'E.S. Press Stop', 'Source Arc I', 'Source Arc V', 
                     'Source Fil I', 'Source Fil V', 'Source Mag I', 'Vaporizer', 'Vaporizer Oven', 'Vaporizer Heater', 'Extraction I', 'Extraction V',
                     'E.S. Aperture V', 'Extraction Axis 1', 'Extraction Axis 2', 'Extraction Axis 3', 'Ext Suppress I', 'Ext Suppress V', 'Acceleration I',
                     'Accel Axis 3', 'Accel Supp I', 'Accel Supp V', 'E.S. Primary I', 'E.S. Secondary I', 'Gas Leak Vlv 1', 'Gas Leak Vlv 2', 'Gas Leak Vlv 3', 
                     'Gas Leak Vlv 4', 'Plus Ten 1', 'Plus Ten 2', 'Plus Ten 3', 'Ground', 'DoseX', 'DoseY']
        
        # Format is 'Value Name' : [position number, row, column, first byte in message, last byte in message, scaler, format]
        self.lookup = {'Dose'              : [2, 0, 1, 6, 10, 1, 'E'], 
                       'Beam Current'      : [3, 1, 1, 10, 14, 1000, 'F'], 
                       'Wafer Size'        : [4, 2, 1, 14, 18, 1, 'D'], 
                       'Preset Scans'      : [5, 3, 1, 18, 22, 1, 'D'], 
                       'Estimated Time'    : [6, 4, 1, 22, 26, 1, 'F'], 
                       'Actual Time'       : [7, 5, 1, 26, 30, 1, 'F'], 
                       'Press Comp'        : [8, 6, 1, 30, 34, 1, 'F'], 
                       'Trim'              : [9, 7, 1, 34, 38, 1, 'F'],
                       'Beam Energy'       : [10, 8, 1, 6, 10, 0.001, 'F'], 
                       'A.M.U.'            : [11, 9, 1, 10, 14, 1, 'F'], 
                       'Magnet Current'    : [12, 10, 1, 14, 18, 1000, 'F'], 
                       'Pressure P1'       : [13, 11, 1, 6, 10, 1, 'E'],
                       'Pressure P2'       : [14, 12, 1, 10, 14, 1, 'E'], 
                       'Pressure P3'       : [15, 13, 1, 14, 18, 1, 'E'], 
                       'E.S. Press Start'  : [16, 14, 1, 18, 22, 1, 'E'], 
                       'E.S. Press Stop'   : [17, 15, 1, 22, 26, 1, 'E'],
                       'Source Arc I'      : [18, 16, 1, 6, 10, 1, 'F'],
                       'Source Arc V'      : [19, 17, 1, 38, 42, 1, 'F'], 
                       'Source Fil I'      : [20, 18, 1, 10, 14, 1, 'F'], 
                       'Source Fil V'      : [21, 19 ,1, 42, 46, 1, 'F'],
                       'Source Mag I'      : [22, 20, 1, 70, 74 , 1, 'F'], 
                       'Vaporizer'         : [23, 21, 1, 198, 202, 1, 'V'], # This one will need to be fixed
                       'Vaporizer Oven'    : [24, 22, 1, 62, 66, 1, 'F'], 
                       'Vaporizer Heater'  : [25, 0, 1, 66, 70, 1, 'F'],
                       'Extraction I'      : [26, 1, 1, 114, 118, 1000, 'F'], 
                       'Extraction V'      : [27, 2, 1, 74, 78, 0.001, 'F'], 
                       'E.S. Aperture V'   : [28, 3, 1, 138, 142, 1, 'F'],   # I found it.  Need to verify the values
                       'Extraction Axis 1' : [29, 4, 1, 78, 82, 1, 'D'], 
                       'Extraction Axis 2' : [30, 5, 1, 82, 86, 1, 'D'], 
                       'Extraction Axis 3' : [31, 6, 1, 86, 90, 1, 'D'], 
                       'Ext Suppress I'    : [32, 7, 1, 126, 130, 1000, 'F'], 
                       'Ext Suppress V'    : [33, 8, 1, 130, 134, 1, 'F'],
                       'Acceleration I'    : [34, 9, 1, 178, 182, 1000, 'F'], 
                       'Accel Axis 3'      : [35, 10, 1, 150, 154, 1, 'D'], 
                       'Accel Supp I'      : [36, 11, 1, 190, 194, 1000, 'F'], 
                       'Accel Supp V'      : [37, 12, 1, 194, 198, 1, 'F'],
                       'E.S. Primary I'    : [38, 13, 1, 174, 178, 1000, 'F'], 
                       'E.S. Secondary I'  : [39, 14, 1, 166, 170, 1000, 'F'], 
                       'Gas Leak Vlv 1'    : [40, 15, 1, 14, 18, 1, 'D'], 
                       'Gas Leak Vlv 2'    : [41, 16, 1, 18, 22, 1, 'D'],
                       'Gas Leak Vlv 3'    : [42, 17, 1, 22, 26, 1, 'D'], 
                       'Gas Leak Vlv 4'    : [43, 18, 1, 26, 30, 1, 'D'], 
                       'Plus Ten 1'        : [44, 19, 1, 54, 58, 1, 'D'], 
                       'Plus Ten 2'        : [45, 20, 1, 118, 122, 1, 'D'], 
                       'Plus Ten 3'        : [46, 21, 1, 182, 186, 1, 'D'], 
                       'Ground'            : [47, 22, 1, 58, 62, 1, 'D'],
                       'DoseX'             : [48],
                       'DoseY'             : [49]}
        
        
        # Buffer to hold data
        self.buffer = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
                       30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
        
    def clearBuffer(self):
        self.buffer.clear()
        for i in range(50):
            self.buffer.append(0)
            
        
    def decodeMessage(self, message):
        # Decode the message coming from the arduino.  
        
        # First convert the message from bytes to ints - just easier to deal with
        intMessage = []
        for val in message:
            intMessage.append(int(val))
        
        # Depending on where the message came from, update the right part of the user interface
        if(len(message) < 4):
            fo.write("Error: message to short - no channel\n")
            return()
        
        channel = intMessage[3]
        
        # Channel 1 = Dose, 2 = Vac, 4 = AMU, 5 = Beam
        if(channel == 1):
            # print('channel 1 - Dose')
            self.setDose(intMessage)
        elif(channel == 2):
            # print('channel 2 - Vac')
            self.setVac(intMessage)
        elif(channel == 3):
            # print('channel 2 - Vac')
            self.setES(intMessage)
        elif(channel == 4):
            # print('channel 4 - AMU')
            self.setAMU(intMessage)
        elif(channel == 5):
            # print('channel 5 - Beam')
            self.setBeam(intMessage)
        return("break")     # What does this do?
        
        
    def setDose(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 1 Dose message checksum failure\n')
        
        fields = ['Dose', 'Beam Current', 'Wafer Size', 'Preset Scans', 'Estimated Time', 'Actual Time', 'Press Comp', 'Trim']
        for field in fields:
            # Calculate the value for the field
            position, row, col, first_byte, last_byte, scaler, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            # Last byte in message is 255, so decrement by one
            if(last_byte < (len(message) - 1)):
                # val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                val = self.decodeValue(message[first_byte: last_byte], scaler, fmt)
                self.buffer[position] = val
        
        if(len(message) > 40):
            self.buffer[48] = message[38]   # I need to verify that these are correct
            self.buffer[49] = message[39]   # I need to verify that these are correct
        
        
    def setVac(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 2 Vac message checksum failure\n')
        
        fields = ['Pressure P1', 'Pressure P2', 'Pressure P3', 'E.S. Press Start', 'E.S. Press Stop']
        for field in fields:
            # Calculate the value for the field
            position, row, col, first_byte, last_byte, scaler, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            # Last byte in message is 255, so decrement by one
            if(last_byte < (len(message) - 1)):
                # val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                val = self.decodeValue(message[first_byte: last_byte], scaler, fmt)
                self.buffer[position] = val
        
    def setES(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 2 Vac message checksum failure\n')
        
        fields = []
        for field in fields:
            # Calculate the value for the field
            position, row, col, first_byte, last_byte, scaler, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            # Last byte in message is 255, so decrement by one
            if(last_byte < (len(message) - 1)):
                # val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                val = self.decodeValue(message[first_byte: last_byte], scaler, fmt)
                self.buffer[position] = val
        
    def setAMU(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 4 AMU message checksum failure\n')
        
        fields = ['Beam Energy', 'A.M.U.', 'Magnet Current']
        for field in fields:
            # Calculate the value for the field
            position, row, col, first_byte, last_byte, scaler, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            # Last byte in message is 255, so decrement by one
            if(last_byte < (len(message) - 1)):
                # val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                val = self.decodeValue(message[first_byte: last_byte], scaler, fmt)
                self.buffer[position] = val
        
    def setBeam(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 5 Beam message checksum failure\n')
        
        fields = ['Source Arc I', 'Source Arc V', 
        'Source Fil I', 'Source Fil V', 'Source Mag I', 'Vaporizer', 'Vaporizer Oven', 'Vaporizer Heater', 'Extraction I', 'Extraction V',
        'E.S. Aperture V', 'Extraction Axis 1', 'Extraction Axis 2', 'Extraction Axis 3', 'Ext Suppress I', 'Ext Suppress V', 'Acceleration I',
        'Accel Axis 3', 'Accel Supp I', 'Accel Supp V', 'E.S. Primary I', 'E.S. Secondary I', 'Gas Leak Vlv 1', 'Gas Leak Vlv 2', 'Gas Leak Vlv 3', 
        'Gas Leak Vlv 4', 'Plus Ten 1', 'Plus Ten 2', 'Plus Ten 3', 'Ground']
        for field in fields:
            # Calculate the value for the field
            position, row, col, first_byte, last_byte, scaler, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            if(last_byte < len(message)):
                val = self.decodeValue(message[first_byte: last_byte], scaler, fmt)
                self.buffer[position] = val
        
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
    
    def requestMessage(self, msg):
        # First convert the message from bytes to ints - just easier to deal with
        intMessage = []
        for val in msg:
            intMessage.append(int(val))
        
        # A request for data message has a length of 3 and the next two bytes are with 20, 23
        # Let's use channel 1 as the clock
        if(intMessage[3] == 1):
            if(intMessage[4] == 3):
                if(intMessage[5] == 20):
                    if(intMessage[6] == 23): 
                        return(True)
        return(False)
    
    def decodeValue(self, msgBytes, scaler, fmt):
        # decodeValue expects four bytes from one of the messages
        # It uses make float to turn the four bytes into a floating point number
        # Then it scales the amount (current in milliamps, energy in KeV, etc)
        # Then prints out the data in the correct format
        if(len(msgBytes) == 0):
            result = 0
        else:
            result = self.makeFloat(msgBytes)
            
        # Now scale the result
        result = result * scaler
        
        # Now that we have the value, let's return a string with the correct format
        if(fmt == 'D'):     # Deccimal
            return('{:.0f}'.format(result))
        elif(fmt == 'F'):   # Floating point
            return('{:.3f}'.format(result))
        elif(fmt == 'E'):   # Scientific notation, exponent
            return('{:.3e}'.format(result))
        elif(fmt == 'V'):   # Vaporizer - this is special
            return('{:.3f}'.format(result))
        
        #    if((msgBytes[0] > 63) and (msgBytes[0] < 80)):
        #        return('Off')
        #    elif((msgBytes[0] > 79) and (msgBytes[0] < 96)):
        #        return('On')
        #    elif((msgBytes[0] > 95) and (msgBytes[0] < 112)):
        #        return('Cool')
        else:
            print('Error: Invalid number format')
            
            
    def makeFloat(self, msgBytes):
        # This will convert four bytes to IEEE float
        if len(msgBytes) != 4:
            raise ValueError("Input must be four bytes long.")
        
        return(struct.unpack('>f', bytes(msgBytes))[0])
            
        
    
fd = fileDecoder()
# fileName = 'C:/Users/DRossman/Downloads/DataFlow-main/DataFlow-main/dataFlowLog3-12-13-24.txt'
# fileName = 'C:/Users/dmros/Downloads/DataFlow-main/DataFlow-main/dataFlowLog3-12-13-24.txt'
# fileName = 'C:/Users/DRossman/OneDrive - Coherent Corporation/Desktop/dataFlowLog4.txt'
# fileName = 'C:/Users/DRossman/Documents/Temp/DataFlow/dataFlowLog4-secondTry2d.txt'
# outputFileName = 'C:/Users/Dmros/Downloads/DataFlow-main//DataFlow-main/output.txt'
# outputFileName = 'C:/Users/DRossman/Documents/Temp/DataFlow/dataFlowLog4-secondTry-outputd.txt'
# fileName = 'E:/dataFlowLog4.txt'
# fileName = 'F:/NV10 Lightpipes/DataFlow1/Mar-5-2025/dataFlowLog4=Mar5-2025.txt'
# fileName = 'F:/NV10 Lightpipes/DataFlow1/Mar-12-2025/dataFlowLog4=Mar12-2025A.txt'
# fileName = 'C:/Users/DRossman/dataFlowLog4-Mar12-2025A.txt'
fileName = 'F:/NV10 Lightpipes/DataFlow1/Apr-13-2025/dataFlowLog4-Apr13-2025.txt'

# outputFileName = 'C:/Users/Dmros/Downloads/DataFlow-main//DataFlow-main/output.txt'
# outputFileName = 'E:/output.txt'
# outputFileName = 'C:/Users/DRossman/output-impOnly.txt'
outputFileName = 'F:/NV10 Lightpipes/DataFlow1/Apr-13-2025/dataFlowLog4-Apr13-2025-out.txt'

f = open(fileName)
fo = open(outputFileName, "w")

# Get rid of the "Program starting line"
line = f.readline()
 
# Get rid of the first line (column headers)
line = f.readline()
line = f.readline()

lastMillis = 0

state = 'waiting'

# Loop through the first couple of lines and try and decode them...
while(line):

    line = f.readline()
    lineData = line.split()
    
    # Line data looks like
    # 14437	Chan5	MsgLg	8	22	22	22	5	3	20	23	255

    # Is this a request for data message?
    if(len(lineData) > 0):
        # print(len(lineData))
        if(fd.requestMessage(lineData[4:])):
            # Get the time (millis)
            currentMillis = int(lineData[0])
            # print(currentMillis)
            
            # If enough tiem has passed, then this is a new request
            if((currentMillis - lastMillis) > 750):
                lastMillis = currentMillis
                
                # We have a new line, should we write it out?
                if((state == 'waiting') and (int(fd.buffer[49]) == 11)):   # Pumpdown has started
                    state = 'pumping'
                    pumpStartTime = currentMillis
                    # Don't write anything out yet
                elif((state == 'pumping') and (int(fd.buffer[49]) != 11)):   # Pumpdown has ended
                    state = 'implanting'
                    pumpDownTime = (currentMillis - pumpStartTime) / 1000   # Convert it from milliseconds to seconds
                    fo.write(f"Pump down time = {pumpDownTime}\n")
                elif((state == 'implanting') and (int(fd.buffer[49]) != 5)):
                    # Write out the data
                    # Then it is time to write out the current data and clear the buffer
                    fo.write(f"{currentMillis}\t")
                    for i in range(50):
                        fo.write(f"{fd.buffer[i]}\t")
                    fo.write("\n")
                elif((state == 'implanting') and (int(fd.buffer[49]) == 5)):
                    # We are finished with this batch
                    fo.write("\n")
                    state = 'waiting'
        
    
    # print(lineData[:10])
    if(len(lineData) > 0):
        # Skip messages with length = 8
        #if(lineData[3] != '8'):
        fd.decodeMessage(lineData[4:])

f.close()
fo.close()
