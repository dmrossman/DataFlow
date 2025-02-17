# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:52:55 2025

@author: dmros
"""

from time import sleep
from pySerialTransfer import pySerialTransfer as txfer
from pySerialTransfer.pySerialTransfer import Status


class Struct:
    z = ''
    y = 0.0


arr = ''


if __name__ == '__main__':
    try:
        testStruct = Struct
        link = txfer.SerialTransfer('COM6')
        
        link.open()
        sleep(5)
    
        while True:
            if link.available():
                recSize = 0
                
                testStruct.z = link.rx_obj(obj_type='c', start_pos=recSize)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['c']
                
                testStruct.y = link.rx_obj(obj_type='f', start_pos=recSize)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['f']
                
                arr = link.rx_obj(obj_type=str,
                                  start_pos=recSize,
                                  obj_byte_size=5)
                recSize += len(arr)
                
                print('{}{} | {}'.format(testStruct.z, testStruct.y, arr))
                
            elif link.status.value <= 0:
                if link.status == Status.CRC_ERROR:
                    print('ERROR: CRC_ERROR')
                elif link.status == Status.PAYLOAD_ERROR:
                    print('ERROR: PAYLOAD_ERROR')
                elif link.status == Status.STOP_BYTE_ERROR:
                    print('ERROR: STOP_BYTE_ERROR')
                else:
                    print('ERROR: {}'.format(link.status.name))
                
        
    except KeyboardInterrupt:
        link.close()