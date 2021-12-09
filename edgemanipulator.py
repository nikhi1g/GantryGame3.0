from cv2 import cv2
import numpy as np


"""
How it works:
spirals out, finds all the pixels one away
if there are not two it deletes the original pixel
then it takes the ajacent pixels, and makes sure that there are more pixels outside that are not the other pixels it found
checks to see if the ones one away have another one one away
"""
'''
Key:
white: unprocessed edge
2: one away
4: 
'''


def denoise_edges(input_img):
    input_img = input_img.copy() #todo not using .copy might be impacting performance
    img = input_img.copy()
    img.fill(0)
    print(img)

    for x in range(len(img)):
        for y in range(len(img[0])):
            if input_img[x][y] == 255:
                fun_zone = input_img.copy() #declares and initializes fun zone
                fun_zone[x][y] = 10
                potential_points = []

                for i in range(-1,2):
                    for j in range (-1,2):
                        if(i == 0) and (j == 0):
                            continue
                        if fun_zone[x+i][y+j] == 255:
                            fun_zone[x+i][y+j] == 20
                            potential_points.append([x+i, y+j])

                if len(potential_points) < 2:
                    continue
                pointctr = 0
                lastk = 0
                for k, point in enumerate(potential_points):
                    print(point)
                    px,py = point
                    if k == lastk:
                        continue
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (i == 0) and (j == 0):
                                continue
                            if fun_zone[px + i][py + j] == 255:
                                fun_zone[px + i][py + j] == 20
                                pointctr += 1
                                lastk = k







def spiral_out(x,y, spiral_radius):
    for j in range(1,spiral_radius+1):
        for i in range(x-j,x+j+1):
            yield (i,y+j)
            yield (i,y-j)
        for i in range(y-j+1, y+j):
            yield (x+j,i)
            yield (x-j,i)
