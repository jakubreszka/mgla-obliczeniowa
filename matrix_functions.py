import numpy as np 

def transpose(matrix):
    n_matrix = np.matrix.transpose(np.array(matrix))
    matrix_list = n_matrix.tolist()
    return matrix_list

def inverse(matrix):
    n_matrix = np.linalg.inv(np.array(matrix))
    matrix_list = n_matrix.tolist()
    return matrix_list
