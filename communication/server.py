import socket

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_number = 5000
size = 1024
serv_address = socket.gethostbyname('0.0.0.0')
serv_socket.bind((serv_address, port_number))
serv_socket.listen(5)
print('Sever is up and running')

while 1:
    client_socket, client_address = serv_socket.accept()
    print('Connection with: ', client_address)
    data = client_socket.recv(size).decode('utf-8')
    print(data)
    if data == 'runtest':
        todo = open('testtt,py', 'r')
        code_str = todo.read()
        todo.close()
        code = compile(code_str, 'testtt.py', exec)
        exec(code)
    else:
        print(data)
    #client_socket.close()
