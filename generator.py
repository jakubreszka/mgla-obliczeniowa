import numpy as np
import json

array = np.random.randint(low=-10, high=10, size=(4,4))
array_list = array.tolist()
with open('tablefile.txt', 'w+') as f:
    json.dump(array_list, f)
