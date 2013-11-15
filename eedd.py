import sys
import time

import serial

__version__ = "dev"

_READ_BYTE_COMMAND = chr(0x00)
_READ_MANY_BYTES_COMMAND = chr(0xFF)
_WRITE_BYTE_COMMAND = chr(0x0F)
_WRITE_MANY_BYTES_COMMAND = chr(0xF0)
_CLEAR_CHIP_COMMAND = chr(0x33)
_PARK_COMMAND = chr(0xDB)
_ERROR_INDICATOR = chr(0xCC)

class EepromInterface:

    def __init__(self, port, baud=57600):

        self.ser = serial.Serial(port, baud)
        time.sleep(2)

    def close(self):
        self.ser.close()

    def handle_verification(self):
        verification_byte = self.ser.read(timeout=5.0)
        if not verification_byte:
            raise Exception("Communication with serial device timed out.  Protocol violation?")
        elif verification_byte == _ERROR_INDICATOR:
            raise Exception("Programmer sent error indicator.  Protocol violation?")

    def read_byte(self, address):

        addlow = chr(address & 0xFF)
        addhi = chr(address >> 8)
        self.ser.write(_READ_BYTE_COMMAND)
        self.ser.write(addlow)
        self.ser.write(addhi)
        byte = self.ser.read()
        return byte

    def read_bytes(self, start_address, count):

        start_addlow = chr(start_address & 0xFF)
        start_addhi = chr(start_address >> 8)
        self.ser.write(_READ_MANY_BYTES_COMMAND)
        self.ser.write(start_addlow)
        self.ser.write(start_addhi)
        self.ser.write(chr(count))
        return self.ser.read(count)
 
    def write_byte(self, address, data):

        addlow = chr(address & 0xFF)
        addhi = chr(address >> 8)
        self.ser.write(_WRITE_BYTE_COMMAND)
        self.ser.write(addlow)
        self.ser.write(addhi)
        self.ser.write(data)
        self.handle_verification()

    def write_bytes(self, start_address, data):

        start_addlow = chr(start_address & 0xFF)
        start_addhi = chr(start_address >> 8)
        self.ser.write(_WRITE_MANY_BYTES_COMMAND)
        self.ser.write(start_addlow)
        self.ser.write(start_addhi)
        self.ser.write(chr(len(data)))
        self.ser.write(data)
        self.handle_verification()

    def clear_chip(self):
        self.ser.write(_CLEAR_CHIP_COMMAND)
        self.handle_verification()

    def park(self):
        self.ser.write(_PARK_COMMAND)
        self.handle_verification()
