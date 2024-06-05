# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 G. Yoder for Steel City Codes Denver
#
# SPDX-License-Identifier: MIT
"""
`adafruit_4x7_segment_display`
================================================================================

A library that can run a multiplexed 4x7 segment display without any external IC's for CircuitPython. Intended for education and teaching.


* Author(s): G. Yoder, Laiq Sorrell

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/gyoder/Adafruit_CircuitPython_4x7_Segment_Display.git"

import time
import board
import digitalio
import analogio


class SevenSegmentModule:
    
    def __init__(self, pin_list):

      self.digit1 = digitalio.DigitalInOut(pin_list[11])
      self.digit1.direction = digitalio.Direction.OUTPUT
      self.digit1.value = False

      self.digit2 = digitalio.DigitalInOut(pin_list[8])
      self.digit2.direction = digitalio.Direction.OUTPUT
      self.digit2.value = True

      self.digit3 = digitalio.DigitalInOut(pin_list[7])
      self.digit3.direction = digitalio.Direction.OUTPUT
      self.digit3.value = True

      self.digit4 = digitalio.DigitalInOut(pin_list[5])
      self.digit4.direction = digitalio.Direction.OUTPUT
      self.digit4.value = True

      self.displays = [self.digit1, self.digit2, self.digit3, self.digit4]


      self.TOP = digitalio.DigitalInOut(pin_list[10])
      self.UPPERLEFT = digitalio.DigitalInOut(pin_list[9])
      self.UPPERRIGHT = digitalio.DigitalInOut(pin_list[6])
      self.LOWERLEFT = digitalio.DigitalInOut(pin_list[0])
      self.LOWERRIGHT = digitalio.DigitalInOut(pin_list[3])
      self.MIDDLE = digitalio.DigitalInOut(pin_list[4])
      self.BOTTOM = digitalio.DigitalInOut(pin_list[1])

      self.TOP.direction = digitalio.Direction.OUTPUT
      self.UPPERLEFT.direction = digitalio.Direction.OUTPUT
      self.UPPERRIGHT.direction = digitalio.Direction.OUTPUT
      self.LOWERLEFT.direction = digitalio.Direction.OUTPUT
      self.LOWERRIGHT.direction = digitalio.Direction.OUTPUT
      self.MIDDLE.direction = digitalio.Direction.OUTPUT
      self.BOTTOM.direction = digitalio.Direction.OUTPUT
      self.numberMap = {
          "0": [self.TOP, self.UPPERLEFT,  self.UPPERRIGHT,   self.LOWERLEFT,  self.LOWERRIGHT, self.BOTTOM],
          "1": [self.UPPERRIGHT, self.LOWERRIGHT],
          "2": [self.TOP, self.UPPERRIGHT, self.MIDDLE, self.LOWERLEFT, self.BOTTOM],
          "3": [self.TOP, self.UPPERRIGHT, self.LOWERRIGHT, self.MIDDLE, self.BOTTOM],
          "4": [self.UPPERLEFT, self.MIDDLE, self.UPPERRIGHT, self.LOWERRIGHT],
          "5": [self.TOP, self.UPPERLEFT, self.LOWERRIGHT,  self.MIDDLE,     self.BOTTOM],
          "6": [self.TOP, self.UPPERLEFT, self.LOWERLEFT,  self.LOWERRIGHT,  self.MIDDLE,     self.BOTTOM],
          "7": [self.TOP, self.UPPERRIGHT, self.LOWERRIGHT],
          "8": [self.TOP, self.UPPERLEFT, self.UPPERRIGHT, self.LOWERLEFT, self.LOWERRIGHT, self.MIDDLE, self.BOTTOM],
          "9": [self.TOP, self.UPPERLEFT, self.UPPERRIGHT, self.LOWERRIGHT, self.MIDDLE, self.BOTTOM],
          "A": [self.TOP, self.UPPERLEFT, self.UPPERRIGHT, self.MIDDLE, self.LOWERLEFT, self.LOWERRIGHT],
          "B": [self.UPPERLEFT, self.LOWERLEFT, self.LOWERRIGHT, self.MIDDLE, self.BOTTOM],
          "C": [self.TOP, self.UPPERLEFT, self.LOWERLEFT, self.BOTTOM],
          "D": [self.UPPERRIGHT, self.LOWERRIGHT, self.LOWERLEFT, self.BOTTOM, self.MIDDLE],
          "E": [self.TOP, self.UPPERLEFT, self.LOWERLEFT, self.MIDDLE, self.BOTTOM],
          "F": [self.TOP, self.UPPERLEFT, self.MIDDLE, self.LOWERLEFT],
          "G": [self.TOP, self.UPPERLEFT, self.LOWERLEFT, self.LOWERRIGHT, self.BOTTOM],
          "H": [self.UPPERLEFT, self.UPPERRIGHT, self.MIDDLE, self.LOWERLEFT, self.LOWERRIGHT],
          "I": [self.UPPERRIGHT, self.LOWERRIGHT],
          "J": [self.UPPERRIGHT, self.LOWERRIGHT, self.LOWERLEFT, self.BOTTOM],
          "K": [self.UPPERLEFT, self.MIDDLE, self.LOWERLEFT, self.LOWERRIGHT, self.UPPERRIGHT],
          "L": [self.UPPERLEFT, self.LOWERLEFT, self.BOTTOM],
          "M": [self.TOP, self.UPPERLEFT, self.UPPERRIGHT, self.LOWERLEFT, self.LOWERRIGHT],
          "N": [self.TOP, self.UPPERLEFT, self.UPPERRIGHT, self.LOWERLEFT, self.LOWERRIGHT],
          "O": [self.TOP, self.UPPERLEFT, self.UPPERRIGHT, self.LOWERLEFT, self.LOWERRIGHT, self.BOTTOM],
          "P": [self.TOP, self.UPPERLEFT, self.UPPERRIGHT, self.MIDDLE, self.LOWERLEFT],
          "Q": [self.TOP, self.UPPERLEFT, self.UPPERRIGHT, self.LOWERLEFT, self.LOWERRIGHT, self.BOTTOM, self.LOWERLEFT],
          "R": [self.LOWERLEFT, self.UPPERLEFT, self.TOP, self.UPPERRIGHT],
          "S": [self.TOP, self.UPPERLEFT, self.LOWERRIGHT, self.MIDDLE, self.BOTTOM],
          "T": [self.UPPERLEFT, self.LOWERLEFT, self.MIDDLE, self.BOTTOM],
          "U": [self.UPPERLEFT, self.UPPERRIGHT, self.LOWERLEFT, self.LOWERRIGHT, self.BOTTOM],
          "V": [self.UPPERLEFT, self.LOWERLEFT, self.LOWERRIGHT, self.BOTTOM],
          "W": [self.UPPERLEFT, self.LOWERLEFT, self.LOWERRIGHT, self.UPPERRIGHT, self.BOTTOM],
          "X": [self.UPPERLEFT, self.UPPERRIGHT, self.MIDDLE, self.LOWERLEFT, self.LOWERRIGHT],
          "Y": [self.UPPERLEFT, self.UPPERRIGHT, self.MIDDLE, self.LOWERRIGHT, self.BOTTOM],
          "Z": [self.TOP, self.UPPERRIGHT, self.MIDDLE, self.LOWERLEFT, self.BOTTOM],
          " ": []
      }
    


    #self.numbers = [zero, one, two, three, four, five, six, seven, eight, nine]

    def setDisplayIndex(self, index):
        for item in self.displays:
            item.value = True
        self.displays[index].value = False
        
    def displayFour(self, strNum):
        listOfChars = list(strNum)        
        stringIndex = 0
        for char in listOfChars:
            self.setDisplayIndex(stringIndex)
            for item in self.numberMap[char]:
                item.value = True
            time.sleep(0.004)
            for item in self.numberMap[char]:
                item.value = False
            stringIndex += 1
    # IT CANNOT display K, M, V, W, and X, Q
    def display(self, strNum, duration):

      strNum = str(strNum)
      strNum = strNum.upper()
      length = len(strNum)
      start = time.time()
      if length <= 4:
          while time.time() - start < duration:
              self.displayFour(strNum)
      else:
          while time.time() - start < duration:
            for i in range(0, len(strNum)):
                second_start = time.time()
                while time.time() - second_start < .15:
                    four_letter_string = strNum[i:i+4]
                    self.displayFour(four_letter_string)
        