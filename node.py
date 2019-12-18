import socket
import matrix_functions
import json
import queue
import threading

server_ip   = '192.168.1.9'
port_number = 4000
SIZE = 65535
request_queue = queue.Queue()

def run_node(ip, port, size):
    try:
        #utworzenie socketu łączącego się z serwerem i połączenie się z serwerem
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.connect((server_ip, port_number))
        print('Node otrzymuje polecenia z serwera o adresie: ' + str(server_ip) + ':' + str(port_number), end='')
        #uruchomienie wątku obsługującego odbiór zapytań z serwear
        runner = threading.Thread(target=getrequests, args=(node_socket, size))
        runner.start()
        while True:
            if request_queue.empty() is False:
                tosend = {}
                #pobranie zapytania z kolejki
                package_json = json.loads(request_queue.get())
                print('Otrzymano polecenie: ' + str(package_json['request']))
                print('Macierz przed wykonaniem polecenia: ')
                print(package_json['data'])
                tosend['receiving_client'] = package_json['sender']
                tosend['request'] = package_json['request']
                tosend['data'] = package_json['data']
                #przetworzenie otrzymanej macierzy
                if package_json['request'] == 'transpose':
                    tosend['answer'] = matrix_functions.transpose(package_json['data'])
                    print('Macierz po wykonaniu polecenia: ')
                elif package_json['request'] == 'inverse':
                    tosend['answer'] = matrix_functions.inverse(package_json['data'])
                    print('Macierz po wykonaniu polecenia: ')
                else:
                    print('Nieznane polecenie!')
                    tosend['answer'] = 'Nieznane polecenie!'
                #wysłanie odpowiedzi do serwera
                print('Wysyłam odpowiedź: ')
                print(tosend['answer'])
                tosend_json = json.dumps(tosend)
                node_socket.send(tosend_json.encode('utf-8'))
    except socket.error as exc:
        print(str(exc))

#odbieranie zapytań i wstawianie do kolejki
def getrequests(node, size):
    while True:
        package = node.recv(size).decode('utf-8')
        request_queue.put(package)

#wyświetlenie kolejki zapytań
def showrequests():
    print('Requesty znajdujące się na węźle: \n' + str(list(request_queue.queue)))

if __name__ == "__main__":
    run_node(server_ip, port_number, SIZE)
