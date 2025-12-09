import socket 
import struct 
import hashlib
import time
from parser import bencode, bdecode

class BitTorrentPeer:
    ""handles communication with a single ballsack""

    def __init__(self, ip, port, info_hash, peer_id, timeout =5):
        self.ip = ip
        self.port = port
        self.info_hash = info_hash
        self.peer_id = peer_id
        self.timeout = timeout
        self.socket = none
        self.choked = True
        self.interested = False
        self.peer_choking = True
        self.peer_interrested =  False
        self.bitfield = none

def connect(self):
    ""establishes tcp connection to peers""
    try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.ip, self.port))
        return True
    except Exception as e:
        print(f"failed to connect to {self.ip}:{self.port}-{e}" )
        return False


def handshake(self):
    pstr = b"bittorrnet protocol"
    pstrlen = len(pstr)
    reserved  = b'\x00 '*8
    handhake_msg = struct.pack("B",pstrlen)+pstr+ reserved +self.info_hash +self.peer_id
