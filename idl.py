# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import datetime as datetime
import os

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
        self.Date_Created = datetime.now().strftime('%m-%d-%Y  %H:%M:%S') 
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
        self.setupParameters = {'Dose' : [1.0e15, 3], 'Energy Kev' : [80.0, 3], '	A.M.U.' : [11.0, 3], '	Beam Current mAmps' : [1.0, 3], 
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
                                'Pump Down Time,sec' : [120, 1], 'Gas #1' : ['OFF', 3], '	Gas #2' : ['OFF', 3], 	'Gas #3' : ['OFF', 3], 'Gas #4' : ['OFF', 3],
                                'Vap' : ['OFF', 3] }
        
        self.Parameters = {}
        
        for param in setupParameters:
            # Create a temp parameter
            tmpList = ()
            # Get the number of times the value is to be repeated in the list
            # This is almost always 3 times, except for Pump Down Time... why can't
            # The all be the same?!
            for i in range(setupParameters[param][1]):
                tmpList.append(setupParameters[param][0])
                
            # Now create a new entry in the parameters dictionary
            self.Parameters[param] 
        # First create a parameter object 
        dose = Parameter(1.0e15, 1.0e15, 1.0e15,)        
        # Then append the key / value pair
        self.Parameters['Dose'] = dose
        
        energy = Parameter(80.0, 80.0, 80.0)
        self.Parameters['Energy Kev'] = energy
        
        amu = Parameter(11.0, 11.0, 11.0) 
        self.Parameters['A.M.U.'] = amu
        
        beam_current = Parameter(1.0, 1.0, 1.0)
        self.Parameters['Beam Current mAmps'] = beam_current
        
        preset_scans = Parameter(10, 10, 10)
        self.Parameters['Preset Scans'] = preset_scans
        
        wafer_size = Parameter(6, 6, 6)
        self.Parameters['Wafer Size, Inch'] = wafer_size
        
        preset_scane = Parameter(0, 0, 0, 0)
        self.Parameters['Preset_Scans'] = preset_scane
        
        est_time = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Estimated_Time'] = est_time
        
        act_time = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Actual_Time'] = act_time
        
        press_comp = Parameter(0.0, 0.0, 1, 1)
        self.Parameters['Pressure_Comp'] = press_comp
        
        trim = Parameter(0.0, 0.0, 1, 1)
        self.Parameters['Trim'] = trim
        
        press_p3 = Parameter(0.000e+000, 0.000e+000, 0, 0)
        self.Parameters['Pressure_P3'] = press_p3
        
        press_p2 = Parameter(0.000e+000, 0.000e+000, 0, 0)
        self.Parameters['Pressure_P2'] = press_p2
        
        press_p1 = Parameter(0.000e+000, 0.000e+000, 0, 0)
        self.Parameters['Pressure_P1'] = press_p1
        
        es_press_start = Parameter(0.000e+000, 0.000e+000, 1, 1)
        self.Parameters['ES_Pressure_Start'] = es_press_start 
        
        es_press_stop = Parameter(0.000e+000, 0.000e+000, 1, 1)
        self.Parameters['ES_Pressure_Stop'] = es_press_stop
        
        arc_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Src_Arc_Current'] = arc_current
        
        arc_voltage = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Src_Arc_Voltage'] = arc_voltage
        
        fil_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Source_Fil_Current'] = fil_current
        
        fil_voltage = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Source_Fil_Voltage'] = fil_voltage
        
        extr_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Extraction_Current'] = extr_current
        
        extr_voltage = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Extraction_Voltage'] = extr_voltage
        
        src_mag_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Source_Magnet_Current'] = src_mag_current
        
        extr_supr_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Extraction_Suppr_Current'] = extr_supr_current
        
        extr_suppr_voltage = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Extraction_Suppr_Voltage'] = extr_suppr_voltage
        
        accel_supr_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Post_Accel_Suppr_Current'] = accel_supr_current
        
        accel_suppr_voltage = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Post_Accel_Suppr_Voltage'] = accel_suppr_voltage
        
        gas1 = Parameter(0, 0, 0, 0)
        self.Parameters['Gas_Leak_Valve_1'] = gas1
        
        gas2 = Parameter(0, 0, 0, 0)
        self.Parameters['Gas_Leak_Valve_2'] = gas2
        
        gas3 = Parameter(0, 0, 0, 0)
        self.Parameters['Gas_Leak_Valve_3'] = gas3
        
        gas4 = Parameter(0, 0, 0, 0)
        self.Parameters['Gas_Leak_Valve_4'] = gas4
        
        vap_oven_temp = Parameter(3, 3, 1, 1)
        self.Parameters['Vaporizer_Oven_Temp'] = vap_oven_temp
        
        vap_heater_temp = Parameter(3, 3, 1, 1)
        self.Parameters['Vaporizer_Heater_Temp'] = vap_heater_temp
        
        axis1 = Parameter(0, 0, 0, 0)
        self.Parameters['Extraction_Axis_1'] = axis1
        
        axis2 = Parameter(0, 0, 0, 0)
        self.Parameters['Extraction_Axis_2'] = axis2
        
        axis3 = Parameter(0, 0, 0, 0)
        self.Parameters['Extraction_Axis_3'] = axis3
        
        eshower_primary_current = Parameter(4.0, 40.0, 1, 1)
        self.Parameters['Elec_Shwr_Pri_Current'] = eshower_primary_current
        
        eshower_sec_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Elec_Shwr_Sec_Current'] = eshower_sec_current
        
        eshower_aper_voltage = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Elec_Shower_Aper_Voltage'] = eshower_aper_voltage
        
        accel_axis3 = Parameter(0, 0, 0, 0)
        self.Parameters['Post_Accel_Axis_3'] = accel_axis3
        
        accel_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Post_Accel_Current'] =  accel_current
        
        interupts = Parameter(0, 0, 0, 0)
        self.Parameters['Interruptions'] = interupts
        
        es4_beam_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['ES4_%Beam_Current'] = es4_beam_current
        
        es4_gas_flow = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['ES4_Implant_Gas_Flow'] = es4_gas_flow
        
        eshower_on = Parameter(0, 0, 1, 0)
        self.Parameters['Electron_Shower_ON'] = eshower_on
        
        eshower_mode = Parameter(0, 0, 1, 0)
        self.Parameters['ES_Primary_Control_Mode'] = eshower_mode 
        
        carrier_gas = Parameter(0, 0, 0, 0)
        self.Parameters['Carrier_Gas_Support'] = carrier_gas
        
        axis3_detune = Parameter(0, 0, 0, 0)
        self.Parameters['Axis_3_Detune'] = axis3_detune
        
        bais_aper_on = Parameter(0, 0, 1, 0)
        self.Parameters['Bias_Aperture_ON'] = bais_aper_on
        
        hi_energy_electrode = Parameter(0, 0, 0, 0)
        self.Parameters['HI_Energy_Electrode'] = hi_energy_electrode
        
        mag_defl_in = Parameter(0, 0, 0, 0)
        self.Parameters['Magnetic_Deflector_In'] = mag_defl_in
        

    def __init__(self, fileName):
        # This is the typical way to create the reipe class, from an existing file
        self.readRecipe(fileName)
    
    def readRecipe(self, fileName):
        # This is the typical way to create the reipe class, from an existing file
        try:
            self.Parameters = {}
            
            with open(fileName, 'r') as file:
                lines = file.readlines()
                
                # If the file is a valid recipe, the first item should contain #Name_of_Engineer
                line = lines[0].split()
                if(line[0] != '#Name_of_Engineer'):
                    print('fileName: ' + fileName + ' is not valid')
                    return()
                
                # Ok, the file looks valid, get the first three lines
                # It looks like the values are optional
                if len(line) > 1:
                    self.Name_of_Engineer = line[1]
                else:
                    self.Name_of_Engineer = ''
                    
                line = lines[1].split()
                if len(line) > 1:
                    self.Implanter_ID = line[1]
                else:
                    self.Implanter_ID = ''
                
                line = lines[2].split()
                if len(line) > 1:
                    self.Species = line[1]
                else:
                    self.Species = ''
                    
                # Let's just assume the date time format stays in two fields
                line = lines[3].split()
                self.Date_Created = line[1] + '  ' + line[2]
                line = lines[4].split()
                self.Date_Last_Modified = line[1] + '  ' + line[2]
                
                # The rest of the lines have parameters
                for line in lines[5:]:
                    contents = line.split()
                    tmpParameter = Parameter(contents[1], contents[2], contents[3], contents[4])
                    self.Parameters[contents[0]] = tmpParameter
                
        except Exception as e:
            print(f'An error occurred: {e}')
            return
        
    def writeRecipe(self, fileName):
        # This is the typical way to create the reipe class, from an existing file
        try:
            
            with open(fileName, 'w') as file:
                
                # Write out the header rows
                file.write('%-30s %s\n' % ("#Name_of_Engineer", self.Name_of_Engineer))
                print(self.Name_of_Engineer)
                file.write('%-30s %s\n' % ("#Implanter_ID", self.Implanter_ID))
                print(self.Implanter_ID)
                file.write('%-30s %s\n' % ("#Species", self.Species))
                print(self.Species)
                file.write('%-30s %s\n' % ("#Date_Created", self.Date_Created))
                print(self.Date_Created)
                file.write('%-30s %s\n' % ("#Date_Last_Modified", self.Date_Last_Modified))
                print(self.Date_Last_Modified)
                
                # Now write out the parameter data
                parameterNames = self.Parameters.keys()
                for parameter in parameterNames:
                    file.write('%-25s %15s %15s %5s %5s \n' % (parameter, self.Parameters[parameter].LowerLimit, 
                                                                 self.Parameters[parameter].UpperLimit, 
                                                                 self.Parameters[parameter].Warning, 
                                                                 self.Parameters[parameter].Interlock))
                    print(parameter)
                
        except Exception as e:
            print(f'An error occurred: {e}')
            return
    
    def __repr__(self):
        # return f"Person(name={self.name}, age={self.age}, email={self.email})"
        pass

if __name__ == "__main__":
    
    # Hmm, just found out that Python doesn't support to methods with different arguments, 
    # so you can't have two __inits__, the second one overwrites the first.
    # recipe0 = Recipe()
    
    inputPath = 'C:/Users/dmros/OneDrive/Documents/GitHub/DataFlow/Recipes/'
    outputPath = 'C:/Users/dmros/OneDrive/Documents/GitHub/DataFlow/Recipes2/'
    # path = r'C:\Users\dmros\Downloads\AOC-1E15-70-H2'
    # fileName = 'ADV-4-B-1E15-50K'
    
    for fileName in os.scandir(inputPath):
        
        tmpRecipe = Recipe(fileName)
        tmpRecipe.writeRecipe(outputPath + fileName.name)
        
    # recipe = Recipe(inputPath + fileName)
    # recipe.writeRecipe(outputPath + fileName)
    
    # print(recipe.Date_Created)
    # parameterNames = recipe.Parameters.keys()
    # for parameter in parameterNames:
    #     tmpStr = parameter + ': LowerLimit = ' + str(recipe.Parameters[parameter].LowerLimit)
    #     print(tmpStr)
