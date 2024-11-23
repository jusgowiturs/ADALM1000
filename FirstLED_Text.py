
# Iterate through various random RGB LED states for all connected devices.

from signal import signal, SIG_DFL, SIGINT
import sys
import time
from random import randrange

from pysmu import Session, LED


if __name__ == '__main__':
    # don't throw KeyboardInterrupt on Ctrl-C
    signal(SIGINT, SIG_DFL)

    session = Session()
    print("Hello",session.devices)
            
    if not session.devices:
        sys.exit(1)

    while True:
        val = randrange(0, 8)
        #val = 5
        for dev in session.devices:
            dev.set_led(val)
        time.sleep(.25)