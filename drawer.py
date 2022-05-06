import sqlite3
import numpy as np
from random import randrange
import cv2 as cv
import sys

from regex import R

#LONGITUDE - horizontal coordinate
#LATITUDE - vertical coordinate

def processCoordinateData(workoutCoordinatesList):
	processedCoordinates = []
	for workoutCoordinates in workoutCoordinatesList:
		if len(workoutCoordinates) > 0:
			for coordinatePairs in workoutCoordinates:
				if ":" in coordinatePairs:
					latLonPairs = eval(coordinatePairs)
					processedCoordinates.append(latLonPairs)
	return processedCoordinates

def getMinMaxValues(processedCoordinates):
	minLat = 1000
	maxLat = 0
	minLon = 1000
	maxLon = 0

	for element in processedCoordinates:
		for coordinatePair in element:
			# so they are not calculated in every step
			currentLongitude = coordinatePair["longitude"]
			currentLatitude = coordinatePair["latitude"]
			# min max longitude
			if currentLongitude > maxLat:
				maxLat = currentLongitude
			if currentLongitude < minLat:
				minLat = currentLongitude
			# min max latitude
			if currentLatitude > maxLon:
				maxLon = currentLatitude 
			if currentLatitude  < minLon:
				minLon = currentLatitude 
			#print(minLon)
			#print(maxLon)
			#print(minLat)
			#print(maxLat)

	return minLat, maxLat, minLon, maxLon

def main():

	if len(sys.argv) < 2 or len(sys.argv) >= 3:
		print("There should only be one argument, the name of the db!")
		return
	# Query to get all coordinates:
	# sqlite3 $DB "SELECT LATLON_ARRAY FROM main_table"

	# Create connection to db
	con = sqlite3.connect(sys.argv[1])
	cursor = con.cursor()

	# do the query
	cursor.execute('SELECT LATLON_ARRAY FROM main_table')
	# get all workouts' latlon lists
	# it's a list of objects like: ('[{"latitude":47.1,"longitude":18.1},{"latitude":47.1,"longitude":18.1}]',)
	workoutCoordinatesList= cursor.fetchall()

	# this is needed because the coordinates are stored in strings
	processedCoordinates = processCoordinateData(workoutCoordinatesList)

	minLat, maxLat, minLon, maxLon = getMinMaxValues(processedCoordinates)
	#for i in processedCoordinates:
	#	print(i)
	#	input()

	#Calculating canvas corner coordinates
	marginInDegrees = 0.01
	cMinLat = float(minLat-marginInDegrees)
	cMaxLat = float(maxLat+marginInDegrees)
	cMinLon = float(minLon-marginInDegrees)
	cMaxLon = float(maxLon+marginInDegrees)

	#Parameters for canvas
	SCALE = 20000
	WIDTH = int( SCALE * (cMaxLon - cMinLon) ) # HORIZONTAL
	HEIGHT = int( SCALE * (cMaxLat - cMinLat) )# VERTICAL 

	#Creating video
	#video = cv.VideoWriter('output.mp4', fourcc = cv.VideoWriter.fourcc(*'mp4v'), fps=60, frameSize = (WIDTH, HEIGHT))

	#Creating image
	#img = np.zeros((WIDTH,HEIGHT,3), np.uint8)
	img = np.full((WIDTH,HEIGHT,3), fill_value = 255, dtype = np.uint8)
	#print(type(img))
	#print(type(img))
	#Drawing on image

	for index, workout in enumerate(processedCoordinates):
		r = randrange(255)
		g = randrange(255)
		b = randrange(255)

		for idx, coordinatePair in enumerate(workout):
			if idx < len(workout)-1:
				xCoordinate = round(SCALE*(cMaxLon-coordinatePair["latitude"])) 
				yCoordinate = HEIGHT - round(SCALE*(cMaxLat-coordinatePair["longitude"])) 
				xCoordinateplus1 = round(SCALE*(cMaxLon-workout[idx+1]["latitude"])) 
				yCoordinateplus1 = HEIGHT - round(SCALE*(cMaxLat-workout[idx+1]["longitude"])) 

				#cv.line(img, (yCoordinate, xCoordinate), (yCoordinateplus1,xCoordinateplus1), (r,g,b), 6)
				cv.circle(img, (yCoordinate, xCoordinate), 6,(r,g,b), -1 )
				#legacy
				#img[ round(SCALE*(cMaxLon-coordinatePair["latitude"])) ][ HEIGHT - round(SCALE*(cMaxLat-coordinatePair["longitude"])) ][0] = 0
				#img[ round(SCALE*(cMaxLon-coordinatePair["latitude"])) ][ HEIGHT - round(SCALE*(cMaxLat-coordinatePair["longitude"])) ][1] = 0
				#img[ round(SCALE*(cMaxLon-coordinatePair["latitude"])) ][ HEIGHT - round(SCALE*(cMaxLat-coordinatePair["longitude"])) ][2] = 0
	#if index % 10 == 0: 
	#	video.write(img)

	#cv.imshow("Display window", img)
	cv.imwrite('randcolor.png',img)

	#video.write(img)
	#video.release()

	k = cv.waitKey(0)
	cv.destroyAllWindows()

	

if __name__ == '__main__':
	main()