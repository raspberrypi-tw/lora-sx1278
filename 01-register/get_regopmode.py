#!/usr/bin/python
# -*- coding:utf-8 -*-

import spidev

spi = spidev.SpiDev()
spi.open(0, 0)

RegOpMode = 0x01
Value     = 0

# Read
ret = spi.xfer([RegOpMode & 0x7F, Value])[1]
print ret         # 128
print ret >> 7    # 1

spi.close()

