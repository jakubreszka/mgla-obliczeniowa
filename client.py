import socket
import numpy as np 

server_ip   = 'localhost'
port_number = 5000
SIZE = 1024
disconnect = False

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((server_ip, port_number))
    print(f'Klient wysyła pakiety na adres: {server_ip}:{port_number}')
    while disconnect is False:
        print('Podaj komende do wywołania: ', end='')
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message == 'disconnect':
            print('Rozłączam się z serwerem')
            disconnect = True
            break
        new_data = client_socket.recv(SIZE).decode('utf-8')
        print(new_data)
except socket.error:
    pass
finally:
    client_socket.close()