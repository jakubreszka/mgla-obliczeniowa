import numpy as np

array = np.random.randint(low=-10, high=10, size=(4,4))
savedarray = np.savetxt('tablefile.txt', array, fmt='%d')
