import socket
import time
import hashlib
import json

#zmienne warunkujące połączenie
server_ip   = '192.168.1.9'
port_number = 5000
SIZE = 65535

#odczyt danych z pliku tekstowego podanego przez użytkownika
def choosefile():
    try:
        print('Podaj nazwe pliku z macierza: ', end='')
        name = input()
        filename = name + '.txt'
        with open(filename, 'r') as f:
            table = json.load(f)
        return table
    except:
        print('Błąd odczytu!')

#funkcja realizująca działanie klienta
def run_client(ip, port, size):
    try:
        #utworzenie socketu łączącego się z serwerem
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #wygenerowanie i zapisanie identyfikatora klienta
        localtime = str(time.time())
        h = hashlib.sha1()
        h.update(localtime.encode('utf-8'))
        h_dig = h.hexdigest()
        print(f'Hash klienta: {h_dig}')
        disconnect = False
        #podłączenie do serwera
        client_socket.connect((server_ip, port_number))
        print(f'Klient wysyła pakiety na adres: {server_ip}:{port_number}')
        while disconnect is False:
            #utworzenie słownika z zapytaniem
            package = {}
            package['sender'] = h_dig
            #pobranie od użytkownika komendy do wykonania przez węzeł
            print('Podaj komende do wywołania: ', end='')
            message = input()
            package['request'] = message
            #sprawdzenie czy użytkownik chce się rozłączyć
            if message == 'disconnect':
                print('Rozłączam się z serwerem')
                package['data'] = []
                package_json = json.dumps(package)
                disconnect = True
                print(f'Wysyłam zapytanie: \n {package_json}')
                client_socket.send(package_json.encode('utf-8'))
                break
            else:
                #pobranie macierzy z pliku podanego przez użytkownika
                data = choosefile()
                package['data'] = data
                #zapisanie zapytania do formatu JSON
                package_json = json.dumps(package)
                #wysłanie i kodowanie zapytania
                print(f'Wysyłam zapytanie: \n {package_json}')
                client_socket.send(package_json.encode('utf-8'))
                #zapisanie czasu wysłania zapytania
                start_time = time.time()
                #oczekiwanie na odesłanie odpowiedzi przez serwer
                while True:
                    newdata = client_socket.recv(size).decode('utf-8')
                    if newdata != '':
                        break
                #zapisanie odpowiedzi do JSONa
                newdata_json = json.loads(newdata)
                print('Otrzymano odpowiedz z serwera: ')
                print(newdata_json)
                #obliczenie czasu oczekiwania na odpowiedź
                end_time = time.time() - start_time
                print('Czas od wysłania zapytania do uzyskania odpowiedzi: ' + str(end_time))
                newdata_json['time'] = end_time
                #zapisanie odpowiedzi do pliku tekstowego
                answerfile = newdata_json['receiving_client'] + '.txt'
                with open(answerfile, 'a+') as ans:
                    json.dump(newdata_json, ans)
                    ans.write('\n')
    except socket.error as exc:
        print(str(exc))
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client(server_ip, port_number, SIZE)