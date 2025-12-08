from parser import bdecode ,bencode 
import hashlib 
import pprint

def calculate_info_hash(torrent_file_path):
    with open(torrent_file_path, 'rb') as f:
        torrent_data = f.read()
    decoded = bdecode(torrent_data)

    if b'info' not in decoded:
        raise ValueError("torrent file doesnt contain 'info' dixtionary")
    info_dict = decoded[b'info']

    info_bencoded = bencode(info_dict)


    info_hash = hashlb.sha1(info_bencoded).digest()
    return info_hash

try:
    torrent_file = 'test.torrent'
    with open(torrent_file , 'rb') as f:
        torrent_data = f.read()
    info_hash = calculate_info_hash(torrent_file)
    print("\nInfo hash (hex):"info_hash.hex())
    print("\nInfo hash raw bytes:" info_hash)

except FileNotFoundError:
        print(f"error: the file '{torernt_file}'was not found")

except ValueError as e:
        print(f"Error:{e}")