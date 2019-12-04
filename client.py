import socket
import numpy as np 
import time
import hashlib

def choosefile():
    try:
        print('Podaj nazwe pliku z macierza: ', end='')
        name = input()
        filename = name + '.txt'
        with open(filename, 'r') as f:
            table = f.read()
    except:
        print('Blad odczytu')
    finally:
        return table


server_ip   = 'localhost'
port_number = 5000
SIZE = 1024
disconnect = False
package = np.array([])
localtime = str(time.time())
print(localtime)
h = hashlib.sha1()
h.update(localtime.encode('utf-8'))
print(h.digest())
package = np.append(package, h)
print(package)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((server_ip, port_number))
    print(f'Klient wysyła pakiety na adres: {server_ip}:{port_number}')
    while disconnect is False:
        print('Podaj komende do wywołania: ', end='')
        message = input()
        package = np.append(package, message)
        data = choosefile()
        package = np.append(package, data)
        stringpackage = np.array_str(package)
        print(f'Wysyłam zapytanie: {stringpackage}')
        client_socket.send(stringpackage.encode('utf-8'))
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