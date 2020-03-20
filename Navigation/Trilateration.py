import numpy as np

def calJacobMatrix(router, pos):
    temp = np.repeat(pos, 4, axis = 0)
    temp = (temp - router) * 2
    
    return temp

def calFuncMatrix(router, pos, dist):
    temp = np.repeat(pos, 4, axis = 0)
    temp = temp - router
    temp = np.square(temp)
    temp = temp.sum(axis = 1)
    temp = temp - np.square(dist.T)
    
    return temp

def calPosition(router, pos, dist, steps = 10, verbose = False):
    for _ in range(steps):
        jacob = calJacobMatrix(router, pos)
        func = calFuncMatrix(router, pos, dist)
        upd = jacob.I.dot(func)
        pos = pos - upd.T
        
        if verbose:
            print(f'\n\nIter{_+1}')
            
            print('Updation Matrix')
            print(upd)
            
            print(f'Position Matrix')
            print(pos.T)
        
    return pos


if __name__ == '__main__':
    router = np.matrix([[0, 0, 0],
            [5, 0, 0],
            [10, 0, 0],
            [20, 0, 0]])

    dist = np.matrix([2,
        3,
        8,
        18])

    pos = np.matrix([5, 5, 5])

    print(calPosition(router, pos, dist).T)





