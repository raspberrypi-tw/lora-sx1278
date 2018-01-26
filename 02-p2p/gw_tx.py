#!/usr/bin/env python

""" A simple continuous receiver class. """

# Copyright 2015 Mayer Analytics Ltd.
#
# This file is part of pySX127x.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.

from time import sleep
import json
import packer
import time
import sys
sys.path.insert(0, '../../pySX127x')        
from SX127x.LoRa import *
from SX127x.board_config import BOARD

class LoRaBeacon(LoRa):
    def __init__(self, verbose=False):
        super(LoRaBeacon, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self._id = "NODE_01"
        self.rx_done = False

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = ''.join([chr(c) for c in payload])

        if data is not None and len(data):
            try:
                _length, _data = packer.Unpack_Str(data)
                print "Time:", str(time.ctime()) 
                #print "Rawinput:", payload
                print "Receive:", _data
            except:
                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
                print "Non-hexadecimal digit found..."
                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
                print "Receive:", data 

        self.set_mode(MODE.SLEEP)
        #self.reset_ptr_rx()
        #self.set_mode(MODE.RXCONT)
        self.rx_done = True


    def start(self):
        while True:
            print '----------------------------------'      

            try:
                rawinput = raw_input(">>> ")
            except KeyboardInterrupt:
                lora.set_mode(MODE.SLEEP)
                BOARD.teardown()
                print "exit()"


            if len(rawinput) < 200:
                self.set_mode(MODE.STDBY)
                self.clear_irq_flags(TxDone=1)

                data = {"id":self._id, "data":rawinput}
                _length, _payload = packer.Pack_Str( json.dumps(data) )
                data = [int(hex(ord(c)), 0) for c in _payload]
                print "data", _payload
                print "Rawinput:", data

                sleep(1)
                self.write_payload(data)                                       
                self.set_mode(MODE.TX)

                sleep(.5)
                self.set_mode(MODE.SLEEP)
                self.set_dio_mapping([0] * 6)
                sleep(.5)
                self.set_mode(MODE.STDBY)
                sleep(.5)
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT)

                for _ in range(t):
                    sleep(.1)

                    if self.rx_done == True:
                        self.rx_done = False
                        break


#    
# initialize sx1278
#    
BOARD.setup()

sf = 7
bw = 7
cr = 1
t = sf * bw * cr

lora = LoRaBeacon()
lora.set_mode(MODE.SLEEP)
lora.set_pa_config(pa_select=1)
lora.set_freq(433)
lora.set_spreading_factor(sf)  # 7-12
lora.set_bw(bw)  # 0-9
lora.set_coding_rate(cr)  # 1-4
lora.clear_irq_flags(TxDone=1)
print(lora)

try:
    lora.start()
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
    print "exit()"
