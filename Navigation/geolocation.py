from PIL import Image
import numpy as np

def getImgShape(file):
    with Image.open(file) as img:
        origShape = img.size
    return origShape

def getXY(latlong, tl, bl, br, file):
    origShape = getImgShape(file)
    blOrig = bl
    
    # shifting orig to bl
    bl = bl - blOrig
    br = br - blOrig
    tl = tl - blOrig
    
    # building scaler
    xScale = origShape[0] / (tl[0, 0] - bl[0, 0])
    yScale = origShape[1] / (br[0, 1] - bl[0, 1])
    scaler = np.matrix([xScale, yScale])

    # operating
    latlong = latlong - blOrig
    ans = np.multiply(latlong, scaler)
    ans[0,0] = origShape[0] - ans[0,0]
    
    return ans.tolist()[0]

def main(latlong, tl, bl, br, file):
    return getXY(latlong, tl, bl, br, file)

if __name__ == '__main__':
    bl = np.matrix([22.732826, 75.893359])
    tl = np.matrix([22.732939, 75.893359])
    br = np.matrix([22.732826, 75.893474])

    latlong = bl

    t = main(latlong, tl, bl, br, "../resources/input/blue.jpg")
    print(t)