import socket
import matrix_functions

server_ip   = 'localhost'
port_number = 4000
SIZE = 1024
node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tosend = bytes(0)
disconnect = False
try:
    node_socket.connect((server_ip, port_number))
    print(f'Node otrzymuje polecenia z serwera o adresie: {server_ip}:{port_number}')
    while disconnect is False:
        request = node_socket.recv(SIZE).decode('utf-8')
        print(f'Otrzymano polecenie {request}')
        if request == 'transpose':
            tosend = matrix_functions.transpose([[1,2],[3,4]]).encode('utf-8')
        else:
            print('Nieznane polecenie!')
        print(tosend)
        node_socket.send(tosend)
        #disconnect = True
except socket.error:
    pass
finally:
    node_socket.close()