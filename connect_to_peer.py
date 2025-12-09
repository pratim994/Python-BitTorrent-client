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


def recieve_message(self):
    try:
        length_data = self._recv_exact(4)
        length = struct.unpack(">I", length_data)

        if length == 0:
            return None, None
        

        msg_id_data = self._recv_exact(1)
        msg_id = struct.unpack("B", msg_id_data)[0]

        payload = b''
        if length >1:
            payload =  self._recv_exact(length-1)
        return msg_id, payload
    except socket.timeout:
        return None, None
    except Exception as e:
        print(f"error recieving message :{e}")
        return None, None

def handle_msg(self,mag_id, payload):
        if msg_id is None:
            return None

        elif msg_id == 0:
            self.peer_choking = True
            print(f"peer {self.ip}:{self.port}:choked us")

        elif msg_id == 1:
            self.peer_choking = False
            print(f"peer {self.ip}:{self.port}: unchoked us")

        elif msg_id == 2:
            self.peer_interested = True

        
        elif msg_id == 3:
            self.peer_interested = False
        
        elif msg_id == 4:
            piece_index =  struct.unpack(">I", payload)[0]
            print(f"peer has piece {piece_index}")

        elif msg_id == 5:
            self.bitfield = payload 
            print(f"bitfield recieved from {self.ip}:{self.port} ({len(payload)}bytes)")

        elif msg_id == 7:
            index = struct.unpack(">I", payload[0:4])[0]
            begin = struct.unpack(">I", payload[4:8])[0]
            block = payload[8:]
            print(f"Recieved piece {index}, offset{block}, {len(block)}bytes")
            return('piece', index, begin, block)
  return None


 def has_piece(self,piece_index):
        if self.bitfield is None:
            return False

        byte_index =  piece_index
        bit_index = 7-(piec_index % 8)
        if byte_index >= len(self.bitfield):
                return False
        return bool((self.bitfield[byte_index]>>bit_index)&1)


def close(self):
    if self.socket:
        self.socket.close()


def download_piece(peer,piece_index,piece_length,piece_hash,block_size=16384):
    piece_data = {}
    max_attempts = 50

    for _in range(max_attempts):
        msg_id, payload = peer.recieve_message()
        if msg_id is not None:
            result = peer.handle_messsage(msg_id, payload)
            if result and result[0] == 'piece':
                -,idx, begin,block = result
                if idx == piece_index:
                    piece_data[begin] = block

        if not peer.has_piece(piece_index):
            print(f"piece doesn't exist saar {piece_index}")
            return None
        
        if not peer.interested:
                peer.send_interested()


        while peer.peer_choking:
            msg_id, payload  = peer.recieve_message()
            if msg_id is not None:
                peer.handle_message(msg_id, payload)
            time.sleep(0.1)

        print(f"Downloading piece {piece_index}({piece_length}, bytes)")

        for begin in range( 0, piece_length, block_size):
            length = min(block_size,piece_length-begin)
            peer.send_request(piece_index,begin,length)
        

        piece_data = {}
        timeout_counter = 0
        max_timeout = 100

        while len(piece_data)*block_size < piece_length and timeout_counter <max_timeout :
            msg_id , payload = peer.recieve_message()


            if msg_id is None:
                timeout_counter += 1
                    time.sleep(0.1)
                    continue
                    








def download_from_peers(torrent_file_path,peers, output_file):
