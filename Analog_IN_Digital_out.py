        
# Iterate through various random RGB LED states for all connected devices.

from signal import signal, SIG_DFL, SIGINT
import sys
import time
from random import randrange

from pysmu import Session, LED
from pysmu import *


if __name__ == '__main__':
    # don't throw KeyboardInterrupt on Ctrl-C
    signal(SIGINT, SIG_DFL)
    print("Hello im in main")
    
    #session = Session()
    session = Session(ignore_dataflow=True, queue_size=50)
    print(session)
    session.devices[0].set_led(5)
    print("Hello im in main")
    if not session.devices:
        print('No Device found')
        #sys.exit(1)
    #session = Session(ignore_dataflow=True, queue_size=50)
    print("Hello",session.devices)
            
    

    dev = session.devices[0]
    print(f"Device detail\n{dev}")
    CHA = dev.channels['A']    # Open CHA
    CHA.mode = Mode.HI_Z # Put CHA in Hi Z mode
    #CHB = devx.channels['B']    # Open CHB
    #CHB.mode = Mode.HI_Z # Put CHB in Hi Z mode
    ADsignal1 = []
    n_sample = 50
    PIO_0 = 28
    DevID = 0x41
    Frequency = int(input("Enter the Clock Frequency (Hz) less than 10 Hz for better visualisation \t:\t"))
    delay_time = 1.0 / Frequency
    while True:
        val = randrange(0, 8)
        #session = Session(ignore_dataflow=True, queue_size=50)
        #print("Hello",session.devices)
        #if not session.devices:
        #    print('no device found')
        #   sys.exit(1)
        DCVA_H = 0.0
        DCVA_L = 0.0
        #val = 5
        
        for dev in session.devices:
            if not session.continuous:
                session.flush()
                session.start(0)
                #print "starting session inside analog in"
                time.sleep(0.2)
            dev.set_led(val)
            print('reading...')
            dev.ctrl_transfer(0x41, 0x51, PIO_0, 0, 0, 0, 10)
            time.sleep(delay_time)
            #ADsignal1 = dev.read(n_sample, -1, True) # get 20 readings
            dev.ctrl_transfer(0x41, 0x50, PIO_0, 0, 0, 0, 10)
            time.sleep(delay_time)    
            ADsignal1 = dev.read(n_sample, -1, True) # get 20 readings
            print(len(ADsignal1[0][0]))
            for index in range(n_sample): # calculate average
                #print(f"cumulative value:\t\t {DCVA}")
                if(ADsignal1[index][0][0]>2):
                    DCVA_H += ADsignal1[index][0][0] # Sum for average CA voltage [Sample index][Channel A[0]/B[1]][Voltage[0]/current[1]]
                else:
                    DCVA_L += ADsignal1[index][0][0] # Sum for average CA voltage [Sample index][Channel A[0]/B[1]][Voltage[0]/current[1]]
                
            print(' {0:.4f}, {0:.4f} '.format(DCVA_H,DCVA_L))# format with 4 decimal places
            time.sleep(0.4)
            #print(f"Array of ADsignal \n{ADsignal1}")
            #time.sleep(.2)
            
          



main()          
            
