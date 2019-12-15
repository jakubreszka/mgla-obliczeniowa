import socket
import matrix_functions
import json
import queue
import threading

server_ip   = 'localhost'
port_number = 4000
SIZE = 1024
node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tosend = {}
request_queue = queue.Queue()

def getrequests():
    while True:
        package = node_socket.recv(SIZE).decode('utf-8')
        request_queue.put(package)

def showrequests():
    print('Requesty znajdujące się na węźle: ')

def run_node(ip, port):
    try:
        node_socket.connect((server_ip, port_number))
        print(f'Node otrzymuje polecenia z serwera o adresie: {server_ip}:{port_number}')
        runner = threading.Thread(target=getrequests, args=())
        runner.start()
        while True:
            package_json = {}
            if request_queue.empty() is False:
                package_json = json.loads(request_queue.get())
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
    except socket.error as exc:
        #print()
        print(str(exc))

run_node(server_ip, port_number)
