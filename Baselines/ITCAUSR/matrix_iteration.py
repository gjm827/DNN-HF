"""
Matrix iteration
Input:
uid_list(list):[uid], uid: the user id of tager users.
Matrix M_sr(numpy arary)
Matrix M_re(numpy array)

Ouput:
Matrix M_x(numpy arary)
"""
import numpy as np 
np.set_printoptions(threshold=np.inf)

def iterate():
    M_x = M_re
    for i in range(0,7):
        M_x = 0.6*M_re + 0.4*np.dot(M_sr,M_x)
    return M_x

if __name__ == '__main__':
    uid_list = load_uid()
    for uid in uid_list:
        #load M_re, M_sr,
        n = M_re.shape[1]
        m = M_sr.shape[0]
        M_x = iterate()