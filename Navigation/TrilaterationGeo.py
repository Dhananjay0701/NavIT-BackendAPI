import numpy as np
import json
# import geolocation


# uses Newton-Raspson to find solution to HaverSine Eqns
# function to use from external scripts => main()
def calParHaverSine(router, pos):
    router = router * (3.14 / 180)
    pos = pos * (3.14 / 180)
    
    temp = temp1 = np.repeat(pos, 4, axis = 0)
    temp = (temp - router) / 2
    temp = np.sin(temp)
    temp = np.square(temp)
    
    p1 = temp[:, 0]
    p2 = np.multiply(np.cos(router[:, 0]), np.cos(temp1[:, 0]))
    p3 = np.multiply(p2, temp[:, 1])
    ans = p3 + p1
    
    return ans
    
def calHaverSineDist(router, pos):
    temp = calParHaverSine(router, pos)
    temp = np.arcsin(np.sqrt(temp))
    temp = temp * 2 * 6371
    
    return temp * 1000
    
def calJacobMatrix(router, pos):
    # Common Var
    parHaverSine = calParHaverSine(router, pos)
    router = router * (3.14 / 180)
    pos = pos * (3.14 / 180)
    denom = np.sqrt(parHaverSine - np.square(parHaverSine)) / (2 * 6371)
    
    # partial diffrential wrt latitude
    temp = temp1 = np.repeat(pos, 4, axis = 0)
    temp = temp2 =(temp - router) / 2
    temp = temp3 = np.sin(temp)
    temp2 = np.cos(temp2)
    temp = np.square(temp)
    
    p1 = np.multiply(temp2[:, 0], temp3[:, 0]) * 4
    p2 = np.multiply(np.cos(router[:, 0]), np.sin(pos[:, 0]))
    p2 = np.multiply(p2, temp[:, 1])
    p2 = (p1 - p2)
    ans1 = p2 / denom
    
    # partial diffrential wrt longitude
    temp = temp1 = np.repeat(pos, 4, axis = 0)
    temp = temp2 =(temp - router) / 2
    
    p1 = np.multiply(np.sin(temp2[:, 1]), np.cos(temp2[:, 1]))
    p2 = np.multiply(np.cos(router[:, 0]), np.cos(pos[:, 0]))
    p2 = np.multiply(p1, p2)
    ans2 = p2 / (denom / 2)
    
    return np.concatenate((ans1, ans2), axis = 1)

def calFuncMatrix(router, pos, dist):
    return calHaverSineDist(router, pos) - dist.T

def calPosition(router, pos, dist, steps = 100, verbose = False, lr = .01):
    # router = np.matrix(router)
    for _ in range(steps):
        jacob = calJacobMatrix(router, pos)
        func = calFuncMatrix(router, pos, dist)
        upd = jacob.I.dot(func) * lr
        pos = pos - upd.T
        
        if verbose:
            print(f'\n\nIter{_+1}')
            
            print('Updation Matrix')
            print(upd)
            
            print(f'Position Matrix')
            print(pos.T)
        
    return pos

def calDistFromSignal(signal, freq):
    signal = np.matrix(signal)
    temp = ((27.55 - (20 * np.log10(freq)) + np.abs(signal)) / 20.0)
    temp1 = np.ones((signal.size)) * 10
    return np.power(temp1, temp)


# func that returns lat, long
def main(signal, routerpos, pos):
    signal = np.matrix(signal)
    routerpos = np.matrix(routerpos)
    pos = np.matrix(pos)

    dist = calDistFromSignal(signal, 2412)
    ans = calPosition(routerpos, pos, dist, steps = 100, verbose = False, lr = .05)

    return ans.tolist()[0]
    

if __name__ == '__main__':
    # jsonresp = """{
    #     "router" : {
    #         "MAC1" : -59.77007181,
    #         "MAC2" : -63.74583912,
    #         "MAC3" : -68.55590568,
    #         "MAC4" : -65.74998833
    #     }
    # }"""

    jsonresp = json.dumps({
        "router" : {
            "MAC1" : -59.77007181,
            "MAC2" : -63.74583912,
            "MAC3" : -68.55590568,
            "MAC4" : -65.74998833
        }
    })

    router = {
        'MAC1' : [22.732854, 75.893427],
        'MAC2' : [22.732824, 75.893506],
        'MAC3' : [22.732712, 75.893502],
        'MAC4' : [22.732940, 75.893614]
    }

    pos = np.matrix([22.73293551, 75.89342641])

    print(main(jsonresp, router, pos))


