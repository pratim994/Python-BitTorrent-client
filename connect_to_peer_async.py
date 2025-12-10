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