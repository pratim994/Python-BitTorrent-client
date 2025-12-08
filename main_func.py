import asyncio
from get_peers import get_peers_from_tracker
from connect_peer_async import download_from_peers_async

async def main():
        peers = get_peers_from_tracker('example.torrent') #please change this when you are actually testing your bit torrent client
        if len(peers) == 0:
            print("no peers found in this tracker...exiting")
            return 

        success = await download_from_peers_async(
           ' example.torrent',
           peers,
           'downloadable-file.mkv',
           max_peers = 50
        )
        if success:
            print("dowload successful")
        else:
            print("download uncessful")
        
try:
    asyncio.run(main())
except keyboardInterrupt:
    print("\download interrupted by user")