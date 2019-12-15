import socket
import numpy as np 
import time
import hashlib
import json
import threading

def choosefile():
    try:
        print('Podaj nazwe pliku z macierza: ', end='')
        name = input()
        filename = name + '.txt'
        with open(filename, 'r') as f:
            table = json.load(f)
        return table
    except:
        print('Blad odczytu')

server_ip   = 'localhost'
port_number = 5000
SIZE = 1024
disconnect = False
newdata = ''
package = {}
localtime = str(time.time())
h = hashlib.sha1()
h.update(localtime.encode('utf-8'))
print(h.hexdigest())
h_dig = h.hexdigest()
package['sender'] = h_dig
print(package)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((server_ip, port_number))
    print(f'Klient wysyła pakiety na adres: {server_ip}:{port_number}')
    while disconnect is False:
        print('Podaj komende do wywołania: ', end='')
        message = input()
        package['request'] = message
        data = choosefile()
        package['data'] = data
        package_json = json.dumps(package)
        print('Wysyłam zapytanie:')
        print(f'{package_json}')
        client_socket.send(package_json.encode('utf-8'))
        if message == 'disconnect':
            print('Rozłączam się z serwerem')
            disconnect = True
            break
        #zamienic na threada
        while True:
            newdata = client_socket.recv(SIZE).decode('utf-8')
            if newdata != '':
                break
        newdata_json = json.loads(newdata)
        print('Otrzymano odpowiedz z serwera: ')
        print(newdata_json['answer'])
        answerfile = newdata_json['recieving_client'] + '.txt'
        with open(answerfile, 'w+') as ans:
            json.dump(newdata_json['answer'], ans)
except socket.error:
    pass
finally:
    client_socket.close()