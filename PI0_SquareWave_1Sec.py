from pysmu import Session
import time

def main():

    session = Session()

    devx = session.devices[0]   # device ID for 1st M1000 in list
    # assign digital pins
    PIO_0 = 28
    DevID = 0x40
    i= 0
    try:
        Frequency = int(input("Enter the Clock Frequency (Hz) less than 10 Hz for better visualisation \t:\t"))
    except ValueError:
        Frequency = 1
        print("Default Frequency of 1 Hz are used")

    delay_time = 1.0 / Frequency
    while(True):
        # set PIO1 high\\
        #dev
        #Source     :       https://www.beyondlogic.org/usbnutshell/usb6.shtml
        #ctrl_transfer	(	
        #   unsigned 	bmRequestType,              #	the request type field for the setup packet   
        #   unsigned 	bRequest,                   #   the request field for the setup packet
        #   unsigned 	wValue,                     #   the value field for the setup packet
        #   unsigned 	wIndex,                     #   the index field for the setup packet
        #   unsigned char * 	data,               #   a suitably-sized data buffer for either input or output (depending on direction bits within bmRequestType)
        #   unsigned 	wLength,                    #   the length field for the setup packet. The data buffer should be at least this size.
        #   unsigned 	timeout                     #   timeout (in milliseconds) that this function should wait before giving up due to no response being received. For an unlimited timeout, use value 0.
        #   )	
        devx.ctrl_transfer(0x40, 0x51, PIO_0, 0, 0, 0, 100)
        # bmRequestType is   0x41 which shows host to device connection, ventor type , Interface
        # bRequest      is   0x51 states Logic High
        # wValue        is   PIO_0 pin number 28
        # timeout       is   100 ms
        devx.set_led(i)
        print("Turn ON")
        time.sleep(delay_time)
        devx.ctrl_transfer(0x40, 0x50, PIO_0, 0, 0, 0, 200)
        i = i+1
        devx.set_led(i)

        time.sleep(delay_time)
        print("Turn OFF")
        
        if(i== 8):
            i = 0


main()

            
