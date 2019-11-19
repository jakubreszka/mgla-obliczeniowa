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


class FogServer():
    clients = []
    nodes = []

    def __init__(self, hostname=socket.gethostbyname(socket.gethostname()), clientport=5000, nodeport=4000, size=1024, fogsize=10):
        #przypisanie adresu ip i portow do komunikacji
        self.hostname = hostname
        self.clientport = clientport
        self.nodeport = nodeport
        self.size = size
        #stworzenie i zbindowanie socketu
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #mozliwosc ponownego wykorzystania adresu socketa
        self.clientsocket.bind((self.hostname, self.clientport))
        #stworzenie i zbindowanie socketu do komunikacji z nodami
        self.nodesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nodesocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.nodesocket.bind((self.hostname, self.nodeport))
        #zmienna warunkujaca liczbe polaczen ktore bedzie akceptowac system
        self.fogsize = fogsize

    def acceptclients(self):
        self.clientsocket.listen(10)
        print(f'Akceptowanie klientów pod adresem: {self.hostname}:{self.clientport}')
        while True:
            client_socket, client_address = self.clientsocket.accept()
            self.clientthread = threading.Thread(target= self.clientconnection, args=(client_socket, client_address))
            self.clientthread.start()
            self.addclient(client_socket)
            print(f'Połączenie z adresu: {client_address}')
            self.showclients()
    
    def acceptnodes(self):
        self.nodesocket.listen(10)
        print(f'Dodawanie nodów obliczeniowych pod adresem: {self.hostname}:{self.clientport}')
        while True:
            node_socket, node_address = self.nodesocket.accept()
            self.nodethread = threading.Thread(target= self.nodeconnection, args=(node_socket, node_address))
            self.nodethread.start()
            self.addnode(node_socket)
            print(f'Dodano węzeł pod adresem: {node_address}')
            self.shownodes()

    def acceptconnections(self):
        self.clientsocket.listen(10)
        self.nodesocket.listen(10)
        print(f'Akceptowanie klientów pod adresem: {self.hostname}:{self.clientport}')
        print(f'Dodawanie węzłów pod adresem: {self.hostname}:{self.nodeport}')
        while True:
            client_socket, client_address = self.clientsocket.accept()
            self.clientthread = threading.Thread(target= self.clientconnection, args=(client_socket, client_address))
            self.clientthread.start()
            self.addclient(client_socket)
            print(f'Klient podłączył się z adresu: {client_address}')
            self.showclients()
            node_socket, node_address = self.nodesocket.accept()
            self.nodethread = threading.Thread(target= self.nodeconnection, args=(node_socket, node_address))
            self.nodethread.start()
            self.addnode(node_socket)
            print(f'Dodano węzeł pod adresem: {node_address}')
            self.shownodes()

    def clientconnection(self, client, address):
        self.requesttype = ''
        while True:
            try:
                data = client.recv(self.size).decode('utf-8')
                print(f'Otrzymano polecenie {data} od klienta: {address}')
                if data == 'disconnect':
                    client.close()
                    print(f'{address} rozłączył się')
                    self.clients.remove(client)
                    self.showclients()
                # elif data == 'transpose':
                #     tosend = matrix_functions.transpose([[1,2],[3,4]]).encode('utf-8')
                #     client.send(tosend)
                # elif data == 'inverse':
                #     tosend = matrix_functions.inverse(([1, 2], [3, 4])).encode('utf-8')
                #     client.send(tosend)
                self.requesttype = data
                #return self.requesttype
            except:
                client.close()
                return False
    
    def nodeconnection(self, node, address):
        self.answer = ''
        while True:
            try:
                node.send(self.requesttype.encode('utf-8'))
                #self.answer = node.recv(self.size).decode('utf-8')
                #return self.answer
            except:
                node.close()
                return False
    
    def addclient(self, client):
        if client not in self.clients:
            self.clients.append(client)
        else:
            print('Klient jest już połączony')
    
    def addnode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
        else:
            print('Węzeł znajduje się już w mgle')
                
    def showclients(self):
        print('Aktualnie połączeni klienci: ')
        print(self.clients)
    
    def shownodes(self):
        print('Aktualnie dodane węzły: ')
        print(self.nodes)



if __name__ == "__main__":
    server = FogServer(hostname='localhost')
    server.acceptconnections()
