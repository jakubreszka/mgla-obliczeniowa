import socket


server_ip   = '192.168.0.6'
port_number = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(server_ip, port_number))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
message = "Test message"

client_socket.sendto(message.encode('utf-8'),(server_ip, port_number))

#sys.exit()