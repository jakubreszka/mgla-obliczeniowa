import numpy as np 

def transpose(matrix):
    return np.matrix.transpose(matrix)

def inverse(matrix):
    return np.linalg.inv(matrix)

def multiply(m_a, m_b):
    return np.matmul(m_a, m_b)