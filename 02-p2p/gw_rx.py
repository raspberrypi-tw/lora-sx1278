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
import time
import json
import packer
import sys
import numpy as np
sys.path.insert(0, '../../pySX127x')        
from SX127x.LoRa import *
from SX127x.board_config import BOARD

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self._id = "GW_01"

    def on_rx_done(self):
        print '----------------------------------'
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = ''.join([chr(c) for c in payload])
        print "Time:", str(time.ctime())
        print "Rawinput:", payload

        try:
            _length, _data = packer.Unpack_Str(data)
            print "Time:", str(time.ctime())
            print "Length:", _length
            print "Receive:", _data
        except:
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print "Non-hexadecimal digit found..."
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print "Receive:", data

        #sleep(0.5)
        #self.set_mode(MODE.SLEEP)
        #self.reset_ptr_rx()
        #######
        #sleep(1)
        #######

        for i in range(3):
            self.set_mode(MODE.STDBY)
            self.clear_irq_flags(TxDone=1)
            data = {"id":self._id, "data":packer.ACK}
            _length, _ack = packer.Pack_Str( json.dumps(data) )
            ack = [int(hex(ord(c)), 0) for c in _ack]
            print "ACK:", self._id
            self.write_payload(ack)                                       
            self.set_mode(MODE.TX)

            # ALOHA(1~3)
            t = i*2 + np.random.random() * 3
            sleep(t)

        self.set_mode(MODE.RXCONT)


    def start(self):
        print 'start to receive...'
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)

#
# initialize sx1278
# 
BOARD.setup()

lora = LoRaRcvCont()
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
lora.set_freq(433)
lora.set_spreading_factor(7)  # 7-12
lora.set_bw(7)  # 0-9 
lora.set_coding_rate(1)  # 1-4         
lora.clear_irq_flags(RxDone=1)
print(lora)

try: 
    lora.start()
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()                    
    print "exit()"

