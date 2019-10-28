import numpy as np 

def transpose(matrix):
    n_matrix = np.matrix.transpose(np.array(matrix))
    #n_matrix = np.ascontiguousarray(n_matrix, dtype=np.float32)
    n_matrix = np.array2string()
    return n_matrix

def inverse(matrix):
    return np.linalg.inv(matrix)

def multiply(m_a, m_b):
    return np.matmul(m_a, m_b)