from ctypes import Structure, c_ubyte, c_ushort, c_uint32
import socket
import struct

class IP(Structure):
    _fields_ = [
        ("type", c_ubyte, 8),
        ("code", c_ubyte, 8),
        ("sum", c_ushort, 16),
        ("id", c_ushort, 16),
        ("num", c_ushort, 16),
        ("data", c_uint32, 32)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

