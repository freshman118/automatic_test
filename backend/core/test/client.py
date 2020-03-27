import socket

c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_sock.connect(('127.0.0.1', 8081))