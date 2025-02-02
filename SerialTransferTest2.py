# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:20:41 2025

@author: Dennis.Rossman
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 13:23:05 2025

@author: dmros
"""

import time
from pySerialTransfer import pySerialTransfer as txfer


if __name__ == '__main__':
    try:
        link = txfer.SerialTransfer('COM11')
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        
        packetID = 0
        
        while True:
            send_size = 0
            
            ###################################################################
            # Send a list
            ###################################################################
            byteList = bytes([22, 22, 22, 1, 3, 20, 23, 255])
            list_size = link.tx_obj(byteList, 0, byte_format='@', val_type_override='c')
            print(list_size)
            
            send_size += list_size
            # print("Int size is {}".format(int_size))
            
            ###################################################################
            # Transmit all the data to send in a single packet
            ###################################################################
            link.send(send_size, packetID)
            packetID = packetID + 1
            if(packetID > 255):
                packetID = 0
            
            ##################################################### ##############
            # Wait for a response and report any errors while receiving packets
            ###################################################################
            while not link.available():
                # A negative value for status indicates an error
                if link.status < 0:
                    if link.status == txfer.Status.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.Status.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.Status.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status.name))
            
            ###################################################################
            # Parse response list
            ###################################################################
            rec_list_  = link.rx_obj(obj_type=type(byteList),
                                     obj_byte_size=list_size)
            
            ###################################################################
            # Display the received data
            ###################################################################
            print('SENT: {}'.format(byteList))
            print('RCVD: {}'.format(rec_list_))
            print(' ')
    
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass