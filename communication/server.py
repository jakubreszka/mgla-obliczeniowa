import socket
import matrix_functions
import threading

# serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# port_number = 5000
# size = 1024
# serv_address = socket.gethostbyname('0.0.0.0')
# #serv_socket.bind((serv_address, port_number))
# serv_socket.bind(('localhost', port_number))
# serv_socket.listen(5)
# print('Serwer uruchomiony')


class NodeManager():
    self.nodes = []

    def acceptnodes(self):
        fog_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fog_socket.bind(('localhost', port_number))
        while True:
            node_socket, node_address = serv_socket.accept()
            print(f'Dodano węzeł pod adresem: {node_socket}')
            if client not in clients:
                clients.append(client)
                Thread(target=clientconnection, args=node_socket).start()

    def nodeconnection(self, nodesocket):
        while True:


class ClientManager():
    clients = []

    def __init__(self, hostname=socket.gethostbyname(socket.gethostname()), port=5000, size=1024):
        self.hostname = hostname
        self.port = port
        self.size = size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # możliwość ponownego wykorzystania adresu socketa
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostname, self.port))

    def acceptclients(self):
        self.socket.listen(10)
        print(f'Akceptowanie klientów pod adresem: {self.hostname}:{self.port}')
        while True:
            client_socket, client_address = self.socket.accept()
            self.clientthread = threading.Thread(target= self.clientconnection, args=(client_socket, client_address))
            self.clientthread.start()
            self.addclient(client_socket)
            print(f'Połączenie z adresu: {client_address}')
            self.showconnecions()
    
    def clientconnection(self, client, address):
        while True:
            try:
                data = client.recv(self.size).decode('utf-8')
                print(f'Otrzymano polecenie {data} od klienta: {address}')
                if data == 'disconnect':
                    client.close()
                    self.clientthread.join()
                    print(f'{address} rozłączył się')
                    self.clients.remove(client)
                    self.showconnecions()
                elif data == 'transpose':
                    tosend = matrix_functions.transpose([[1,2],[3,4]]).encode('utf-8')
                    client.send(tosend)
                elif data == 'inverse':
                    tosend = matrix_functions.inverse(([1, 2], [3, 4])).encode('utf-8')
                    client.send(tosend)
                else:
                    raise error('Nieznana komenda, rozłączam klienta')
            except:
                client.close()
                return False
    
    def addclient(self, client):
        if client not in self.clients:
            self.clients.append(client)
        else:
            print('Klient jest już połączony')
                
    def showconnecions(self):
        print(self.clients)



if __name__ == "__main__":
    manager = ClientManager(hostname='localhost')
    manager.acceptclients()
