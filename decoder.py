# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 08:54:22 2024

@author: dmros
"""

# This code requires tksheet which is not a builtin library.  Use pip install tksheet to install

class fileDecoder():
    def __init__(self):
        var_names = ['Dose', 'Beam Current', 'Wafer Size', 'Preset Scans', 'Estimated Time', 'Actual Time', 'Press Comp', 'Trim', 'Beam Energy', 'A.M.U.',
                     'Magnet Current', 'Pressure P1', 'Pressure P2', 'Pressure P3', 'E.S. Press Start', 'E.S. Press Stop', 'Source Arc I', 'Source Arc V', 
                     'Source Fil I', 'Source Fil V', 'Source Mag I', 'Vaporizer', 'Vaporizer Oven', 'Vaporizer Heater', 'Extraction I', 'Extraction V',
                     'E.S. Aperture V', 'Extraction Axis 1', 'Extraction Axis 2', 'Extraction Axis 3', 'Ext Suppress I', 'Ext Suppress V', 'Acceleration I',
                     'Accel Axis 3', 'Accel Supp I', 'Accel Supp V', 'E.S. Primary I', 'E.S. Secondary I', 'Gas Leak Vlv 1', 'Gas Leak Vlv 2', 'Gas Leak Vlv 3', 
                     'Gas Leak Vlv 4', 'Plus Ten 1', 'Plus Ten 2', 'Plus Ten 3', 'Ground']
        
        var_data = ['1.0e14', '1.23', '6', '25', '5.23', '2:12', '0', '1.0', '60.0', '49.0',
                     '123.0', '1.0e-5', '1.0e-6', '1.0e-7', '1.0e-5', '1.0e-4', '0.8', '60.1', 
                     '127.5', '5.24', '8.1', 'OFF', '23.1', '25.2', '1.27', '50.1',
                     '1.27', '500', '450', '350', '0.12', '1.2', '0.1',
                     '850', '0.12', '1.2', '10.0', '0.1', '100', '200', '300', 
                     '400', '991', '992', '993', '994']
        
        # Format is 'Value Name' : [sheet number, row, column, first byte in message, last byte in message, K1, K2], ... 
        self.lookup = {'Dose'              : [1, 0, 1, 6, 9, 2, 64, 'E'], 
                       'Beam Current'      : [1, 1, 1, 10, 13, 0.002, 54, 'F'], 
                       'Wafer Size'        : [1, 2, 1, 14, 17, 2, 64, 'D'], 
                       'Preset Scans'      : [1, 3, 1, 18, 21, 2, 64, 'D'], 
                       'Estimated Time'    : [1, 4, 1, 22, 25, 0.002, 59, 'F'], 
                       'Actual Time'       : [1, 5, 1, 26, 29, 0.002, 59, 'F'], 
                       'Press Comp'        : [1, 6, 1, 30, 33, 0.002, 59, 'F'], 
                       'Trim'              : [1, 7, 1, 34, 37, 0.002, 59, 'F'],
                       'Beam Energy'       : [1, 8, 1, 6, 9, 0.032, 66, 'F'], 
                       'A.M.U.'            : [1, 9, 1, 10, 13, 0.03125038, 61, 'F'], 
                       'Magnet Current'    : [1, 10, 1, 14, 17, 1.333, 64, 'F'], 
                       'Pressure P1'       : [1, 11, 1, 6, 9, 2, 64, 'E'],
                       'Pressure P2'       : [1, 12, 1, 10, 13, 2, 64, 'E'], 
                       'Pressure P3'       : [1, 13, 1, 14, 17, 2, 64, 'E'], 
                       'E.S. Press Start'  : [1, 14, 1, 18, 21, 2, 64, 'E'], 
                       'E.S. Press Stop'   : [1, 15, 1, 22, 25, 2, 64, 'E'],
                       'Source Arc I'      : [1, 16, 1, 6, 9, 0.002, 59, 'F'],
                       'Source Arc V'      : [1, 17, 1, 38, 41, 0.002, 59, 'F'], 
                       'Source Fil I'      : [1, 18, 1, 10, 13, 0.002, 59, 'F'], 
                       'Source Fil V'      : [1, 19 ,1, 42, 45, 0.002, 59, 'F'],
                       'Source Mag I'      : [1, 20, 1, 70, 73 , 0.002, 59, 'F'], 
                       'Vaporizer'         : [1, 21, 1, 198, 201, 0.002, 59, 'V'], # This one will need to be fixed
                       'Vaporizer Oven'    : [1, 22, 1, 62, 65, 0.002, 59, 'F'], 
                       'Vaporizer Heater'  : [2, 0, 1, 66, 69, 0.002, 59, 'F'],
                       'Extraction I'      : [2, 1, 1, 114, 117, 0.002, 54, 'F'], 
                       'Extraction V'      : [2, 2, 1, 74, 77, 0.002, 64, 'F'], 
                       'E.S. Aperture V'   : [2, 3, 1, 138, 141, 0.002, 64, 'F'],   # I found it.  Need to verify the values
                       'Extraction Axis 1' : [2, 4, 1, 78, 81, 2, 64, 'D'], 
                       'Extraction Axis 2' : [2, 5, 1, 82, 85, 2, 64, 'D'], 
                       'Extraction Axis 3' : [2, 6, 1, 86, 89, 2, 64, 'D'], 
                       'Ext Suppress I'    : [2, 7, 1, 126, 129, 0.002, 54, 'F'], 
                       'Ext Suppress V'    : [2, 8, 1, 130, 133, 0.002, 64, 'F'],
                       'Acceleration I'    : [2, 9, 1, 178, 181, 0.002, 54, 'F'], 
                       'Accel Axis 3'      : [2, 10, 1, 150, 153, 2, 64, 'D'], 
                       'Accel Supp I'      : [2, 11, 1, 190, 193, 0.002, 54, 'F'], 
                       'Accel Supp V'      : [2, 12, 1, 194, 197, 0.002, 64, 'F'],
                       'E.S. Primary I'    : [2, 13, 1, 174, 177, 0.002, 54, 'F'], 
                       'E.S. Secondary I'  : [2, 14, 1, 166, 169, 0.002, 54, 'F'], 
                       'Gas Leak Vlv 1'    : [2, 15, 1, 14, 17, 2, 64, 'D'], 
                       'Gas Leak Vlv 2'    : [2, 16, 1, 18, 21, 2, 64, 'D'],
                       'Gas Leak Vlv 3'    : [2, 17, 1, 22, 25, 2, 64, 'D'], 
                       'Gas Leak Vlv 4'    : [2, 18, 1, 26, 29, 2, 64, 'D'], 
                       'Plus Ten 1'        : [2, 19, 1, 54, 57, 2, 64, 'D'], 
                       'Plus Ten 2'        : [2, 20, 1, 118, 121, 2, 64, 'D'], 
                       'Plus Ten 3'        : [2, 21, 1, 182, 185, 2, 64, 'D'], 
                       'Ground'            : [2, 22, 1, 58, 61, 2, 64, 'D']}
        
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
        
        fo.write("Chan 1\t")
        fields = ['Dose', 'Beam Current', 'Wafer Size', 'Preset Scans', 'Estimated Time', 'Actual Time', 'Press Comp', 'Trim']
        for field in fields:
            # Calculate the value for the field
            sheet, row, col, first_byte, last_byte, K1, K2, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            # Last byte in message is 255, so decrement by one
            if(last_byte < (len(message) - 1)):
                val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                fo.write(f"{val}\t")
        fo.write('\n')
        
        
    def setVac(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 2 Vac message checksum failure\n')
        
        fo.write("Chan 2\t")
        fields = ['Pressure P1', 'Pressure P2', 'Pressure P3', 'E.S. Press Start', 'E.S. Press Stop']
        for field in fields:
            # Calculate the value for the field
            sheet, row, col, first_byte, last_byte, K1, K2, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            # Last byte in message is 255, so decrement by one
            if(last_byte < (len(message) - 1)):
                val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                fo.write(f"{val}\t")
        fo.write('\n')
        
    def setES(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 2 Vac message checksum failure\n')
        
        fo.write("Chan 3\t")
        fields = []
        for field in fields:
            # Calculate the value for the field
            sheet, row, col, first_byte, last_byte, K1, K2, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            # Last byte in message is 255, so decrement by one
            if(last_byte < (len(message) - 1)):
                val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                fo.write(f"{val}\t")
        fo.write('\n')
        
    def setAMU(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 4 AMU message checksum failure\n')
        
        fo.write("Chan 4\t")
        fields = ['Beam Energy', 'A.M.U.', 'Magnet Current']
        for field in fields:
            # Calculate the value for the field
            sheet, row, col, first_byte, last_byte, K1, K2, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            # Last byte in message is 255, so decrement by one
            if(last_byte < (len(message) - 1)):
                val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                fo.write(f"{val}\t")
        fo.write('\n')

    def setBeam(self, message):
        # if(self.checkSum(message) == False):
        #     fo.write('Error - Chan 5 Beam message checksum failure\n')
        
        fo.write("Chan 5\t")
        fields = ['Source Arc I', 'Source Arc V', 
        'Source Fil I', 'Source Fil V', 'Source Mag I', 'Vaporizer', 'Vaporizer Oven', 'Vaporizer Heater', 'Extraction I', 'Extraction V',
        'E.S. Aperture V', 'Extraction Axis 1', 'Extraction Axis 2', 'Extraction Axis 3', 'Ext Suppress I', 'Ext Suppress V', 'Acceleration I',
        'Accel Axis 3', 'Accel Supp I', 'Accel Supp V', 'E.S. Primary I', 'E.S. Secondary I', 'Gas Leak Vlv 1', 'Gas Leak Vlv 2', 'Gas Leak Vlv 3', 
        'Gas Leak Vlv 4', 'Plus Ten 1', 'Plus Ten 2', 'Plus Ten 3', 'Ground']
        for field in fields:
            # Calculate the value for the field
            sheet, row, col, first_byte, last_byte, K1, K2, fmt = self.lookup[field]
            # Make sure the bytes to decode are in the message
            if(last_byte < len(message)):
                val = self.decodeValue(message[first_byte: last_byte], K1, K2, fmt)
                fo.write(f"{val}\t")
        fo.write('\n')
        
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
    
    def decodeValue(self, msgBytes, K1, K2, fmt):
        # decodeValue expects three bytes from one of the messages
        # If the first byte is zero, just return zero
        # Otherwise:
        #      Raise 4 to the power of the result of subtracting K2 from the first byte
        #      Take the second byte, if it is less than 128, then byte 2 and byte 3 don't change
        #      If byte 2 is greater than 127, then byte 2 = byte 2 * 2 - 128
        #      and byte 3 = byte 3 * 2
        # result = (K1/32768) * 4^(byte 1 - K2)*(32768 + 256 * byte 2 + byte 3)
        if(len(msgBytes) == 0):
            result = 0
        elif(msgBytes[0] == 0):
            result = 0
        else:
            if (msgBytes[1] >= 128):
                msgBytes[1] = 2 * msgBytes[1] - 128
                msgBytes[2] = 2 * msgBytes[2]
            
            result = (K1/32768) * 4**(msgBytes[0] - K2) * (32768 + (256 * msgBytes[1]) + msgBytes[2])
        
        # Now that we have the value, let's return a string with the correct format
        
        if(fmt == 'D'):     # Deccimal
            return('{:.0f}'.format(result))
        elif(fmt == 'F'):   # Floating point
            return('{:.3f}'.format(result))
        elif(fmt == 'E'):   # Scientific notation, exponent
            return('{:.3e}'.format(result))
        elif(fmt == 'V'):   # Vaporizer - this is special
            if((msgBytes[0] > 63) and (msgBytes[0] < 80)):
                return('Off')
            elif((msgBytes[0] > 79) and (msgBytes[0] < 96)):
                return('On')
            elif((msgBytes[0] > 95) and (msgBytes[0] < 112)):
                return('Cool')
        else:
            print('Error: Invalid number format')
        
    
fd = fileDecoder()
# fileName = 'C:/Users/DRossman/Downloads/DataFlow-main/DataFlow-main/dataFlowLog3-12-13-24.txt'
# fileName = 'C:/Users/dmros/Downloads/DataFlow-main/DataFlow-main/dataFlowLog3-12-13-24.txt'
fileName = 'E:/dataFlowLog4-Sunday.txt'

# outputFileName = 'C:/Users/Dmros/Downloads/DataFlow-main//DataFlow-main/output.txt'
outputFileName = 'E:/output.txt'

f = open(fileName)
fo = open(outputFileName, "w")
 
# Get rid of the first line (column headers)
line = f.readline()
line = f.readline()

# Loop through the first couple of lines and try and decode them...
while(line):

    line = f.readline()
    lineData = line.split()
    if(len(lineData) > 0):
        # Skip messages with length = 8
        #if(lineData[3] != '8'):
        fo.write(f"{lineData[0]}\t")
        fd.decodeMessage(lineData[4:])
        
f.close()
fo.close()
