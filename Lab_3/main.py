from ctypes import Structure, c_ubyte, c_ushort, c_uint32
import socket
import struct

class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte, 8),
        ("len", c_ushort, 16),
        ("id", c_ushort, 16),
        ("offset", c_ushort, 16),
        ("ttl", c_ubyte, 8),
        ("protocol_num", c_ubyte, 8),
        ("sum", c_ushort, 16),
        ("scr", c_uint32, 32),
        ("dst", c_uint32, 32)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(selfdelf, socket_buffer=None):
        # human readable IP addresses
        self.scr_address = socket.inet_ntoa(struct.pack("<L", self.scr))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))