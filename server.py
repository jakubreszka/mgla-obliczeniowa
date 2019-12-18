import socket
import threading
import json
import queue
import time

class FogServer():
    clients = []
    nodes = []
    client_threads = []
    node_threads = []
    answers = {}
    request = ''
    requests = queue.Queue()
    node_queue = queue.Queue()

    def __init__(self, hostname=socket.gethostbyname(socket.gethostname()), clientport=5000, nodeport=4000, size=65535):
        #przypisanie adresu ip i portow do komunikacji
        self.hostname = hostname
        self.clientport = clientport
        self.nodeport = nodeport
        self.size = size
        #stworzenie i zbindowanie socketu do komunikacji z węzłami
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientsocket.bind((self.hostname, self.clientport))
        #stworzenie i zbindowanie socketu do komunikacji z nodami
        self.nodesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nodesocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.nodesocket.bind((self.hostname, self.nodeport))

    def acceptconnections(self):
        #maksymalna liczba połączeń
        self.clientsocket.listen(10)
        self.nodesocket.listen(10)
        print(f'Akceptowanie klientów pod adresem: {self.hostname}:{self.clientport}')
        print(f'Dodawanie węzłów pod adresem: {self.hostname}:{self.nodeport}')
        #tworzenie wątków na metody obsługujące przychodzące i martwe połączenia
        client_listener = threading.Thread(target= self.acceptclients)
        node_listener = threading.Thread(target= self.acceptnodes)
        client_remover = threading.Thread(target= self.remove_dead_clients)
        node_remover = threading.Thread(target= self.remove_dead_nodes)
        #uruchomienie wątków
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
            #przyjmowanie połączeń przez socket klientów, dodanie klienta do listy
            client_socket, client_address = self.clientsocket.accept()
            self.addclient(client_socket)
            #wyświetlenie dodanych klientów
            print(f'\nKlient podłączył się z adresu: {client_address}\n')
            self.showclients()
            #utworzenie wątku na metodę zarządzającą połączeniem z klientem
            self.client_threads.append(threading.Thread(target= self.clientconnection, args=(client_socket, client_address)))
            self.client_threads[-1].start()

    def acceptnodes(self):
        while True:
            node_socket, node_address = self.nodesocket.accept()
            self.node_queue.put((node_socket, node_address))
            self.addnode(node_socket)
            print(f'\nDodano węzeł pod adresem: {node_address}\n')
            self.shownodes()
            self.node_threads.append(threading.Thread(target= self.nodeconnection, args=()))
            self.node_threads[-1].start()
            #self.showqueue()

    def clientconnection(self, client, address):
        tosend = {}
        while True:
            try:
                #odbiór pakietu od klienta
                self.request = client.recv(self.size).decode('utf-8')
                print(f'\nOtrzymano polecenie {self.request} od klienta: {address}')
                request_json = json.loads(self.request)
                self.requests.put(request_json)
                #sprawdzenie żądanego polecenia
                if request_json['request'] == 'disconnect':
                    print(f'{address} rozłączył się')
                    self.clients.remove(client)
                    client.close()
                    break
                else:
                    #oczekiwanie na pojawienie się odpowiedzi z węzła
                    while True:
                        if request_json['sender'] in self.answers:
                            tosend = self.answers[request_json['sender']]
                            self.answers.pop(request_json['sender'])
                            break 
                    #wysłanie odpowiedzi do klienta
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
                package = self.requests.get()
                if package['request'] == 'disconnect':
                    pass
                else:
                    #wybranie kolejnego węzła i wysłanie zapytania
                    node, address = self.node_queue.get()
                    print(f'\nWysyłam polecenie na węzeł {address}')
                    node.send(json.dumps(package).encode('utf-8'))
                    self.request = ''
                    #odebranie odpowiedzi od węzła i wstawienie do słownika
                    self.answer = node.recv(self.size).decode('utf-8')
                    print('\nOdpowiedź z węzła: \n' + str(self.answer))
                    answer_json = json.loads(self.answer)
                    self.answer = ''
                    self.answers[answer_json['receiving_client']] = answer_json
                    #wstawienie węzłą z powrotem do kolejki
                    self.node_queue.put((node, address))
            except socket.error as exc:
                print(str(exc))
                node.close()
                self.nodes.remove(node)
                return False
        node.close()
        self.nodes.remove(node)

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
    
    def showqueue(self):
        print('Status kolejki węzłów: ')
        for node in list(self.node_queue.queue):
            print(node)
    
if __name__ == "__main__":
    server = FogServer(hostname='192.168.1.9')
    server.acceptconnections()