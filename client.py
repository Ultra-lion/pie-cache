import socket 


target_host = '127.0.0.1'
target_port = 9876


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client.connect((target_host,target_port))



# client.send("get a12".encode())

# resp = client.recv(4096)

# print(resp)


# client.connect((target_host,target_port))

client.send('put a12 gem'.encode())

resp = client.recv(4096)

print(resp.decode())


client.send("get a12".encode())

resp = client.recv(4096)

print(resp.decode())

# client.connect((target_host,target_port))

# client.send("get a12".encode())

# resp = client.recv(4096)

# print(resp)