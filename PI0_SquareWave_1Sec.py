from pysmu import Session, Mode
import time


import time
def PIO_Squarewave():

    session = Session()

    devx = session.devices[0]   # device ID for 1st M1000 in list
    # assign digital pins
    PIO_0 = 28
    DevID = 0x41
    i= 0
    try:
        Frequency = int(input("Enter the Clock Frequency (Hz) less than 10 Hz for better visualisation \t:\t"))
    except ValueError:
        Frequency = 1
        print("Default Frequency of 1 Hz are used")

    delay_time = 1.0 / Frequency
    while(True):
        # set PIO1 high\\
        devx.ctrl_transfer(0x41, 0x51, PIO_0, 0, 0, 0, 10)
        devx.set_led(i)
        print("Turn ON")
        time.sleep(delay_time)
        devx.ctrl_transfer(0x41, 0x50, PIO_0, 0, 0, 0, 200)
        i = i+1
        devx.set_led(i)

        time.sleep(delay_time)
        print("Turn OFF")
        
        if(i== 8):
            i = 0
            
            
PIO_Squarewave()