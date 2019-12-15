import socket
import matrix_functions
import threading
import json
import queue
import time

class FogServer():
    clients = []
    nodes = []
    client_threads = []
    node_threads = []
    #struktura slownika - id_klienta: odpowiedz
    answers = {}
    requests = {}
    idle_nodes = []
    request = ''
    requests = queue.Queue()
    nodes_queue = []

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
        print()
        client_listener = threading.Thread(target= self.acceptclients)
        node_listener = threading.Thread(target= self.acceptnodes)
        client_remover = threading.Thread(target= self.remove_dead_clients)
        node_remover = threading.Thread(target= self.remove_dead_nodes)
        client_listener.start()
        node_listener.start()
        client_remover.start()
        node_remover.start()
        client_listener.join()
        node_listener.join()
        client_remover.join()
        node_remover.join()

    def acceptclients(self):
        while True:
            client_socket, client_address = self.clientsocket.accept()
            self.addclient(client_socket)
            print(f'\nKlient podłączył się z adresu: {client_address}')
            self.client_threads.append(threading.Thread(target= self.clientconnection, args=(client_socket, client_address)))
            self.client_threads[-1].start()
            self.showclients()

    def acceptnodes(self):
        while True:
            node_socket, node_address = self.nodesocket.accept()
            self.addnode(node_socket)
            print(f'\nDodano węzeł pod adresem: {node_address}')
            self.shownodes()
            #self.node_threads.append(threading.Thread(target= self.nodeconnection, args=(node_socket, node_address)))
            self.node_threads.append(threading.Thread(target= self.nodeconnection, args=()))
            self.node_threads[-1].start()
            self.nodes_queue.insert(0, (node_socket, node_address))
            print('\nStatus kolejki: \n' + str(self.nodes_queue))

    def clientconnection(self, client, address):
        tosend = {}
        while True:
            try:
                self.request = client.recv(self.size).decode('utf-8')
                print(f'\nOtrzymano polecenie {self.request} od klienta: {address}')
                request_json = json.loads(self.request)
                self.requests.put(request_json)
                if request_json['request'] == 'disconnect':
                    print(f'{address} rozłączył się')
                    self.clients.remove(client)
                    client.close()
                #czesc wyzej wykonuje sie przed dodaniem noda
                #petla while wykonuje sie w trakcie obslugi polaczenia noda
                #kiedy znajduje traf, przerywa sie, konczy sie kod noda i wykonuje pozostaly tej funkcji
                #zamienic to na threada
                while True:
                    if request_json['sender'] in self.answers:
                        tosend = self.answers[request_json['sender']]
                        self.answers.pop(request_json['sender'])
                        break 
                tosend_json = json.dumps(tosend)
                print('\nWysyłam odpowiedź do klienta\n')
                client.send(tosend_json.encode('utf-8'))
            except:
                self.clients.remove(client)
                client.close()
                return False
    
    def nodeconnection(self):
        while True:
            try:
                #czekanie na przyslanie nowego przed dalsza egzekucja kodu
                while True:
                    if self.request != '':
                        break
                node, address = self.select_node()
                #node, address = self.nodes_queue[0]
                #del self.nodes_queue[0]
                #self.nodes_queue.append((node, address))
                # print('\nStatus kolejki: \n' + str(self.nodes_queue))
                package = self.requests.get()
                print(f'\nWysyłam polecenie na węzeł {address}')
                node.send(json.dumps(package).encode('utf-8'))
                self.request = ''
                self.answer = node.recv(self.size).decode('utf-8')
                print('\nOdpowiedź z węzła: \n' + str(self.answer))
                answer_json = json.loads(self.answer)
                self.answer = ''
                self.answers[answer_json['recieving_client']] = answer_json
                #del self.nodes_queue[0]
                #self.nodes_queue.append((node, address))
                print('\nStatus kolejki: \n' + str(self.nodes_queue))
            except socket.error as exc:
                print(str(exc))
                node.close()
                self.nodes.remove(node)
                return False
        node.close()
        self.nodes.remove(node)

    def select_node(self):
        node, address = self.nodes_queue[0]
        del self.nodes_queue[0]
        self.nodes_queue.append((node, address))
        return node, address

    def remove_dead_clients(self):
        while True:
            time.sleep(5)
            for thread in self.client_threads:
                if not thread.is_alive():
                    self.client_threads.remove(thread)
                    print('Usunięto martwy wątek klienta')
                    print(thread)
                    print('Aktywne watki klientów')
                    print(self.client_threads)
    
    def remove_dead_nodes(self):
        while True:
            time.sleep(5)
            for thread in self.node_threads:
                if not thread.is_alive():
                    self.node_threads.remove(thread)
                    print('Usunięto martwy wątek węzła')
                    print(thread)
                    print('Aktywne watki węzłów')
                    print(self.node_threads)
    
    def addclient(self, client):
        if client not in self.clients:
            self.clients.append(client)
        else:
            print('Klient jest już połączony')
    
    def addnode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
        else:
            print('Węzeł jest już połączony')
                
    def showclients(self):
        print('Aktualnie połączeni klienci: ')
        for client in self.clients:
            print(client)
    
    def shownodes(self):
        print('Aktualnie dodane węzły: ')
        for node in self.nodes:
            print(node)
    
if __name__ == "__main__":
    server = FogServer(hostname='localhost')
    server.acceptconnections()