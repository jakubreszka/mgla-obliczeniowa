import socket
import matrix_functions
import numpy as np
import json

server_ip   = 'localhost'
port_number = 4000
SIZE = 1024
node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tosend = {}
disconnect = False
try:
    node_socket.connect((server_ip, port_number))
    print(f'Node otrzymuje polecenia z serwera o adresie: {server_ip}:{port_number}')
    while disconnect is False:
        package = node_socket.recv(SIZE).decode('utf-8')
        package_json = json.loads(package)
        print(f'Otrzymano polecenie {package_json["request"]}')
        print('Macierz przed wykonaniem polecenia: ')
        print(package_json['data'])
        tosend['recieving_client'] = package_json['sender']
        if package_json['request'] == 'transpose':
            tosend['answer'] = matrix_functions.transpose(package_json['data'])
        elif package_json['request'] == 'inverse':
            tosend['answer'] = matrix_functions.inverse(package_json['data'])
        else:
            print('Nieznane polecenie!')
        print('Macierz po wykonaniu polecenia: ')
        print(tosend['answer'])
        tosend_json = json.dumps(tosend)
        node_socket.send(tosend_json.encode('utf-8'))
        disconnect = True
except socket.error:
    pass
finally:
    node_socket.close()