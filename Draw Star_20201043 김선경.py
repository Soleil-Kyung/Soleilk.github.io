#20201043 김선경

import numpy as np
import cv2

def getline(x0, y0, x1, y1):
    points=[]

    if abs(x1-x0) >= abs(y1-y0):
        if x0<x1 :
            for x in range(x0, x1+1):
                y = (x-x0)*(y1-y0) / (x1-x0)+y0
                yint = int(y)
                points.append((x, yint))
        else:
            for x in range(x1, x0-1):
                y=(x-x0)*(y1-y0)/(x1-x0)+y0
                yint=int(y)
                points.append((x, yint))
        return points
    else:
        if y0<y1 :
            for y in range(y0, y1+1):
                x=(y-y0)*(x1-x0)/(y1-y0)+x0
                xint=int(x)
                points.append((xint, y))
        else :
            for y in range(y1, y0-1):
                x=(y-y0)*(x1-x0)/(y1-y0)+x0
                xint=int(x)
                points.append((xint, y))
        return points

   

def drawLine(canvas,x0,y0, x1, y1, color=(255, 255, 255)):
    xys = getline(x0, y0, x1, y1)
    for xy in xys:
        x, y=xy
        canvas[y, x, :] = color
    return


def deg2rad(deg):
    rad=deg*np.pi/180.
    return rad


def getRegularNGon(ngon):
    delta_angle=360./ngon
    points=[]
    for i in range(ngon):
        degree=i*delta_angle
        radian=deg2rad(degree)
        x=np.cos(radian)
        y=np.sin(radian)
        points.append((x,y))

    points=np.array(points)
    return points

def drawLinePQ(canvas, p, q, color): 
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    return 

def drawPolygon(canvas, pts, color):
    for k in range(pts.shape[0]-1):
        drawLine(canvas, pts[k, 0], pts[k, 1], 
        pts[k+1, 0], pts[k+1, 1], color)

    drawLinePQ(canvas, pts[-1], pts[0], color)


def drawStar(im, points, color):
    n = len(points)
    for i in range(n):
        drawLine(im, points[i, 0], points[i, 1], points[(i+2)%n, 0], points[(i+2)%n, 1], color)
    return

#--main

def main ():
    width, height =1400, 1200
    canvas = np.zeros((height, width, 3), dtype='uint8')


   

    while True :

        color=np.random.randint(0, 256, size=3)
        ngon=5
        points=getRegularNGon(ngon)
        
    
        points=points*100
        points[:, 0] += 500 
        points[:, 1] += 200

        points=points.astype('int')
        drawStar(canvas, points, color)
       

    

    

        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27: 
            break

if __name__ == "__main__":
    main()

