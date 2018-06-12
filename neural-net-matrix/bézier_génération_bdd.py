# -*- coding: latin1 -*-
import matplotlib.pyplot as plt
from random import random, randint
import numpy as np
from pygame import image

def generer_image(img_size, n_points, precision) :
    p = n_points
    img_size = int(img_size*1.5)
    Points = [[i*img_size/(p-1), random()*(img_size+1)] for i in range(p)]
    X = []
    Y = []

    #Precision
    n = precision

    #Partie compliquee mais qui marche
    for t in range(n) :
        Droites = [Points]
        for i in range(p-1) :
            Temp = []
            Ref = Droites[-1]
            for j in range(len(Ref)-1) :
                Temp.append([(Ref[j+1][0]-Ref[j][0])*t/n+Ref[j][0], (Ref[j+1][1]-Ref[j][1])*t/n+Ref[j][1]])
            Droites.append(Temp)
        X.append(Droites[-1][0][0])
        Y.append(Droites[-1][0][1])

    X1 = list(map(int, X))
    Y1 = list(map(int, Y))

    #Adaptation de la courbe dans une image
    for i in range(len(X1)-1, 0, -1) :
        if X1[i] == X[i-1] :
            X1.pop(i)
            Y1.pop(i)

    X2 = []
    Y2 = []
    for i in range(len(X1)-1) :
        for k in range(X1[i+1]-X1[i]) :
            X2.append(X1[i]+k)
            Y2.append(Y1[i]+k*(Y[i+1]-Y[i])/(X[i+1]-X[i]))
    X2.append(X1[-1])
    Y2.append(Y1[-1])

    #Recuperation d'images de milieux
    imgforet = image.load("foret.png")
    imgmer = image.load("mer.png")
    xf, yf = imgforet.get_size()
    xm, ym = imgmer.get_size()
    foret0 = image.tostring(imgforet, "RGB")
    mer0 = image.tostring(imgmer, "RGB")
    xif, yif = randint(0, xf-img_size), randint(0, yf-img_size)
    xim, yim = randint(0, xm-img_size), randint(0, ym-img_size)
    foret = b""
    for y in range(img_size) :
        pos = (yif+y)*xf*3+xif*3
        foret += foret0[pos : pos+img_size*3]
    mer = b""
    for y in range(img_size) :
        pos = (yim+y)*xm*3+xim*3
        mer += mer0[pos : pos+img_size*3]

    #Creation de l'image
    def pxl(x,y,c):
        return x*3+c + (img_size*3)*y

    rendu = ""
    for y in range(img_size) :
        for x in range(img_size) :
            if y < Y2[x] : rendu += mer[3*img_size*y+3*x : 3*img_size*y+3*x+3].decode(encoding='latin1')
            else : rendu += foret[3*img_size*y+3*x : 3*img_size*y+3*x+3].decode(encoding='latin1')

    #Application du flou
    def flou(imgstr, imgsize, bsize, x, y, c) :
        infx = max(0, x-bsize)
        supx = min(img_size, x+bsize+1)
        infy = max(0, y-bsize)
        supy = min(img_size, y+bsize+1)
        s, n = 0, 0
        for i in range(infx, supx) :
            for j in range(infy, supy) :
                s += imgstr[pxl(i,j,c)]
                n += 1
        return(int(s/n))

    sq_size=1
    blur_size = 1
    rendu = rendu.encode(encoding='latin1')

    rendu2 = list(rendu)

    for x in range(img_size) :
        inf = int(max(0, Y2[x]-sq_size))
        sup = int(min(img_size, Y2[x]+sq_size+1))
        for y in range(inf, sup) :
            rendu2[pxl(x,y,0)] = flou(rendu, img_size, blur_size, x, y, 0)
            rendu2[pxl(x,y,1)] = flou(rendu, img_size, blur_size, x, y, 1)
            rendu2[pxl(x,y,2)] = flou(rendu, img_size, blur_size, x, y, 2)


    #Application d'une rotation aleatoire
    def rotation(x, y, xcentre, ycentre, theta) :
        z = complex(x-xcentre, y-ycentre)
        z *= np.exp(theta*1j)
        return int(z.real)+xcentre, int(z.imag)+ycentre

    theta = random()*2*np.pi
    rendu3 = []

    for x in range(img_size//6, 5*img_size//6) :
        for y in range(img_size//6, 5*img_size//6) :
            xr, yr = rotation(x, y, img_size//2, img_size//2, theta)
            rendu3.append(rendu2[pxl(xr, yr, 0)])
            rendu3.append(rendu2[pxl(xr, yr, 1)])
            rendu3.append(rendu2[pxl(xr, yr, 2)])

    PtsBezier = [rotation(x, Y2[x], img_size//2, img_size//2, theta) for x in range(img_size)]

    return rendu3, PtsBezier


img_size = 64
n_points = 32
precision = 250
s = ""

"""rendu, pts = generer_image(img_size, n_points, precision)
imgrendu = image.fromstring(bytes(rendu), [img_size]*2, "RGB")
image.save(imgrendu, "rendu.png")
X = [p[0] for p in pts]
Y = [p[1] for p in pts]
plt.plot(X,Y)
plt.show()"""


for i in range(100) :
    print(str(i)+"%")
    for j in range(4) :
        rendu, pts = generer_image(img_size, n_points, precision)
        for c in range(len(rendu)//3) :
            s += str(rendu[3*c])+"."+str(rendu[3*c+1])+"."+str(rendu[3*c+2])+"/"
        s += "\n"
        for pt in pts :
            s += str(pt[0])+"."+str(pt[1])+"/"
        s += "\n"

datafile = open("bordersdata.txt", "w")
datafile.write(s)
datafile.close()
