from signal import signal, SIG_DFL, SIGINT
import sys
import time
from random import randrange

from pysmu import Session, LED, Mode
from pysmu import *

from joblib import Parallel, delayed
from concurrent.futures import ThreadPoolExecutor

class ADALM1000():
  def __init__(self,n_sample = 50):
    self.session = Session(ignore_dataflow=True, queue_size=n_sample)
    
    

    if not self.session.devices:
        print('No Device found')
        sys.exit(1)
    self.n_sample = n_sample
    self.session.flush()

    self.session.start(0)
    self.dev = self.session.devices[0]

    CHB = self.dev.channels['A']    # Open CHA
    CHB.mode = Mode.HI_Z # Put CHA in Hi Z mode
    self.PIO_0 = 28
    self.PIO_3 = 3
    time.sleep(0.2)

  def ctrl_transfer_device(self,delay_time):
    print('Square Generating...')
    for i in range(delay_time):
      
      self.dev.ctrl_transfer(0x40, 0x51, self.PIO_0, 0, 0, 0, 10)
      print(f'Pin 1 Status is {self.dev.ctrl_transfer(0xC0,  0x91, self.PIO_3, 0, 0, 1, 100)}')
      self.dev.set_led(3)
      self.dev.ctrl_transfer(0x40, 0x50, self.PIO_0, 0, 0, 0, 10)
      time.sleep(delay_time)
      print(f'Pin 1 Status is {self.dev.ctrl_transfer(0xC0,  0x91, self.PIO_3, 0, 0, 1, 100)}')
      self.dev.set_led(7)
      time.sleep(delay_time)

  def clear_Session(self):
    self.session.flush()
    
    
  def read_device(self):
    print("reading Analog")
    
    self.ADsignal1 = self.dev.read(self.n_sample, -1, True)  # Get readings
    #print(self.ADsignal1)
    self.process_signals()
  def process_signals(self):
    DCVA_H = 0
    DCVA_L = 0
    print(f"Processing....\nLength of Analog input {len(self.ADsignal1)}")
    for index in range(self.n_sample):  # Calculate average
        print(f'{index}: {self.ADsignal1[index][0][0]}')
        if self.ADsignal1[index][0][0] > 2:
            DCVA_H += self.ADsignal1[index][0][0]  # Sum for high voltage
        else:
            DCVA_L += self.ADsignal1[index][0][0]  # Sum for low voltage
    DCVA_H /= self.n_sample
    DCVA_L /= self.n_sample 
    print( DCVA_H, DCVA_L)
    self.clear_Session()
    return DCVA_H, DCVA_L
    


#X = ADALM1000(n_sample = 1000 )
#print(X.dev)
#for i in range(5):
#    X.ctrl_transfer_device(1)
#    X.read_device()
#print(X.process_signals())
#def main():
#    X = ADALM1000(n_sample=1000)
#
#    # Use joblib to run both tasks in parallel
#    Parallel(n_jobs=2)(
#        delayed(X.ctrl_transfer_device)(1),  # Run ctrl_transfer_device(1)
#        delayed(X.read_device)()              # Run read_device()
#    )
def main():
    X = ADALM1000(n_sample=20)
    
    # Use ThreadPoolExecutor to run the functions in parallel
    with ThreadPoolExecutor() as executor:
        # Submit both tasks to the executor
        future_read = executor.submit(X.read_device)  # Run read_device()
        future_ctrl = executor.submit(X.ctrl_transfer_device, 1)  # Run ctrl_transfer_device(1)
        

        # Wait for both tasks to complete and get their results (if needed)
        future_ctrl.result()  # Waits for ctrl_transfer_device to finish
        future_read.result()  # Waits for read_device to finish
        X.clear_Session()

if __name__ == "__main__":
    main()
