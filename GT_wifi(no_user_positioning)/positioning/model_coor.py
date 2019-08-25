#This program will generate the coordinate of reader
#The minimum is 3
#Maximum is 8

import math

def plan_coor(height, num):
    length = round(math.sqrt(4/3) * height, 2)

    a = round(length * (1/4),2)
    b = round(length * (2/4),2)
    c = round(length * (3/4),2)
    r = round(math.sqrt(b**2 - a**2),2)
     

    standard = [(0,0), (length,0), (b,height)]

    if num != 3:   
        extend = [(a,r),(c,r),(b,0),(a,0),(c,0)]
        for i in range(num-3):
            standard.append(extend[i])
    return standard
#get_coor(30,5)