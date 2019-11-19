import socket
import matrix_functions

server_ip   = 'localhost'
port_number = 4000
SIZE = 1024
print(f'Node otrzymuje polecenia z serwera o adresie: {server_ip}:{port_number}')
node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tosend = bytes(0)
try:
    node_socket.connect((server_ip, port_number))
    request = node_socket.recv(SIZE).decode('utf-8')
    print(f'Otrzymano polecenie {request}')
    #if request == 'transpose':
    #    tosend = matrix_functions.transpose([[1,2],[3,4]]).encode('utf-8')
    #elif request == 'inverse':
    #    tosend = matrix_functions.inverse([[1,2],[3,4]]).encode('utf-8')
    #node_socket.send(tosend)

except socket.error:
    pass
finally:
    node_socket.close()