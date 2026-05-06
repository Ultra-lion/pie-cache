import socket
import asyncio
import re

from cache_handler import PieCacheManager

SOCKET_SERVER_IP = '127.0.0.1'
SOCKET_SERVER_PORT = 9876

async def cache_worker(reader, writer):
    
    global PieCacheManagerInstance

    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    pat = '(get|put|del) ([A-Za-z0-9].*)'
    match = re.search(pat, message)
    res=""
    if match:
        query_items = match.groups()
        op = query_items[0]
        if op=='get':
            key = query_items[1]
            res = PieCacheManagerInstance.get_cache_item(key)
        elif op=='put':
            key, val = query_items[1].split(' ')
            res = PieCacheManagerInstance.set_cache_item(key,val)
        elif op=='del':
            key = query_items[1]
            PieCacheManagerInstance.del_item_cache(key)
            res = "Done"


        writer.write(res.encode())

    else:
        print("what the helly")
        writer.write("Invalid Query")

    await writer.drain()
    writer.close()
    await writer.wait_closed()



async def main():
    server = await asyncio.start_server(cache_worker, SOCKET_SERVER_IP, SOCKET_SERVER_PORT)
    server_addresses = ', '.join([str(sock.getsockname()) for sock in server.sockets])
    print(f"listening on {server_addresses}")
    
    global PieCacheManagerInstance 
    PieCacheManagerInstance = PieCacheManager()

    async with server:
        await server.serve_forever()


asyncio.run(main=main())

