import numpy as np
from TrilaterationGeo import calHaverSineDist as hsd

def getElevation(latlong, pos, posEle, dist, floorHeight):
    base = np.square(hsd(pos, latlong))
    dist = np.square(dist)
    ans = np.sqrt(dist - base)
    ans = np.floor((ans + posEle) / floorHeight)

    return ans