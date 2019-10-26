import socket, sys


server_ip   = '192.168.0.6'
port_number = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(server_ip, port_number))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
message = "Test message".encode('utf-8')
try:
    client_socket.connect((server_ip, port_number))
    client_socket.send(message)
except socket.error:
    pass
finally:
    client_socket.close()