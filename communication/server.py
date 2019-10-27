import socket
import testtt
import matrix_functions

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_number = 5000
size = 1024
serv_address = socket.gethostbyname('0.0.0.0')
serv_socket.bind((serv_address, port_number))
serv_socket.listen(5)
print('Serwer uruchomiony')

while 1:
    client_socket, client_address = serv_socket.accept()
    print('Polaczono z: ', client_address)
    data = client_socket.recv(size).decode('utf-8')
    print('Otrzymano polecenie: {0}'.format(data))
    if data == 'runtest':
        tosend = testtt.message('XD')
        client_socket.send(tosend)
    else:
        print(data)
    client_socket.close()
