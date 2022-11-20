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



def getSq(w, h):
    points = [[0, 0, 1], [-w, 0, 1], [-w, -h, 1], [0, -h, 1]]
    points = np.array(points)
    return points

def getTr(w, h):
    points = [[0, -w/2, 1], [0, w/2, 1], [h, 0, 1]]
    points = np.array(points)
    return points



def getRegularNGon(ngon):
    delta_angle=360./ngon
    points=[]
    for i in range(ngon):
        degree=i*delta_angle
        radian=deg2rad(degree)
        x=np.cos(radian)
        y=np.sin(radian)
        points.append((x,y, 1))

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


def makeRmat(degree):
    r=deg2rad(degree)
    c=np.cos(r)
    s=np.sin(r)
    Rmat=np.eye(3)
    Rmat[0,0]=c
    Rmat[0,1]=-s
    Rmat[1, 0]= s
    Rmat[1, 1]=c
    return Rmat

def rotate_Points(degree, points):
    R=makeRmat(degree)
    qT=R @ points.T
    points=qT.T
   
    return points

def makeTmat(tx, ty):
    m = np.eye(3)
    m[0,2] = tx 
    m[1,2] = ty
    return m 

#--main

def main ():
    
    width, height = 1000, 1000
    canvas = np.zeros((height, width, 3), dtype='uint8')


    a= 30
    

    while True :
        
        canvas[:, :, :] = 0

        color=np.random.randint(0, 256, size=3)
        
    

        #pillar
        points=getSq(100, 200)
        T1 = makeTmat(200,0)
        T2 = makeTmat(0, 400)
        T3 = makeTmat(-50, 0)
        Hp =  T1 @ T2 @ T3
        Qp = (Hp @ points.T).T

        Qp=Qp.astype('int')
        drawPolygon(canvas, Qp, color)

        #wing1
        tpoints=getTr(30, 70)
        T4 = makeTmat(100, 200)
        R1 = makeRmat(a)
        T5 = makeTmat(-70, 0)
        Hw = T4 @ R1 @ T5
        Qw = (Hw @ tpoints.T).T

        Qw = Qw.astype('int')
        drawPolygon(canvas, Qw, color)

        #wing2
        T6 = makeTmat(100, 200)
        R2 = makeRmat(a+72)
        T7 = makeTmat(-70, 0)
        Hw2 = T6 @ R2 @ T7
        Qw2 = (Hw2 @ tpoints.T).T

        Qw2 = Qw2.astype('int')
        drawPolygon(canvas, Qw2, color)

        #wing3
        T8 = makeTmat(100, 200)
        R3 = makeRmat(a+144)
        T9 = makeTmat(-70, 0)
        Hw3 = T8 @ R3 @ T9
        Qw3 = (Hw3 @ tpoints.T).T

        Qw3 = Qw3.astype('int')
        drawPolygon(canvas, Qw3, color)

        #wing4
        T10 = makeTmat(100, 200)
        R4 = makeRmat(a+216)
        T11 = makeTmat(-70, 0)
        Hw4 = T10 @ R4 @ T11
        Qw4 = (Hw4 @ tpoints.T).T

        Qw4 = Qw4.astype('int')
        drawPolygon(canvas, Qw4, color)

        #wing5
        T12 = makeTmat(100, 200)
        R5 = makeRmat(a+288)
        T13 = makeTmat(-70, 0)
        Hw5 = T12 @ R5 @ T13
        Qw5 = (Hw5 @ tpoints.T).T

        Qw5 = Qw5.astype('int')
        drawPolygon(canvas, Qw5, color)

        a += 5


        





        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27:
            break

if __name__=="__main__":
    main()