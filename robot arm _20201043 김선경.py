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

def getRect(w=4, h=2) :
    hw = w/2
    hh = h/2
    points =[ [hw, hh, 1], [-hw, hh, 1], [-hw, -hh, 1], [hw, -hh, 1]]
    points=np.array(points)
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
    
    width, height = 760, 760
    canvas = np.zeros((height, width, 3), dtype='uint8')
    canvas[:, :, :] = 0

    

    while True :

        color=np.random.randint(0, 256, size=3)
        points=getRect(100, 50)


        #H1
        T1=makeTmat(0, -50)
        T2=makeTmat(50, 50)
        R1=makeRmat(90) 
        
        H1= T2 @ R1 @ T1 
        H11= (H1 @ points.T).T
        H11=H11.astype('int')

        drawPolygon(canvas, H11, color)

         #Q2
        T1=makeTmat(0, -50)
        T3=makeTmat(0,50)
        T4=makeTmat(50, 0)

        R2=makeRmat(20)

        H2 = H1 @ T4 @ T3 @ R2 @ T1
        Q2= (H2 @ points.T).T
        Q2=Q2.astype('int')

        drawPolygon(canvas, Q2, color)

        #Q3
        R3=makeRmat(70)
        H3 = H2 @ T4 @ T3 @ R3 @ T1
        Q3 = (H3 @ points.T).T
        Q3=Q3.astype('int')

        drawPolygon(canvas, Q3, color)

        #Q4
        R4=makeRmat(90)
        T5=makeTmat(50, 0)

        H4= H3 @ T5 @ T3 @ R4 @ T1
        Q4 = (H4 @ points.T).T
        Q4 = Q4.astype('int')

        drawPolygon(canvas, Q4, color)


       

        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27:
            break

if __name__=="__main__":
    main()



        

    