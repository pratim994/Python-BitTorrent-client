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

    try:
        self.socket.send(handhake_msg)
        response = self.recv_exact(68)

        resp_pstrlen = response[0]
        resp_pstr = resposne[1:20]  
        resp_reserved = resposne[20:28]
        resp_info_hash =  response[28:48]
        resp_peer_id = response[48:68]


        if resp_pstrlen != 19 or resp_pstr != pstr:
            print( f"invalid handshake from {self.ip}:{self.port}")
            return False

        if resp_info_hash !=  self.info_hash:
            print(f"info hash mismatch  from {self.ip}:{self.port}")
            return False

        print(f"handshake succesful with {self.ip}:{self.port} ")
            return True

        except Exception as e:
            print(f"handshake failed {self.ip}:{self.port}-{e}")
            return False

  def _recv_exact(self,n):
        data  = b' ' 
        while len(data)<n:
            chunk = self.socket.recv( n-len(data))
            if not chunk:
                raise ConnectionError("Connection closed by peer")
                data += chunk 
        return data

def send_interested(self):
    msg = struct.pack(">IB",1,2)
    self.socket.send(msg)
    self.interested = True
    print(f"sent to {self.ip}:{self.port}")


def send_request(self, piece_index, begin,length):
    msg = struct.pack(  ">IBII", 13,6, piece_index, begin, length)
    self.socket.send(msg)
    print(f"send requested piece {piece_index}, offset{begin}, length {length}")
    

