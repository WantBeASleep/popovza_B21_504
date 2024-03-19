from glob import glob
import os
from PIL import Image as pim
import numpy as np

def microchel(x, y, arr):
    mat = (arr[y][x] + arr[y][x+1] + arr[y+1][x] + arr[y+1][x+1]) // 4
    disp = (arr[y][x] - mat) ** 2 + (arr[y][x+1] - mat) ** 2 + (arr[y+1][x] - mat) ** 2 + (arr[y+1][x+1] - mat) ** 2
    return mat, disp

def macrochel(x, y, arr):
    mat, disp = microchel(x-1, y+1, arr)

    tmat, tdisp = microchel(x, y+1, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    tmat, tdisp = microchel(x-1, y, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    tmat, tdisp = microchel(x, y, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    # return mat
    return np.uint8(mat)
    

def abc(imgname):
    # inptArr = np.array(pim.open(imgname).convert('L'))
    inptArr = np.array(pim.open(imgname).convert('L'), dtype=np.uint16)
    h, w = inptArr.shape
    newArr = np.zeros((h, w), dtype=np.uint8)
    for y in range (1, h-2):
        for x in range (1, w-2):
            newArr[y][x] = macrochel(x, y, inptArr)
    
    return newArr


inpt = os.path.join(os.path.dirname(__file__), 'input/*')
for name in glob(inpt):
    ans = pim.fromarray(abc(name), mode='L')
    ans.save(os.path.join(os.path.dirname(__file__), 'output', os.path.basename(name)))
