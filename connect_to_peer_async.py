import asyncio 
import socket 
import struct
import hashlib
import time 
from parser import bdecode, bencode
from collections import defaultdict

class AysncBitPeer:
    def __init__(self, ip, port, info_hash, peer_id, timeout=10):
        self.ip = ip
        self.port = port
        self.info_hash   = info_hash
        self.peer_id =  peer_id
        self.timeout =  timeout
        self.reader = None
        self.writer = None
        self.choked = True
        self.interested = False
        self.peer_choking =  True
        self.peer_interested = False
        self.bitfield = None
        self.connected  = False


        async def connect(self):
            try:
                self.reader, self.writer  = await asyncio.wait_for( 
                    asyncio.open_connection(self.ip, sef.port),
                    timeout= self.timeout
                )
                self.connected = True
                return True
            except Exception as e:
                print(f"failed to connect to port {self.port}:{self.ip}-{e}")
                return False

        async def handshake(self):
            pstr  = b"Bittorrent protocol"
            pstrlen = len(pstr)
            reserved = b'\x00'*8

            handshake_msg = struct.pack("B", pstrlen)+pstr+reserved+self.info_hash+self.peer_id

            try:
                self.writer.write(handshake_msg)
                await self.writer.drain()

                response = await ayncio.wait_for(
                    self.reader.readexactly(68),
                    timeout = self.timeout
                )

                resp_pstrlen = response[0]
                resp_pstr = response[1:20]
                resp_info_hash = response[28:48]

                if resp_pstrlen != 19 or resp_pstr != pstr:
                    print(f"Invalid hansdshake from {self.ip}:{self.port}")
                    return False

                if resp_info_hahs != self.info_hash :
                    print(f"Info hash mismatch from {self.ip}:{self.port}")
                    return False


                print(f"handshake successfull with {self.ip}:{self.port}")
                return True

            except Exception as e:
                print(f"Handshake failed with {self.ip}:{self.port}-{e}")
                return False

async def send_interested(self):
    msg = struct.pack(">IB", 1, 2)
    self.writer.write(msg)
    await self.writer.drain()
    self.interested = True


async def send_requested(self, piece_index, begin, length):
        msg = struct.pack(">IBIII", 13,6, piece_index, begin, length)
        self.writer.write(msg)
        await self.writer.drain()



async def recieve_message(self): 
    try:
        length_data = await asyncio.wait_for(
            self.reader.readexactly(4),
            timeout = self.timeout
        )
        length = struct.unpack("I", length_data)[0]
        if length == 0:
            return None,None


        msg_data = await asyncio.wait_for(
            self.reader.readexactly(length),
            timeout = self.timeout
        )
        msg_id = msg_data[0]
        payload = msg_data[1:] if length >1 else b''

        return msg_id, payload


    except asyncio.TimeoutError:
        return None, None
    except Exception as e:
        return None ,None

    
def handle_message(self, msg_id, payload):
    if msg_id is None:
        return None

    if msg_id  == 0:
        self.peer_choking = True

    if msg_id == 1:
        self.peer_choking = True
        print(f"Peer unchoked us {self.ip}:{self.port}")

    if msg_id ==2:
        self.peer_interested = True

    if msg_id == 3:
        self.peer_interested = True

    if msg_id == 4:
        piece_index = struct.unpack(">I", payload)[0]

    if msg_id == 5:
        self.bitfield = payload
        print(f"Recieved  bitfield from {self.ip}:{self.port} ")
    if msg_id == 7
        index = struct.unpack(">I", payload[0:4])[0]

        begin= struct.unpack(">I", paload[4:8])[0]
        block = payload[8:]
        return ('piece', index, begin , block)

    return None

def has_piece(self, piece_index):
    if self.bitfield is None:
        return False
    byte_index = piece_index
    bit_index = 7- (byte_index%8)

    if byte_index >= len(self.bitfield)
       return False
    return bool((self.bitfield[byte_index]>>bit_index)&1)


async def close(self):
    if self.writer:
        self.writer.close()
        await self.writer.wait_closed()
   self.connected = False


async def download_piece_from_peer(peer, piece_index, piece_length , block_size=16384):
     if not peer.has_piece(piece_index):
        return None

    if not peer.interested():
        await peer.send_interested()


    wait_time = 0
    while peer.peer_choking and wait_time < 5:
        msg_id, payload = await peer.recieve_message()
    await asyncio.sleep(0.1)
    wait_time += 0.1

    if peer.peer_choking:
        return None

    blocks_needed = []
    for begin in range(0,piece_length, block_size):
        length = min(block_size,piece_length - begin)
        blocks_needed.append(begin, length)
        await peer.send_request(piece_index, begin, length)
    
    piece_data = {}
    timeout_counter = 0
    max_timeout = 100

    while len(piece_data)< len(blocks_needed) and timeout_counter < max_timeout:
        msg_id, payload = await peer.recieve_message()

        if msg_id is None:
            timeout_counter += 1
            await asyncio.sleep(0.1)
            continue

    result = peer.handle_message(msg_id, payload)
    

        
