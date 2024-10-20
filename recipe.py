# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import datetime as datetime

class Parameter:
    # Used in the recipe
    def __init__(self, lower, upper, warning, interlock):        
        self.LowerLimit = lower
        self.UpperLimit = upper
        self.Warning = warning
        self.Interlock = interlock
        
# Define a simple class
class Recipe:
    def __init__(self):
        # What does DataFlow use for a brand new / empty recipe?
        self.Name_of_Engineer = ''
        self.Implanter_ID = ''
        self.Species = ''
        self.Date_Created = datetime.now().strftime('%m-%d-%Y %H:%M:%S') 
        self.Date_Last_Modified = datetime.now().strftime('%m-%d-%Y %H:%M:%S') 
        
        # Let's try a dictionary of parameters.  The values of the parameter
        # can be looked up by the parameter's name.
        self.Parameters = {}
        
        # First create a parameter object 
        dose = Parameter(1.0e15, 1.0e15, 1, 1)        
        # Then append the key / value pair
        self.Parameters['Dose'] = dose
        
        energy = Parameter(69.0, 71.0, 1, 1)
        self.Parameters['Beam_Energy'] = energy
        
        amu = Parameter(1.600, 2.600, 1, 1) 
        self.Parameters['AMU'] = amu
        
        beam_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Beam_Current'] = beam_current
        
        mag_current = Parameter(0.0, 0.0, 0, 0)
        self.Parameters['Magnetic_Current'] = mag_current
        
        wafer_size = Parameter(3, 3, 1, 1)
        self.Parameters['Wafer_Size'] = wafer_size
        
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
                self.Date_Created = line[1] + ' ' + line[2]
                line = lines[4].split()
                self.Date_Last_Modified = line[1] + ' ' + line[2]
                
                # The rest of the lines have parameters
                for line in lines[5:]:
                    contents = line.split()
                    tmpParameter = Parameter(contents[1], contents[2], contents[3], contents[4])
                    self.Parameters[contents[0]] = tmpParameter
                
        except Exception as e:
            print(f'An error occurred: {e}')
            return
    
    def __repr__(self):
        # return f"Person(name={self.name}, age={self.age}, email={self.email})"
        pass


# Example usage
if __name__ == "__main__":
    
    # Hmm, just found out that Python doesn't support to methods with different arguments, 
    # so you can't have two __inits__, the second one overwrites the first.
    # recipe0 = Recipe()
    
    path = r'C:\Users\dmros\Downloads\AOC-1E15-70-H2'
    recipe = Recipe(path)
    
    print(recipe.Date_Created)
    parameterNames = recipe.Parameters.keys()
    for parameter in parameterNames:
        tmpStr = parameter + ': LowerLimit = ' + str(recipe.Parameters[parameter].LowerLimit)
        print(tmpStr)
