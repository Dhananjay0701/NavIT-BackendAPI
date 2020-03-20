import numpy as np

def latlonToPix(latlong, origShape, bl, br, tl):
    slope = (br[0] - bl[0]) / (br[1] - bl[1])
    theta2 = np.arctan(slope) * -1
    
    tx = (latlong[1] - bl[1]) * np.cos(theta2) - (latlong[0] - bl[0]) * np.sin(theta2)
    txx = (br[1] - bl[1]) * np.cos(theta2) - (br[0] - bl[0]) * np.sin(theta2)
    
    ty = (latlong[1] - bl[1]) * np.sin(theta2) + (latlong[0] - bl[0]) * np.cos(theta2)
    tyy = (tl[1] - bl[1]) * np.sin(theta2) + (tl[0] - bl[0]) * np.cos(theta2)
    
    px = origShape[0] * (tx / txx)
    py = origShape[1] * (ty / tyy)
    
    if px < 0:
        px = 0
    elif px > origShape[0]:
        px = origShape[0]
        
    if py < 0:
        py = 0
    elif py > origShape[1]:
        py = origShape[1] 
    
    return (np.floor(px), np.floor(py))

if __name__ == '__main__':
    origShape = (512, 512)
    # y, x
    bl = (22.737020, 75.894094)
    br = (22.736815, 75.894831)
    tl = (22.737895, 75.894323)

    #latlong = (22.737457, 75.8944625)
    #latlong = (22.737358, 75.894578)
    latlong = (22.738258, 75.893922)

    print(latlonToPix(latlong, origShape, bl, br, tl))