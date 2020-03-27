import socket


while True:
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind(('', 8081))
    s_sock.listen(5)