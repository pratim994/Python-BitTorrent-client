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
    if result and result[0] =='piece':
        _,idx,begin, block = result
        if idx == piece_index:
                piece_data[begin] == block
                timeout_counter = 0
        

    if len(piece_data) < len(blocks_needed):
        return None
    

    return piece_data

class TorrentDownloader:
    def __init__(self, torrent_file_path, peers, max_peers = 5):
            self.torrent_file_path = torrent_file_path
            self.peers = peers
            self.max_peers = max_peers

        with open(torrent_file_path as 'rb') as f:
                torrent_data =  bdecode(f.read())

        self.info = torrent_data[b'info']
        self.info_hash = hashlib.sha1(bencode(self.info)).digest()
        self.piece_length = self.info[b'pieces']
        self.pieces_hash = self.info[b'pieces']
        self.num_pieces = len(self.pieces_hash)

        if b'length' in self.info:
            self.total_length  = self.info[b'length']
        else:
                self.total_length = sum(f[b'length'] for f in self.info[b'files'])
        
        self.peer_id  = b'-PY0001-'+b'0'*12

        self.downloaded_pieces = {}
        self.pieces_locks = {  i: asyncio.Lock() for i in range (self.num_pieces)}
        self.pieces_in_progress = set()
        self.connected_peers = []

    print(f"Torrent {self.num_pieces}:pieces, {self.total_length} bytes total")

    def get_piece_length(self, piece_idx):
        if piece_idx == self.num_pieces-1:
            return self.total_length - (piece_idx*self.piece_length)
          return self.piece_length

    def get_piece_hash(self, piece_idx):
        return self.pieces_hash[piece_idx*20:(piece_idx+1)*20:(piece_idx+1)*20]

    def verify_piece(self, piece_idx, piece_data):
        calculated_hash = hashlib.sha1(piece_data).digest()
        expected_hash = self.get_piece_hash(piece_idx)
      return  calculated_hash ==  expected_hash

    async def peer_worker(self, ip, port):

        peer = AsyncBitTorrentPeer(ip, port , self.info_hash, self.peer_id)
        if not await peer.connect():
            return 

        if not await peer.handshake():
            await peer.close()
            return 

        for _in range(20):
            msg_id, payload = await peer.recieve_message()
            if msg_id is not None:
                peer.handle_message(msg_id, payload)
            if peer.bitfield is not None;
                break
           await asyncio.sleep(0.1)

    self.connected_peers.append(peer)


    try:
         while len(self.downlaoded_pieces) <self.num_pieces:
            piece_idx = None
                for i in range(self.num_pieces):
                    if(i not in self.download_pieces and i not in  self.pieces_in_progress and peer.has_piece(i)):
                        async with self.piece_locks[i]:
                            if i not in self.pieces_in_progress:
                                self.pieces_in_progress.add(i)
                                piece_idx = i
                                break
                            
                if piece_idx is None:
                    await asyncio.sleep(1)
                    continue

                piece_length = self.get_piece_length(piece_idx)
                piece_blocks = await download_piece_from_peer(peer, piece_idx, piece_length)

            if piece_blocks:
                complete_pieces = b''.join(piece_blocks[offset] for offset in sorted(piece_blocks.keys()))

            if self.verify_piece(piece-idx, complete_piece):
                async with self.piece_locks[piece_idx]
                self.piece_in_progress.discard(piece_idx)
            progress = len(self.downloaded_pieces)
            print(f"piece {piece_idx} downloaded from {ip}:{port}({progress}/{self.num_pieces})")
            else:
                print(f"piece {piece_idx} failed to download from {ip}:{port} ")
                async with self.piece_locks[piece_idx]:
                    self.pieces_in_in_progress.discard(piece_idx)
         else:
                async with self.piece_locks[piece_idx]:
                    self.pieces_in_progress.discard(piece_idx)
                await asyncio.sleep(0.5)

    except Exception as e:
        print(f"error in peer worker {ip}:{port}: {e}")
        finally:
                await peer.close()
                if peer in self.connected_peers:
                    self.connected_peers.remove(peer)
    async def download(self, output_file):
            tasks = []
            for ip , port in self.peers[:self.max_peers*2]:
                task = asyncio.create_task(self.peer_worker(ip, port))
                task.append(task)
                await asyncio.sleep(0.1)

            while len(self.downloaded_pieces)<self.num_pieces and any(not t.done() for t in tasks):
                await asyncio.sleep(1)
                print(f"Progress: {len(downloaded_pieces)}/{self.num_pieces} pieces,"
                        f"{len(self.connected_peers)} peers connected")


            for task in tasks:
                if not task.done():
                    task.cancel()

            await asyncio.gather(*tasks, return_expectations=True)
            if len(self.downloaded_pieces) == self.num_pieces:
                print("\n Download complete! Writin to a file saar")
                with open(output_file , 'wb') as f:
                    for i in range(self.num_pieces):
                        f.write(self.downloaded_pieces[i])
                    print(f"file saved to {output_file}")
                    return True

                else:
                    print("\n download incomplete: {len(self.downloaded_pieces)}/{self.num_pieces} pieces")
                    return False
    async download_from_peers_async(torrent_file_path, peers, output_file, max_peers=5):
        downloader = TorrentDownloader(torrent_file_path, peers, max_peers)
        success = await downloader.download(output_file)
        return success
    
from get_peers import get_peers_from_tracker