import numpy as np
import json

print('Podaj nazwe pliku wynikowego: ', end='')
name = input()
print('Podaj rozmiar macierzy: ', end='')
x = int(input())
filename = name + '.txt'
array = np.random.randint(low=-10, high=10, size=(x,x))
array_list = array.tolist()
with open(filename, 'w+') as f:
    json.dump(array_list, f)
