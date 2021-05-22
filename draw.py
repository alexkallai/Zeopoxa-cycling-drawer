#!/usr/bin/python

#LONGITUDE - horizontal coordinate
#LATITUDE - vertical coordinate

#importing the required packages
import cv2 as cv
import numpy as np
import csv
import sys
from random import randrange

#Argument value printed for debug and put into variable
try:
    coordinatefilename = sys.argv[1]
    print (coordinatefilename)
except:
    print('One argument is needed.')
    quit()

#Reading in csv file into a reader variable
coordinatelist = []
try:
    with open(coordinatefilename, newline='') as f:
        coordinatefile = csv.reader(f)
        coordinatelist = list(coordinatefile)
except:
    print('Not able to read csv file')
    quit()


#coordinatelist is cast into float from text
coordinatelistfloat = []
for row in coordinatelist:
        coordinatelistfloat.append( [float(row[0]), float(row[1])] ) #list of LAT LON float numbers

#finding max and min values
minlat = coordinatelistfloat[0][1]
maxlat = coordinatelistfloat[0][1]
minlon = coordinatelistfloat[0][0]
maxlon = coordinatelistfloat[0][0]
for row in coordinatelistfloat:
   if row[1]>maxlat: maxlat=row[1] 
   if row[1]<minlat: minlat=row[1] 
   if row[0]>maxlon: maxlon=row[0] 
   if row[0]<minlon: minlon=row[0] 

#Printing min and max values for debug
print('Minimum latitude value:', minlat)
print('Maximum latitude value:', maxlat, 'diff = ', maxlat-minlat)
print('Minimum longitude value:', minlon)
print('Maximum longitude value:', maxlon, 'diff = ', maxlon-minlon)

#Calculating canvas corner coordinates
cminlat = round(minlat-0.5)
cmaxlat = round(maxlat+0.5)
cminlon = round(minlon-0.5)
cmaxlon = round(maxlon+0.5)

#Printing min and max values of canvas
print(cminlat)
print(cmaxlat)
print(cminlon)
print(cmaxlon)

#Parameters for canvas
SCALE = 800
WIDTH = SCALE * (cmaxlon - cminlon) # HORIZONTAL
HEIGHT = SCALE * (cmaxlat - cminlat) # VERTICAL 

#Creating video
video = cv.VideoWriter('output.mp4', fourcc = cv.VideoWriter.fourcc(*'DIVX'), fps=60, frameSize = (WIDTH, HEIGHT))

#Creating image
img = np.zeros((WIDTH,HEIGHT,3), np.uint8)
print(type(img))
#Drawing on image
runvar = 0
for row in coordinatelistfloat:
    img[ round(SCALE*(cmaxlon-row[0])) ][ HEIGHT - round(SCALE*(cmaxlat-row[1])) ][0] = randrange(255)
    img[ round(SCALE*(cmaxlon-row[0])) ][ HEIGHT - round(SCALE*(cmaxlat-row[1])) ][1] = randrange(255)
    img[ round(SCALE*(cmaxlon-row[0])) ][ HEIGHT - round(SCALE*(cmaxlat-row[1])) ][2] = randrange(255)
    if runvar % 10 == 0: 
        video.write(img)
    runvar=runvar+1
    print(runvar)

cv.imshow("Display window", img)
#cv.imwrite('randcolor.png',img)

video.write(img)
video.release()

k = cv.waitKey(0)
cv.destroyAllWindows()