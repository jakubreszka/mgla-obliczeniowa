import numpy as np 

def transpose(matrix):
    n_matrix = np.array(matrix)
    return np.matrix.transpose(n_matrix)

def inverse(matrix):
    return np.linalg.inv(matrix)

def multiply(m_a, m_b):
    return np.matmul(m_a, m_b)