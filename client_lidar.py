#!/usr/bin/env python3

import serial
import time
from collections import deque
from serial.serialutil import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, parity=PARITY_NONE, bytesize=EIGHTBITS, stopbits=STOPBITS_ONE)

Q = deque([0x59]*9)
while(True):
  b = ser.read()
  Q.rotate(-1)
  Q[0] = ord(b)
  if Q[0] == 0x59 and Q[1] == 0x59:
    #Dist_L Dist_H Strength_L Strength_H Temp_L Temp_H Checksum
    dist = (Q[3] * 256) + Q[2]
    strength = (Q[5] * 256) + Q[4]
    temp = (Q[7] * 256) + Q[6]
    checksum = sum([Q[i] for i in range(8)]) % 256
    if checksum == Q[8]:
      print(dist, strength, temp)
    else:
      print('Checksum is wrong')
