from PIL import Image
import numpy as np

def approx(mapFile, pos):
    # Open Img and covert as bitmap
    with Image.open(mapFile) as img:
        imgArr = np.asarray(img.convert('L')).copy()
    imgArr[imgArr < 200] = 0
    imgArr[imgArr > 200] = 1

    # measure euclid dist to place to nearest path px
    xo, yo = np.where(imgArr == 0)
    x = xo
    y = yo

    px = np.ones((x.shape[0])) * pos[0]
    py = np.ones((x.shape[0])) * pos[1]

    x = x - px
    y = y - py
    x = np.square(x)
    y = np.square(y)
    ans = x + y

    return (xo[np.where(ans == ans.min())[0].tolist()[0]], yo[np.where(ans == ans.min())[0].tolist()[0]])


if __name__ == '__main__':
    mapFile = '../resources/maps/customMap1/floor0/pathonly.jpg'
    xi = 779
    yi = 1372
    print(approx(mapFile, (xi, yi)))