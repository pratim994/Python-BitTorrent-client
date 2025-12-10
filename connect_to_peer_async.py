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
        