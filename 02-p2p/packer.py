#!/usr/bin/python
# -*- coding: UTF-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2016, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# packer.py
# A demo program for lora to send message compatible with python2/3
#
# Author : sosorry
# Date   : 10/03/2017
#

SOH  = "01"    # 0x01
ACK  = "06"    # 0x06
CRLF = "\r\n"  # 0x32 0x41 0x33 0x31

#
# pack string to customized payload
#
# payload: [SOH]    [LENGTH]   [PAYLOAD]          [CRLF]
#          4 bytes  6 bytes    length * 2 bytes   4 bytes
#
def Pack_Str(string):
    data   = string.encode("hex")
    length = len(data)

    if length < 10:
        length = str(0) + str(0) + str(length)
    elif length >= 10 and length < 100:
        length = str(0)  + str(length)
    else:
        length = str(length)

    payload = SOH + length.encode("hex") + data + CRLF
    """
    print "len:", len(payload)
    print "SOH:", SOH 
    print "hex:", length.encode("hex")
    print "data:", data
    print "CRLF:", CRLF
    print "RAW:", payload
    """

    return [length, payload]


#
# unpack payload to string
#
def Unpack_Str(string):
    soh    = string[0:1]
    #length = int((string[2:8]).decode("hex")) /2
    length = int((string[2:8]).decode("hex")) /2
    data   = (string[8:-2]).decode("hex")

    return [length, data]

