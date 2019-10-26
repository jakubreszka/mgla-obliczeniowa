import socket 

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_number = 5000
size = 1024
serv_socket.bind(('', port_number))
serv_socket.listen(5)

while 1:
    (client_socket, client_address) = serv_socket.accept()
    print('Connection with: ', client_address)
    data = serv_socket.recv(size)
    print(data)
    client_socket.close()
