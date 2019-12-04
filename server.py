import socket
import matrix_functions
import threading
import numpy as np

class FogServer():
    clients = []
    nodes = []
    client_threads = []
    node_threads = []
    #struktura slownika - id_klienta: odpowiedz
    answers = {}

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

    def acceptconnections(self):
        self.clientsocket.listen(10)
        self.nodesocket.listen(10)
        print(f'Akceptowanie klientów pod adresem: {self.hostname}:{self.clientport}')
        print(f'Dodawanie węzłów pod adresem: {self.hostname}:{self.nodeport}')
        while True:
            client_socket, client_address = self.clientsocket.accept()
            self.client_threads.append(threading.Thread(target= self.clientconnection, args=(client_socket, client_address)))
            self.client_threads[-1].start()
            self.addclient(client_socket)
            print(f'Klient podłączył się z adresu: {client_address}')
            self.showclients()
            print(self.client_threads)
        while True:
            node_socket, node_address = self.nodesocket.accept()
            self.node_threads.append(threading.Thread(target= self.nodeconnection, args=(node_socket, node_address)))
            self.node_threads[-1].start()
            self.addnode(node_socket)
            print(f'Dodano węzeł pod adresem: {node_address}')
            self.shownodes()
            print(self.node_threads)

    def clientconnection(self, client, address):
        self.request = ''
        while True:
            try:
                self.request = client.recv(self.size).decode('utf-8')
                print(f'Otrzymano polecenie {self.request} od klienta: {address}')
                if data == 'disconnect':
                    client.close()
                    print(f'{address} rozłączył się')
                    self.clients.remove(client)
                    self.client_threads
                    self.showclients()
                client.send(self.answer.encode('utf-8'))
            except:
                client.close()
                return False
    
    def nodeconnection(self, node, address):
        self.answer = ''
        #while True:
        try:
            print(f'Wysyłam polecenie {self.request} na węzeł {address}')
            node.send(self.request.encode('utf-8'))
            self.answer = node.recv(self.size)
            self.answer.decode('utf-8')
            print(self.answer)
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