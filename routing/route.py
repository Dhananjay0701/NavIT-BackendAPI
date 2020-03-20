import numpy as np
import cv2
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from routing.a_star import astar
import io
import base64

def route(mapfile, origin, destination):
    # opening converting to bitmap
    with Image.open(mapfile) as img:
        origShape = img.size[::-1]
        imgArr = np.copy(np.asarray(img.convert('L')))

    imgArr[imgArr < 200] = 0
    imgArr[imgArr > 200] = 1

    pathCor = astar(imgArr, origin, destination)
    # pathCor = astar(imgArr, (95, 1202), (1989, 818))

    if not(pathCor):
        return False

    # plotting a* route and thicken it
    path = np.zeros(origShape)
    for arr in pathCor:
        path[arr] = 255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilate = cv2.dilate(path, kernel, iterations=3)
    img = Image.fromarray(dilate)
    img = img.convert('L')
    imgMask = img.copy()
    img.close()
    
    # Dynamically building BLUE route png
    blueArr = np.ones((origShape[0], origShape[1], 3))
    blueArr[:, :, 0] = blueArr[:, :, 0] * 34
    blueArr[:, :, 1] = blueArr[:, :, 1] * 213
    blueArr[:, :, 2] = blueArr[:, :, 2] * 245
    blue = Image.fromarray(np.uint8(blueArr))
    blue.putalpha(imgMask)
    final = blue.copy()

    blue.close()

    # preparing img tobe sent
    imgByteArr = io.BytesIO()
    final.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    encoded_img = base64.b64encode(imgByteArr).decode('UTF-8')

    return encoded_img
