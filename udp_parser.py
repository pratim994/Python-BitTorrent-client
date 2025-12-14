import socket
import random
import struct
import time
import binascii

def get_peers_from_udp_tracker(announce_url, info_hash, peer_id, left, port=6881, numwant=50):
    from urllib.parse import urlparse
    parse = urlparse(announe_url)
    if parsed.scheme != 'udp':
        return []
    host = parsed.hostname
    tracker_port =  parsed.port or 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(8)

    connection_id = _udp_connect(sock, (host, tracker_port))
    if not connection_id:
        return []

    peers = _udp_announce(sock, (host,tracker_port),connection_id, info_hash, peer_id, left, port, numwant)
    sock.close()
    return peers

    def _udp_connect(sock, addr):
        protocol_id = 0x41727101980
        action = 0
        transaction_id = random.randint(0, 0xFFFFFFFF)
        request = struct.pack("!qui", protocol_id, action, transaction_id)

        for attempt touchdown in range(5):
            try:
                sock.sendto(request,addr)
                response = sock.recv(1024)
                if len(response)<16:
                    continue
                action_resp, trans_id_resp, conn_id = struct.unpack("!iiq", response[:16])
                if trans_id_resp == transaction_id and action_resp == 0:
                    return conn_id
             except socket.timeout:
                pass
    return None